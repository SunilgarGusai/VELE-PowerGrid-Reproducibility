from pathlib import Path
import re,json,hashlib
import numpy as np,pandas as pd,networkx as nx
R=Path(__file__).resolve().parent
lock=json.loads((R/'PHASE18_SELECTION_LOCK_AND_HASHES.json').read_text())
expected=pd.read_csv(R/'PHASE18_ALL_PHYSICAL_OUTAGES_RIGOROUS_CUT_BOUNDS.csv')
names={'ieee57_typ':'pglib_opf_case57_ieee.m','ieee57_api':'api_pglib_opf_case57_ieee__api.m',
       'ieee118_typ':'pglib_opf_case118_ieee.m','ieee118_api':'api_pglib_opf_case118_ieee__api.m'}
def mat(t,key):
 m=re.search(r'mpc\.'+key+r'\s*=\s*\[([\s\S]*?)\];',t)
 assert m is not None
 return np.array([[float(x) for x in line.split('%',1)[0].strip().rstrip(';').split()]
 for line in m.group(1).splitlines() if line.split('%',1)[0].strip()])
checks=[]
for name,fn in names.items():
 p=R/'inputs'/fn
 assert hashlib.sha256(p.read_bytes()).hexdigest()==lock['source_case_sha256'][fn]
 t=p.read_text();bus=mat(t,'bus');gen=mat(t,'gen');br=mat(t,'branch')
 gen=gen[gen[:,7]>0];br=br[br[:,10]>0]
 assert np.all(bus[:,2]>=0) and np.all(bus[:,4]==0) and np.all(br[:,2]>=0) and np.all(br[:,5]>0)
 demand=float(bus[:,2].sum())
 for idx in range(len(br)+1):
  now=np.delete(br,idx-1,axis=0) if idx else br
  G=nx.DiGraph()
  G.add_nodes_from(map(int,bus[:,0]))
  G.add_nodes_from(['SRC','DST'])
  for b in bus:
   if b[2]>0:G.add_edge(int(b[0]),'DST',capacity=float(b[2]))
  for g in gen:
   i=int(g[0]);before=G['SRC'][i]['capacity'] if G.has_edge('SRC',i) else 0.
   G.add_edge('SRC',i,capacity=before+float(g[8]))
  for e in now:
   i,j=int(e[0]),int(e[1]);rating=float(e[5])
   for u,v in ((i,j),(j,i)):
    before=G[u][v]['capacity'] if G.has_edge(u,v) else 0.
    G.add_edge(u,v,capacity=before+rating)
  out=nx.maximum_flow_value(G,'SRC','DST',flow_func=nx.algorithms.flow.preflow_push)
  loss=max(0.,demand-out)
  rr=expected[(expected.condition==name)&(expected.branch_id==idx)]
  assert len(rr)==1
  ref=float(rr.iloc[0].mandatory_shed_lower_bound_MW)
  assert abs(loss-ref)<1e-5,(name,idx,loss,ref)
  checks.append((name,idx,loss))
assert len(checks)==536
print('FRESH_OFFLINE_PGLIB_ONLY_CUT_REPLAY_PASS',len(checks))
