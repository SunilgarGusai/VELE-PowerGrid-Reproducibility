"""Independently regenerate the 536 rated physical-circuit capacity-cut bounds."""
from pathlib import Path
import re,hashlib,json,sys
import networkx as nx
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parent
case_names={'ieee57_typ':'pglib_opf_case57_ieee.m',
 'ieee57_api':'api_pglib_opf_case57_ieee__api.m',
 'ieee118_typ':'pglib_opf_case118_ieee.m',
 'ieee118_api':'api_pglib_opf_case118_ieee__api.m'}
sha=json.loads((ROOT/'SOURCE_CASE_SHA256.json').read_text())
def matrix(t,name):
 m=re.search(r'mpc\.'+name+r'\s*=\s*\[([\s\S]*?)\];',t)
 assert m,name
 return np.asarray([[float(v) for v in ln.split('%',1)[0].strip().rstrip(';').split()]
     for ln in m.group(1).splitlines() if ln.split('%',1)[0].strip()],float)
def graph(bus,gen,br):
 G=nx.DiGraph()
 G.add_nodes_from(map(int,bus[:,0]))
 G.add_nodes_from(['SOURCE','SINK'])
 for v in bus:
  if v[2]>0:G.add_edge(int(v[0]),'SINK',capacity=float(v[2]))
 for v in gen:
  p=int(v[0]);G.add_edge('SOURCE',p,capacity=(
   G['SOURCE'][p]['capacity'] if G.has_edge('SOURCE',p) else 0.)+float(v[8]))
 for line in br:
  u,v=int(line[0]),int(line[1]);r=float(line[5])
  for a,b in ((u,v),(v,u)):
   G.add_edge(a,b,capacity=(G[a][b]['capacity'] if G.has_edge(a,b) else 0.)+r)
 return G
old=pd.read_csv(ROOT/'PHASE18_ALL_PHYSICAL_OUTAGES_RIGOROUS_CUT_BOUNDS.csv')
rows=[]
for case,name in case_names.items():
 p=ROOT/'inputs'/name
 assert hashlib.sha256(p.read_bytes()).hexdigest()==sha[name],name
 t=p.read_text();bus=matrix(t,'bus');br=matrix(t,'branch');gen=matrix(t,'gen')
 gen=gen[gen[:,7]>0];br=br[br[:,10]>0]
 assert (bus[:,2]>=0).all() and (bus[:,4]==0).all()
 assert (br[:,2]>=0).all() and (br[:,5]>0).all()
 assert (gen[:,8]>=0).all()
 demand=float(bus[:,2].sum())
 for i in range(len(br)+1):
  current=br if i==0 else np.delete(br,i-1,axis=0)
  network=graph(bus,gen,current)
  flow=nx.maximum_flow_value(network,'SOURCE','SINK',
    flow_func=nx.algorithms.flow.preflow_push)
  lower=max(0.,demand-flow)
  ref=old[(old.condition==case)&(old.branch_id==i)]
  assert len(ref)==1
  assert abs(lower-float(ref.iloc[0].mandatory_shed_lower_bound_MW))<1e-5
  rows.append((case,i,lower))
assert len(rows)==536
new=pd.DataFrame(rows,columns=['condition','branch_id','recomputed_cut_lower_bound_MW'])
output=ROOT/'REGENERATED_536_CUT_LOWER_BOUNDS.csv'
new.to_csv(output,index=False)
heavy=new[(new.condition=='ieee118_api')&(new.branch_id>0)]
found=set(heavy[heavy.recomputed_cut_lower_bound_MW>1e-6].branch_id)
assert found.issuperset({52,53,55,173})
print('PASSED: all 536 source-rated cut bounds match archived results within 1e-5 MW')
print('positive heavy IEEE118 all physical outages',len(found))
