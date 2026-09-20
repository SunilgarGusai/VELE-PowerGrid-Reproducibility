#!/usr/bin/env python3
"""Reproduce Phase-2 parsing, topology audit, and base DC power-flow outputs."""
from pathlib import Path
import re, hashlib
import numpy as np
import pandas as pd
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
MAT = ROOT/'inputs'/'matpower_8.1'
LEG = ROOT/'inputs'/'legacy_topology'
PARSED = ROOT/'outputs'/'parsed'
DCOUT = ROOT/'outputs'/'dc_base'
PARSED.mkdir(parents=True, exist_ok=True)
DCOUT.mkdir(parents=True, exist_ok=True)

BUS_COLS=['bus_i','type','Pd','Qd','Gs','Bs','area','Vm','Va','baseKV','zone','Vmax','Vmin']
GEN_COLS=['bus','Pg','Qg','Qmax','Qmin','Vg','mBase','status','Pmax','Pmin','Pc1','Pc2','Qc1min','Qc1max','Qc2min','Qc2max','ramp_agc','ramp_10','ramp_30','ramp_q','apf']
BR_COLS=['fbus','tbus','r','x','b','rateA','rateB','rateC','ratio','angle','status','angmin','angmax']

def mat(txt,name):
    m=re.search(rf'mpc\.{name}\s*=\s*\[(.*?)\];',txt,re.S)
    if not m: raise ValueError(f'missing mpc.{name}')
    rows=[]
    for raw in m.group(1).split(';'):
        raw='\n'.join(line.split('%')[0] for line in raw.splitlines()).strip()
        if raw: rows.append([float(x) for x in raw.replace('\n',' ').split()])
    if len({len(r) for r in rows})!=1: raise ValueError(f'nonrectangular {name}')
    return np.array(rows,float)

def scalar(txt,name):
    m=re.search(rf'mpc\.{name}\s*=\s*([^;]+);',txt)
    if not m: raise ValueError(name)
    return float(m.group(1).strip())

def parse_case(path):
    txt=path.read_text()
    bus=mat(txt,'bus'); gen=mat(txt,'gen'); br=mat(txt,'branch'); base=scalar(txt,'baseMVA')
    b=pd.DataFrame(bus,columns=BUS_COLS[:bus.shape[1]]); g=pd.DataFrame(gen,columns=GEN_COLS[:gen.shape[1]]); r=pd.DataFrame(br,columns=BR_COLS[:br.shape[1]])
    b[['bus_i','type']]=b[['bus_i','type']].astype(int); g[['bus','status']]=g[['bus','status']].astype(int); r[['fbus','tbus','status']]=r[['fbus','tbus','status']].astype(int)
    b.insert(0,'node_idx',range(len(b))); g.insert(0,'gen_id',range(1,len(g)+1)); r.insert(0,'branch_id',range(1,len(r)+1))
    return base,b,g,r

def dcpf(base,bus,gen,br):
    ids=bus.bus_i.astype(int).tolist(); idx={bid:i for i,bid in enumerate(ids)}; nb=len(bus); nl=len(br)
    f=np.array([idx[int(v)] for v in br.fbus]); t=np.array([idx[int(v)] for v in br.tbus]); stat=br.status.to_numpy(float); x=br.x.to_numpy(float)
    if np.any((stat>0)&(x==0)): raise ValueError('in-service zero-x branch')
    tap=np.ones(nl); mask=br.ratio.to_numpy(float)!=0; tap[mask]=br.ratio.to_numpy(float)[mask]
    bb=stat/x/tap; shift=br.angle.to_numpy(float)*np.pi/180; pfinj=bb*(-shift)
    Bf=np.zeros((nl,nb)); rr=np.arange(nl); Bf[rr,f]=bb; Bf[rr,t]=-bb
    B=np.zeros((nb,nb)); Pbusinj=np.zeros(nb)
    for k in range(nl):
        B[f[k],:]+=Bf[k,:]; B[t[k],:]-=Bf[k,:]; Pbusinj[f[k]]+=pfinj[k]; Pbusinj[t[k]]-=pfinj[k]
    Pbus=-(bus.Pd.to_numpy(float))/base-Pbusinj-bus.Gs.to_numpy(float)/base
    for row in gen[gen.status>0].itertuples(index=False): Pbus[idx[int(row.bus)]]+=float(row.Pg)/base
    refs=bus.loc[bus.type==3,'bus_i'].astype(int).tolist()
    if len(refs)!=1: raise ValueError(f'expected one ref, got {refs}')
    ref=idx[refs[0]]; nonref=[i for i in range(nb) if i!=ref]; Va0=bus.Va.to_numpy(float)*np.pi/180; Va=Va0.copy()
    Va[nonref]=np.linalg.solve(B[np.ix_(nonref,nonref)], Pbus[nonref]-B[np.ix_(nonref,[ref])].ravel()*Va0[ref])
    Pf=(Bf@Va+pfinj)*base
    rg=gen.index[(gen.status>0)&(gen.bus==refs[0])][0]; old=float(gen.loc[rg,'Pg']); delta=(B[ref,:]@Va-Pbus[ref])*base; new=old+delta
    expected=-(bus.Pd.to_numpy(float)+bus.Gs.to_numpy(float))/base
    for gi,row in gen[gen.status>0].iterrows(): expected[idx[int(row.bus)]]+=(new if gi==rg else float(row.Pg))/base
    inj=B@Va+Pbusinj; residual=inj-expected
    rated=br.rateA.to_numpy(float)>0; loading=np.full(nl,np.nan); loading[rated]=np.abs(Pf[rated])/br.rateA.to_numpy(float)[rated]; overload=rated&(loading>1)
    return refs[0],rg,old,new,delta,Va,Pf,residual,rated,loading,overload

summary=[]; dcsummary=[]
for path in sorted(MAT.glob('case*.m'), key=lambda p:int(re.search(r'\d+',p.stem).group())):
    case=path.stem; base,bus,gen,br=parse_case(path); cdir=PARSED/case; cdir.mkdir(exist_ok=True)
    bus.to_csv(cdir/'bus.csv',index=False); gen.to_csv(cdir/'gen.csv',index=False); br.to_csv(cdir/'branch.csv',index=False); pd.DataFrame({'node_idx':bus.node_idx,'bus_id':bus.bus_i}).to_csv(cdir/'bus_mapping.csv',index=False)
    active=br[br.status>0]; active=active[active.fbus.isin(bus.loc[bus.type!=4,'bus_i'])&active.tbus.isin(bus.loc[bus.type!=4,'bus_i'])]
    edges={tuple(sorted((int(a),int(b)))) for a,b in active[['fbus','tbus']].itertuples(index=False,name=None)}; G=nx.Graph(); G.add_nodes_from(bus.loc[bus.type!=4,'bus_i'].astype(int)); G.add_edges_from(edges)
    on=gen[gen.status>0]; summary.append({'case':case,'baseMVA':base,'buses':len(bus),'isolated_type4_buses':int((bus.type==4).sum()),'bus_type_ref':int((bus.type==3).sum()),'bus_type_pv':int((bus.type==2).sum()),'bus_type_pq':int((bus.type==1).sum()),'generators_total':len(gen),'generators_online':len(on),'generator_buses_online':on.bus.nunique(),'total_Pd_MW':bus.Pd.sum(),'positive_load_MW':bus.loc[bus.Pd>0,'Pd'].sum(),'negative_Pd_MW':bus.loc[bus.Pd<0,'Pd'].sum(),'load_buses_positive':int((bus.Pd>0).sum()),'load_buses_negative':int((bus.Pd<0).sum()),'online_Pg_MW':on.Pg.sum(),'online_Pmax_MW':on.Pmax.sum(),'online_Pmin_MW':on.Pmin.sum(),'branches_total':len(br),'branches_active':len(active),'branches_offline':int((br.status<=0).sum()),'unique_active_simple_edges':len(edges),'parallel_branch_surplus':len(active)-len(edges),'active_rateA_positive':int((active.rateA>0).sum()),'active_rateA_coverage_pct':float((active.rateA>0).mean()*100),'active_rateB_positive':int((active.rateB>0).sum()),'active_rateC_positive':int((active.rateC>0).sum()),'active_zero_x':int((active.x==0).sum()),'active_negative_x':int((active.x<0).sum()),'active_transformer_taps_nonunity':int(((active.ratio!=0)&(~np.isclose(active.ratio,1))).sum()),'active_phase_shifters_nonzero_angle':int((~np.isclose(active.angle,0)).sum()),'components':nx.number_connected_components(G),'connected':nx.is_connected(G),'simple_density':nx.density(G),'simple_diameter':nx.diameter(G)})
    ref,rg,old,new,delta,Va,Pf,residual,rated,loading,overload=dcpf(base,bus,gen,br)
    od=DCOUT/case; od.mkdir(exist_ok=True)
    inj=np.zeros(len(bus)); index={int(v):i for i,v in enumerate(bus.bus_i)}
    for k,row in br.iterrows(): inj[index[int(row.fbus)]]+=Pf[k]; inj[index[int(row.tbus)]]-=Pf[k]
    pd.DataFrame({'node_idx':bus.node_idx.astype(int),'bus_id':bus.bus_i.astype(int),'bus_type':bus.type.astype(int),'Va_input_deg':bus.Va,'Va_dc_deg':Va*180/np.pi,'Pd_MW':bus.Pd,'Gs_MW_at_1pu':bus.Gs,'net_injection_dc_MW':inj}).to_csv(od/'base_dc_bus_results.csv',index=False)
    bo=br[['branch_id','fbus','tbus','x','ratio','angle','status','rateA']].copy(); bo['Pf_dc_MW']=Pf; bo['Pt_dc_MW']=-Pf; bo['abs_flow_MW']=np.abs(Pf); bo['loading_rateA_pu']=loading; bo['overloaded_rateA']=overload; bo.to_csv(od/'base_dc_branch_results.csv',index=False)
    pd.DataFrame(sorted(edges),columns=['source','target']).to_csv(od/'structural_edges.csv',index=False)
    dcsummary.append({'case':case,'ref_bus_id':ref,'slack_gen_id':int(gen.loc[rg,'gen_id']),'slack_Pg_input_MW':old,'slack_Pg_dc_MW':new,'slack_adjustment_MW':delta,'slack_Pmin_MW':float(gen.loc[rg,'Pmin']),'slack_Pmax_MW':float(gen.loc[rg,'Pmax']),'slack_within_limits':bool(gen.loc[rg,'Pmin']-1e-9<=new<=gen.loc[rg,'Pmax']+1e-9),'max_abs_power_balance_residual_MW':float(np.max(np.abs(residual))*base),'max_abs_angle_deg':float(np.max(np.abs(Va*180/np.pi))),'max_abs_branch_flow_MW':float(np.max(np.abs(Pf))),'rated_branches_rateA':int(rated.sum()),'base_overload_count_rateA':int(overload.sum()),'base_overload_fraction_of_rated':float(overload.sum()/rated.sum()) if rated.sum() else np.nan,'max_rateA_loading_pu':float(np.nanmax(loading)) if rated.sum() else np.nan})

pd.DataFrame(summary).to_csv(PARSED/'case_summary.csv',index=False)
pd.DataFrame(dcsummary).to_csv(DCOUT/'base_dc_summary.csv',index=False)

comp=[]
for n in [30,57,118,300]:
    br=pd.read_csv(PARSED/f'case{n}'/'branch.csv'); new={tuple(sorted((int(a),int(b)))) for a,b in br.loc[br.status>0,['fbus','tbus']].itertuples(index=False,name=None)}
    olddf=pd.read_csv(LEG/f'IEEE{n}.csv'); old={tuple(sorted((int(a),int(b)))) for a,b in olddf[['source','target']].itertuples(index=False,name=None)}
    comp.append({'network':f'IEEE{n}','matpower_8_1_unique_edges':len(new),'legacy_unique_edges':len(old),'common_edges':len(new&old),'matpower_only_edges':len(new-old),'legacy_only_edges':len(old-new),'exact_match':new==old})
pd.DataFrame(comp).to_csv(PARSED/'topology_legacy_comparison.csv',index=False)
print('Phase 2 reproduced successfully.')
