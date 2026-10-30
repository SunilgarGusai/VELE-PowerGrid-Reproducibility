"""Reproducible VELE03 journal figures. Source figures are independently generated from frozen inputs."""
from pathlib import Path
# Run certified_cut_v2/fetch_pglib_v23_07_sources.py first to populate the pinned inputs.
import math,re,json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.lines import Line2D
import numpy as np,pandas as pd
BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/'certified_cut_v2'
OUT=BASE/'docs'/'assets'/'v2-figures';OUT.mkdir(parents=True,exist_ok=True)
NAVY='#173750';INK='#172634';TEAL='#11788A';ORANGE='#B86A3B';MUTED='#657889';BG='#F4F8FA';LINE='#CFDDE4'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.3,'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,'pdf.fonttype':42,'svg.fonttype':'none'})
audit=[]
def finish(fig,name,inputs):
 for ext,kw in [('png',dict(dpi=340)),('pdf',{}),('svg',{})]:
  fig.savefig(OUT/(name+'.'+ext),bbox_inches='tight',pad_inches=.10,facecolor='white',**kw)
 plt.close(fig)
 from PIL import Image
 im=Image.open(OUT/(name+'.png'))
 audit.append(dict(name=name,pixels=im.size,inputs={Path(p).name:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in inputs},
               png_sha256=hashlib.sha256((OUT/(name+'.png')).read_bytes()).hexdigest()))
def make_ax(size):
 fig,ax=plt.subplots(figsize=size);ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');return fig,ax
def box(ax,x,y,w,h,title,sub,color):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.008,rounding_size=.015',lw=1.15,ec=LINE,fc='white',transform=ax.transAxes,zorder=2))
 ax.add_patch(Rectangle((x+.003,y+.018),.008,h-.036,fc=color,transform=ax.transAxes,zorder=3))
 ax.text(x+.026,y+h-.071,title,fontsize=9.0,fontweight='bold',color=NAVY,va='center',transform=ax.transAxes,zorder=4)
 for j,t in enumerate(sub):
  ax.text(x+.026,y+h-.135-j*.048,t,fontsize=7.2,color=MUTED,va='center',transform=ax.transAxes,zorder=4)
def arr(ax,x0,x1,y):
 ax.add_patch(FancyArrowPatch((x0,y),(x1,y),arrowstyle='-|>',mutation_scale=15,lw=1.55,color=NAVY,transform=ax.transAxes,zorder=5))
# FIGURE 1: no text outside cards. Two cohorts, separate methods and outcomes.
fig,ax=make_ax((7.15,3.08))
ax.text(.02,.978,'VALIDATION DESIGN',fontsize=9.1,fontweight='bold',color=NAVY,va='top')
ax.text(.98,.978,'Two source cohorts • distinct endpoints',fontsize=8.25,color=MUTED,ha='right',va='top')
ax.text(.02,.892,'A  |  STRUCTURAL–DC OBSERVABILITY',fontsize=9.2,fontweight='bold',color=TEAL,va='center')
for x,t,sub in [(.020,'MATPOWER 8.1',['6 IEEE systems','784 physical outages']),
                (.364,'VELE structure',['VELE + mean ecc.','simple graph projection']),
                (.708,'DC flow proxy',['Flow redistribution','not AC curtailment'])]:
 box(ax,x,.61,.272,.242,t,sub,TEAL)
for x in (.020,.364):arr(ax,x+.283,x+.334,.733)
ax.plot([.02,.98],[.54,.54],color=LINE,lw=1,transform=ax.transAxes)
ax.text(.02,.477,'B  |  SOURCE-RATED NECESSARY CURTAILMENT',fontsize=9.2,fontweight='bold',color=ORANGE,va='center')
for x,t,sub in [(.020,'PGLib-OPF v23.07',['IEEE57 / IEEE118','typical & stressed']),
                (.364,'Physical cuts',['Generator Pmax','circuit MVA limits']),
                (.708,'MW cut bound',['Necessary curtailed load','not an AC OPF'])]:
 box(ax,x,.139,.272,.242,t,sub,ORANGE)
for x in (.020,.364):arr(ax,x+.283,x+.334,.262)
ax.text(.5,.042,'Evidence streams are analysed separately, never pooled.',fontsize=8.5,style='italic',ha='center',color=MUTED)
finish(fig,'Fig1_Study_Design',[])
# FIGURE 2: actual branch 52 removed; source-rated remaining cut.
sourcefile=SOURCE/'inputs'/'api_pglib_opf_case118_ieee__api.m'
def mat(t,name):
 m=re.search(r'mpc\.'+name+r'\s*=\s*\[([\s\S]*?)\];',t)
 return np.array([[float(z) for z in l.split('%',1)[0].rstrip(';').split()]
           for l in m.group(1).splitlines() if l.split('%',1)[0].strip()])
br=mat(sourcefile.read_text(),'branch')
assert tuple(map(int,br[51,:2]))==(37,39) and br[51,5]==151
live=br[br[:,10]>0];remaining=np.delete(live,51,axis=0);S={39,40,41,42}
cross=sorted([(int(q[0]),int(q[1]),float(q[5])) for q in remaining if (int(q[0]) in S)!=(int(q[1]) in S)])
assert cross==sorted([(37,40,140.0),(42,49,89.0),(42,49,89.0)])
local=sorted([tuple(map(int,q[:2])) for q in remaining if int(q[0]) in S and int(q[1]) in S])
assert local==sorted([(39,40),(40,41),(40,42),(41,42)])
fig,ax=make_ax((7.15,3.4))
ax.text(.02,.972,'IEEE118  |  STRESSED OPERATION  |  CIRCUIT 52 REMOVED',fontsize=10.2,color=NAVY,fontweight='bold',va='top')
ax.add_patch(FancyBboxPatch((.48,.18),.495,.65,boxstyle='round,pad=.008,rounding_size=.018',
                            ec='#B7D6DB',fc='#EDF7F8',lw=1.1,transform=ax.transAxes))
ax.text(.73,.798,'CRITICAL SET  S = {39, 40, 41, 42}',fontsize=9.1,fontweight='bold',ha='center',color=NAVY)
ax.text(.15,.80,'OUTSIDE S',fontsize=9.0,fontweight='bold',ha='center',color=MUTED)
pos={37:(.17,.57),49:(.17,.27),39:(.58,.72),40:(.79,.63),41:(.59,.41),42:(.79,.28)}
for u,v in local:
 x,y=pos[u];p,q=pos[v];ax.plot([x,p],[y,q],color='#82A6B1',lw=2.2,transform=ax.transAxes,zorder=1)
ax.plot([pos[37][0],pos[40][0]],[pos[37][1],pos[40][1]],lw=2.5,color=ORANGE,transform=ax.transAxes,zorder=2)
for off in [-.012,.012]:
 ax.plot([pos[49][0],pos[42][0]],[pos[49][1]+off,pos[42][1]+off],lw=2.1,color=ORANGE,transform=ax.transAxes,zorder=2)
ax.plot([pos[37][0],pos[39][0]],[pos[37][1],pos[39][1]],ls=(0,(4,3)),lw=1.8,color='#AD4B4B',transform=ax.transAxes,zorder=1)
ax.text(.345,.755,'REMOVED 52',fontsize=8.1,color='#AD4B4B',ha='center',fontweight='bold')
ax.text(.45,.540,'140 MVA',fontsize=8.6,color=ORANGE,ha='center',fontweight='bold')
ax.text(.42,.326,'2 × 89 MVA',fontsize=8.6,color=ORANGE,ha='center',fontweight='bold')
for n,(x,y) in pos.items():
 ax.add_patch(Circle((x,y),.029,fc='#D9EDF0' if n in S else '#F1F3F5',ec=NAVY,lw=1.3,transform=ax.transAxes,zorder=5))
 ax.text(x,y,str(n),fontsize=8.8,fontweight='bold',ha='center',va='center',transform=ax.transAxes,zorder=6)
ax.text(.51,.113,'Demand in S: 378.29 MW     Local Pmax: 0 MW     Remaining interface: 318 MVA',ha='center',fontsize=8.5)
ax.text(.51,.044,'Certified unavoidable curtailed demand  ≥  60.29 MW',ha='center',fontsize=10.7,color=ORANGE,fontweight='bold')
finish(fig,'Fig2_Branch52_Physical_Cut',[sourcefile])
# FIGURE 3: independent 13 certificates; color = eccentricity response.
cutfile=SOURCE/'PHASE18_EXPLICIT_13_CONNECTED_AC_CUT_CERTIFICATES.csv'
cuts=pd.read_csv(cutfile)
assert len(cuts)==13
zero={int(x) for x in cuts.loc[cuts.VELE_delta_zero.astype(bool),'branch_id']}
assert zero=={52,53,55,173}
data=cuts.sort_values('cut_certificate_minimum_shed_MW')
vals=data.cut_certificate_minimum_shed_MW.to_numpy(float)
ids=data.branch_id.astype(int).tolist()
fig,ax=plt.subplots(figsize=(7.15,4.15))
ys=np.arange(13)
ax.barh(ys,vals,height=.67,color=[ORANGE if n in zero else TEAL for n in ids])
for yi,v in zip(ys,vals):ax.text(v+1.3,yi,f'{v:.2f}',fontsize=8.2,va='center')
ax.set_yticks(ys,[str(n) for n in ids])
ax.set_xlim(0,108);ax.set_xlabel('Necessary-curtailment lower bound (MW)',fontsize=9.3,labelpad=7)
ax.set_ylabel('Physical circuit ID',fontsize=9.3)
ax.set_title('All 13 connected, cut-positive outages',loc='left',fontsize=10.6,color=NAVY,fontweight='bold',pad=16)
ax.grid(axis='x',color=LINE,lw=.7);ax.set_axisbelow(True)
for s in ['top','right','left']:ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(LINE);ax.tick_params(axis='y',length=0,pad=7)
ax.legend(handles=[Line2D([0],[0],color=ORANGE,lw=6,label='VELE unchanged'),Line2D([0],[0],color=TEAL,lw=6,label='VELE changed')],
          loc='upper left',frameon=False,fontsize=8.25,ncol=2,bbox_to_anchor=(0,-.13))
fig.tight_layout(pad=1.0)
fig.subplots_adjust(bottom=.22)
finish(fig,'Fig3_Thirteen_Independently_Certified_Cases',[cutfile])
# FIGURE 4: four source conditions, only two underlying topologies.
source=SOURCE/'PHASE18_CUT_BOUND_CASE_SUMMARY.csv'
c=pd.read_csv(source).set_index('condition').loc[['ieee57_typ','ieee57_api','ieee118_typ','ieee118_api']]
conn=c.cut_certified_positive_connected.to_numpy(int)
disc=(c.cut_certified_positive_all-c.cut_certified_positive_connected).to_numpy(int)
assert conn.tolist()==[0,0,0,13] and disc.tolist()==[1,1,5,4]
fig,ax=plt.subplots(figsize=(7.15,3.00))
ys=np.arange(4)
ax.barh(ys,conn,height=.53,color=ORANGE,label='Connected, positive bound')
ax.barh(ys,disc,left=conn,height=.53,color=TEAL,label='Disconnected, positive bound')
ax.set_yticks(ys,['IEEE57 typical','IEEE57 stressed','IEEE118 typical','IEEE118 stressed'])
ax.invert_yaxis();ax.set_xlim(0,20);ax.set_xticks([0,5,10,15])
ax.set_title('Positive necessary-curtailment certificates by operating state',loc='left',fontsize=10.4,color=NAVY,fontweight='bold',pad=13)
ax.set_xlabel('Physical outages with positive cut bounds (count)',labelpad=6,fontsize=9)
for yi,(a,b) in enumerate(zip(conn,disc)):ax.text(a+b+.33,yi,f'{a+b}',va='center',fontsize=9.0,fontweight='bold')
ax.grid(axis='x',color=LINE,lw=.7);ax.set_axisbelow(True)
for s in ['top','right','left']:ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(LINE);ax.tick_params(axis='y',length=0,pad=8)
ax.legend(loc='lower left',bbox_to_anchor=(0,-.38),ncol=2,frameon=False,fontsize=8.5)
fig.subplots_adjust(left=.235,right=.967,top=.86,bottom=.3)
finish(fig,'Fig4_Certificates_By_Operating_Condition',[source])
(OUT/'SOURCE_FIGURE_MANIFEST.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
print('FOUR_VECTOR_AND_340DPI_FIGURES_VALIDATED',json.dumps(audit,indent=2))
