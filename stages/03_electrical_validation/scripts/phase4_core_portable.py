from __future__ import annotations
import os
os.environ.setdefault('OMP_NUM_THREADS','1'); os.environ.setdefault('OPENBLAS_NUM_THREADS','1'); os.environ.setdefault('MKL_NUM_THREADS','1')
import sys, math, random, time, json
from pathlib import Path
import numpy as np, pandas as pd, networkx as nx
from scipy.linalg import eigh
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import shortest_path

SEED=20260812
CASES=['case14','case30','case39','case57','case118','case300']
LABEL={c:c.replace('case','IEEE') for c in CASES}
ATTACKS=['random_attack','adaptive_degree','adaptive_betweenness']
PKG=Path(__file__).resolve().parents[1]
OUT=PKG/'outputs/reproduced_checkpoints'; OUT.mkdir(parents=True,exist_ok=True)

def nkey(v):
    try:return (0,float(v))
    except:return (1,str(v))

def comp_evec(H):
    nodes=sorted(H.nodes(),key=nkey)
    if len(nodes)<=1:return np.zeros(len(nodes))
    A=nx.to_scipy_sparse_array(H,nodelist=nodes,dtype=float,format='csr')
    D=shortest_path(A,directed=False,unweighted=True)
    return np.max(D,axis=1).astype(float)

def vele_comp(H):
    n=len(H)
    if n<=1:return 0.0
    e=comp_evec(H); M=e[:,None]+e[None,:]; np.fill_diagonal(M,0)
    lm=eigh(M,subset_by_index=[n-1,n-1],eigvals_only=True,check_finite=False)[0]
    return 2*float(lm)

def vele(G):
    if len(G)<=1:return 0.0
    return sum(vele_comp(G.subgraph(c)) for c in nx.connected_components(G) if len(c)>1)

def intensity(G): return vele(G)/(len(G)-1) if len(G)>1 else 0.0

def stability(I,I0):
    if I0<=0:return 0.0
    q=max(0.0,I/I0)
    return 0.0 if q==0 else float(2*min(q,1)/(1+q))

def rand_order(G,seed):
    a=sorted(G,key=nkey); random.Random(seed).shuffle(a); return a

def choose_adapt(H,mode):
    nodes=sorted(H,key=nkey)
    if mode=='adaptive_degree':
        d=dict(H.degree());m=max(d.values());return next(v for v in nodes if d[v]==m)
    bc=nx.betweenness_centrality(H,normalized=True);m=max(bc.values());return next(v for v in nodes if np.isclose(bc[v],m,rtol=1e-12,atol=1e-15))

def load_case(case):
    bus=pd.read_csv(PKG/'inputs/parsed'/f'{case}_bus.csv')
    gen=pd.read_csv(PKG/'inputs/parsed'/f'{case}_gen.csv')
    br=pd.read_csv(PKG/'inputs/parsed'/f'{case}_branch.csv')
    summary=pd.read_csv(PKG/'inputs/parsed/case_summary.csv').set_index('case')
    baseMVA=float(summary.loc[case,'baseMVA'])
    dcsummary=pd.read_csv(PKG/'inputs/base_dc/base_dc_summary.csv').set_index('case').loc[case]
    basebr=pd.read_csv(PKG/'inputs/base_dc'/f'{case}_base_dc_branch_results.csv')
    edges=pd.read_csv(PKG/'inputs/structural'/f'{case}_structural_edges.csv')
    G=nx.Graph(); G.add_nodes_from(bus.bus_i.astype(int)); G.add_edges_from(edges[['source','target']].itertuples(index=False,name=None))
    pg0={int(r.gen_id):float(r.Pg) for r in gen.itertuples(index=False)}
    slack_gid=int(dcsummary.slack_gen_id); pg0[slack_gid]=float(dcsummary.slack_Pg_dc_MW)
    baseflow={int(r.branch_id):float(r.Pf_dc_MW) for r in basebr.itertuples(index=False)}
    return bus,gen,br,baseMVA,G,pg0,baseflow,dcsummary,basebr

def bounded_dispatch(pg0,pmin,pmax,target):
    pg0=np.clip(np.asarray(pg0,float),pmin,pmax); pmin=np.asarray(pmin,float);pmax=np.asarray(pmax,float)
    target=float(target); lo=float(pmin.sum()); hi=float(pmax.sum())
    if target<lo-1e-8 or target>hi+1e-8: raise ValueError(f'target {target} outside [{lo},{hi}]')
    p=pg0.copy(); cur=float(p.sum())
    if abs(target-cur)<=1e-9:return p
    if target>cur:
        rem=target-cur; head=pmax-p
        while rem>1e-9:
            avail=head>1e-12; H=float(head[avail].sum())
            if H<=1e-12:break
            add=np.zeros_like(p); add[avail]=rem*head[avail]/H; add=np.minimum(add,head)
            p+=add; rem=target-float(p.sum()); head=pmax-p
    else:
        rem=cur-target; down=p-pmin
        while rem>1e-9:
            avail=down>1e-12; H=float(down[avail].sum())
            if H<=1e-12:break
            sub=np.zeros_like(p); sub[avail]=rem*down[avail]/H; sub=np.minimum(sub,down)
            p-=sub; rem=float(p.sum())-target; down=p-pmin
    delta=target-float(p.sum())
    if abs(delta)>1e-7:
        if delta>0:
            for i in range(len(p)):
                a=min(delta,pmax[i]-p[i]); p[i]+=a; delta-=a
                if delta<=1e-8:break
        else:
            need=-delta
            for i in range(len(p)):
                a=min(need,p[i]-pmin[i]); p[i]-=a; need-=a
                if need<=1e-8:break
    return p

def solve_component(comp_nodes, bus, gen, br, baseMVA, pg0map, original_ref):
    nodes=sorted(map(int,comp_nodes),key=nkey); node_set=set(nodes)
    bsub=bus[bus.bus_i.astype(int).isin(node_set)].copy()
    gsub=gen[(gen.status>0)&(gen.bus.astype(int).isin(node_set))].copy()
    brsub=br[(br.status>0)&br.fbus.astype(int).isin(node_set)&br.tbus.astype(int).isin(node_set)].copy()
    positive_load=float(bsub.Pd.clip(lower=0).sum()); negative_pd=float(bsub.Pd.clip(upper=0).sum()); gs=float(bsub.Gs.sum())
    out={'nodes':len(nodes),'positive_load_MW':positive_load,'negative_Pd_MW':negative_pd,'Gs_MW':gs,'gen_count':len(gsub),'branch_count':len(brsub)}
    if len(gsub)==0:
        out.update(energized=False,served_positive_load_MW=0.0,load_shed_MW=positive_load,negative_injection_curtailed_MW=-negative_pd,generation_MW=0.0,max_balance_residual_MW=0.0,total_abs_flow_MW=0.0,rms_flow_MW=0.0,max_abs_flow_MW=0.0,angle_span_deg=0.0)
        return out, pd.DataFrame(columns=['branch_id','fbus','tbus','Pf_dc_MW','rateA','loading_rateA_pu','overloaded_rateA']), {}
    pmax=gsub.Pmax.to_numpy(float); pmin=gsub.Pmin.to_numpy(float); basepg=np.array([pg0map[int(x)] for x in gsub.gen_id],float)
    raw_target=positive_load + negative_pd + gs; maxcap=float(pmax.sum()); mincap=float(pmin.sum()); shed=0.0; neg_curt=0.0; target=raw_target
    if target>maxcap: shed=min(positive_load,target-maxcap); target-=shed
    if target<mincap:
        need=mincap-target; available=-negative_pd; neg_curt=min(need,available); target+=neg_curt
    if target<mincap-1e-7 or target>maxcap+1e-7:
        out.update(energized=False,served_positive_load_MW=0.0,load_shed_MW=positive_load,negative_injection_curtailed_MW=-negative_pd,generation_MW=0.0,max_balance_residual_MW=np.nan,total_abs_flow_MW=0.0,rms_flow_MW=0.0,max_abs_flow_MW=0.0,angle_span_deg=np.nan)
        return out, pd.DataFrame(columns=['branch_id','fbus','tbus','Pf_dc_MW','rateA','loading_rateA_pu','overloaded_rateA']), {}
    dispatch=bounded_dispatch(basepg,pmin,pmax,target)
    alpha=1.0 if positive_load<=0 else max(0.0,(positive_load-shed)/positive_load)
    served_pd=np.where(bsub.Pd.to_numpy(float)>0,bsub.Pd.to_numpy(float)*alpha,bsub.Pd.to_numpy(float))
    if negative_pd<0 and neg_curt>0:
        neg_scale=max(0.0,1-neg_curt/(-negative_pd)); served_pd=np.where(served_pd<0,served_pd*neg_scale,served_pd)
    idx={bid:i for i,bid in enumerate(nodes)}; nb=len(nodes); nbranch=len(brsub)
    if nbranch==0:
        out.update(energized=True,served_positive_load_MW=positive_load-shed,load_shed_MW=shed,negative_injection_curtailed_MW=neg_curt,generation_MW=float(dispatch.sum()),max_balance_residual_MW=0.0,total_abs_flow_MW=0.0,rms_flow_MW=0.0,max_abs_flow_MW=0.0,angle_span_deg=0.0)
        return out,pd.DataFrame(columns=['branch_id','fbus','tbus','Pf_dc_MW','rateA','loading_rateA_pu','overloaded_rateA']),dict(zip(gsub.gen_id.astype(int),dispatch))
    f=np.array([idx[int(x)] for x in brsub.fbus],int); t=np.array([idx[int(x)] for x in brsub.tbus],int)
    x=brsub.x.to_numpy(float); ratio=brsub.ratio.to_numpy(float); tap=np.where(ratio!=0,ratio,1.0); bb=1.0/x/tap
    shift=brsub.angle.to_numpy(float)*np.pi/180; pfinj=bb*(-shift)
    rows=np.r_[f,f,t,t]; cols=np.r_[f,t,f,t]; vals=np.r_[bb,-bb,-bb,bb]; B=coo_matrix((vals,(rows,cols)),shape=(nb,nb)).tocsr()
    Pbusinj=np.zeros(nb); np.add.at(Pbusinj,f,pfinj); np.add.at(Pbusinj,t,-pfinj)
    Pnet=-(served_pd + bsub.Gs.to_numpy(float))/baseMVA; tmp=Pnet.copy(); Pnet=np.zeros(nb)
    for r,bid in enumerate(bsub.bus_i.astype(int)): Pnet[idx[bid]]=tmp[r]
    for row,pg in zip(gsub.itertuples(index=False),dispatch): Pnet[idx[int(row.bus)]] += float(pg)/baseMVA
    rhs=Pnet-Pbusinj
    if int(original_ref) in node_set: ref=int(original_ref)
    else:
        agg=gsub.groupby('bus').Pmax.sum().reset_index(); mx=agg.Pmax.max(); ref=int(sorted(agg.loc[np.isclose(agg.Pmax,mx),'bus'].astype(int).tolist())[0])
    ri=idx[ref]; non=np.array([i for i in range(nb) if i!=ri],int); theta=np.zeros(nb)
    if len(non): theta[non]=spsolve(B[non][:,non],rhs[non])
    Pf=(bb*(theta[f]-theta[t])+pfinj)*baseMVA; residual=(B@theta + Pbusinj)-Pnet
    rate=brsub.rateA.to_numpy(float); rated=rate>0; loading=np.full(nbranch,np.nan); loading[rated]=np.abs(Pf[rated])/rate[rated]
    bo=brsub[['branch_id','fbus','tbus','rateA']].copy(); bo['Pf_dc_MW']=Pf;bo['loading_rateA_pu']=loading;bo['overloaded_rateA']=rated&(loading>1+1e-12)
    out.update(energized=True,served_positive_load_MW=positive_load-shed,load_shed_MW=shed,negative_injection_curtailed_MW=neg_curt,generation_MW=float(dispatch.sum()),max_balance_residual_MW=float(np.max(np.abs(residual))*baseMVA),total_abs_flow_MW=float(np.sum(np.abs(Pf))),rms_flow_MW=float(np.sqrt(np.mean(Pf**2))),max_abs_flow_MW=float(np.max(np.abs(Pf))),angle_span_deg=float((theta.max()-theta.min())*180/np.pi))
    return out,bo,dict(zip(gsub.gen_id.astype(int),dispatch))

def evaluate_state(active_nodes,bus,gen,br,baseMVA,G0,pg0map,baseflow,original_ref,base_positive_load,base_flow_burden):
    active=set(map(int,active_nodes)); H=G0.subgraph(active).copy(); comps=[set(c) for c in nx.connected_components(H)] if len(H) else []
    compouts=[]; flowframes=[]; dispatch={}
    for ci,c in enumerate(comps,1):
        co,ff,dd=solve_component(c,bus,gen,br,baseMVA,pg0map,original_ref);co['component_id']=ci;compouts.append(co)
        if len(ff):ff=ff.copy();ff['component_id']=ci;flowframes.append(ff)
        dispatch.update(dd)
    cdf=pd.DataFrame(compouts); flows=pd.concat(flowframes,ignore_index=True) if flowframes else pd.DataFrame(columns=['branch_id','fbus','tbus','rateA','Pf_dc_MW','loading_rateA_pu','overloaded_rateA','component_id'])
    remaining_bus=bus[bus.bus_i.astype(int).isin(active)]; surviving_pos=float(remaining_bus.Pd.clip(lower=0).sum()); removed_load=base_positive_load-surviving_pos
    served=float(cdf.served_positive_load_MW.sum()) if len(cdf) else 0.; shed=float(cdf.load_shed_MW.sum()) if len(cdf) else 0.; energ_comps=int(cdf.energized.sum()) if len(cdf) else 0; deenerg=len(cdf)-energ_comps
    largest_energ=max([int(r.nodes) for r in cdf.itertuples() if r.energized],default=0); totalflow=float(flows.Pf_dc_MW.abs().sum()) if len(flows) else 0.; maxflow=float(flows.Pf_dc_MW.abs().max()) if len(flows) else 0.; rms=float(np.sqrt(np.mean(flows.Pf_dc_MW.to_numpy(float)**2))) if len(flows) else 0.
    rated=flows.rateA.to_numpy(float)>0 if len(flows) else np.array([],bool); over=flows.overloaded_rateA.to_numpy(bool) if len(flows) else np.array([],bool); maxload=float(np.nanmax(flows.loading_rateA_pu)) if rated.any() else np.nan
    if len(flows):
        b0=np.array([baseflow[int(i)] for i in flows.branch_id],float); fs=flows.Pf_dc_MW.to_numpy(float); den=float(np.sum(np.abs(b0))); flow_redist=float(np.sum(np.abs(fs-b0))/den) if den>1e-12 else np.nan
    else: flow_redist=np.nan
    burden=totalflow/served if served>1e-9 else np.nan; burden_ratio=burden/base_flow_burden if np.isfinite(burden) and base_flow_burden>0 else np.nan
    metrics=dict(nodes_remaining=len(active),components=len(comps),energized_components=energ_comps,deenergized_components=deenerg,largest_energized_component_bus_fraction=largest_energ/len(G0) if len(G0) else 0,surviving_positive_load_MW=surviving_pos,removed_positive_load_MW=removed_load,served_positive_load_MW=served,unserved_surviving_load_MW=shed,surviving_load_served_fraction=served/surviving_pos if surviving_pos>0 else 1.0,system_served_load_fraction=served/base_positive_load if base_positive_load>0 else 1.0,total_generation_MW=float(cdf.generation_MW.sum()) if len(cdf) else 0.,negative_injection_curtailed_MW=float(cdf.negative_injection_curtailed_MW.sum()) if len(cdf) else 0.,total_abs_flow_MW=totalflow,rms_flow_MW=rms,max_abs_flow_MW=maxflow,flow_redistribution_stress=flow_redist,flow_burden_MWperMW=burden,flow_burden_ratio_to_base=burden_ratio,rated_surviving_branches=int(rated.sum()),overload_count_rateA=int(over.sum()),overload_fraction_rateA=float(over.sum()/rated.sum()) if rated.sum() else np.nan,max_rateA_loading_pu=maxload,max_component_balance_residual_MW=float(cdf.max_balance_residual_MW.max()) if len(cdf) else 0.)
    return metrics,cdf,flows,dispatch,H
