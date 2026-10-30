from pathlib import Path
import re,hashlib,json,numpy as np,pandas as pd,networkx as nx
R=Path(__file__).resolve().parent
lock=json.loads((R/'SOURCE_CASE_SHA256.json').read_text())
src=R/'inputs'/'api_pglib_opf_case118_ieee__api.m'
assert hashlib.sha256(src.read_bytes()).hexdigest()==lock[src.name]
t=src.read_text()
def mat(key):
 m=re.search(r'mpc\.'+key+r'\s*=\s*\[([\s\S]*?)\];',t)
 return np.array([[float(v) for v in line.split('%',1)[0].strip().rstrip(';').split()] for line in m.group(1).splitlines() if line.split('%',1)[0].strip()])
bus=mat('bus');gen=mat('gen');br=mat('branch')
gen=gen[gen[:,7]>0];br=br[br[:,10]>0]
prior=pd.read_csv(R/'PHASE18_IEEE118_API_CONNECTED_PROVABLE_SHEDDING.csv')
rows=[]
for p in prior.itertuples():
 k=int(p.branch_id)
 rest=np.delete(br,k-1,axis=0)
 G=nx.DiGraph();G.add_nodes_from(map(int,bus[:,0]))
 G.add_nodes_from(['s','t'])
 for row in bus:
  if row[2]>0:G.add_edge(int(row[0]),'t',capacity=float(row[2]))
 for row in gen:
  u=int(row[0]);x=float(row[8]);G.add_edge('s',u,capacity=(G['s'][u]['capacity'] if G.has_edge('s',u) else 0.)+x)
 for row in rest:
  a,b=int(row[0]),int(row[1]);v=float(row[5])
  for i,j in [(a,b),(b,a)]:
   before=G[i][j]['capacity'] if G.has_edge(i,j) else 0
   G.add_edge(i,j,capacity=before+v)
 val,(left,right)=nx.minimum_cut(G,'s','t',capacity='capacity',
                                flow_func=nx.algorithms.flow.edmonds_karp)
 sinknodes=sorted(x for x in right if isinstance(x,int))
 sinkset=set(sinknodes)
 demand=sum(float(q[2]) for q in bus if int(q[0]) in sinkset)
 power=sum(float(q[8]) for q in gen if int(q[0]) in sinkset)
 boundaries=[float(q[5]) for q in rest if (int(q[0]) in sinkset)!=(int(q[1]) in sinkset)]
 limit=sum(boundaries)
 deficit=demand-power-limit
 assert abs(deficit-p.mandatory_shed_lower_bound_MW)<1e-5,(k,deficit,p.mandatory_shed_lower_bound_MW)
 assert deficit>0 and abs(val-(np.maximum(bus[:,2],0).sum()-deficit))<1e-5
 rows.append({'branch_id':k,'source_version':'pglib-opf-v23.07-ieee118-api',
 'source_sha256':lock[src.name],
 'sink_cut_buses':','.join(map(str,sinknodes)),
 'sink_cut_bus_count':len(sinknodes),'cut_positive_demand_MW':demand,
 'cut_generator_total_Pmax_MW':power,'cut_remaining_branch_RATEA_sum_MVA':limit,
 'cut_certificate_minimum_shed_MW':deficit,
 'networkx_second_solver':'edmonds_karp','independent_match_to_preflow_push':True,
 'VELE_delta_zero':bool(p.vele_zero)})
x=pd.DataFrame(rows)
x.to_csv(R/'PHASE18_EXPLICIT_13_CONNECTED_AC_CUT_CERTIFICATES.csv',index=False)
print('SECOND_ALGORITHM_13_CUT_CERTIFICATES_PASS',len(x))
print(x[['branch_id','sink_cut_bus_count','cut_positive_demand_MW','cut_generator_total_Pmax_MW','cut_remaining_branch_RATEA_sum_MVA','cut_certificate_minimum_shed_MW','VELE_delta_zero']].to_string(index=False))
