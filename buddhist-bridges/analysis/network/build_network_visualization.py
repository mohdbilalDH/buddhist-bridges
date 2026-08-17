#!/usr/bin/env python3
"""Build the self-contained Network Visualization MVP from current derived tables."""
import csv, json, os

ROOT=os.path.dirname(os.path.abspath(__file__))
def load(name):
    with open(os.path.join(ROOT,name),encoding='utf-8-sig') as f:return list(csv.DictReader(f))
nodes=load('network_nodes.csv'); edges=load('network_relation_families.csv')
centrality=load('network_relation_family_centrality.csv')
metrics={}
for r in centrality:
    if r['node_id']:
        metrics.setdefault(r['node_id'],{})[r['relation_family']]={'degree':r['degree'],'betweenness':r['betweenness_undirected_projection']}
for n in nodes: n['centrality']=metrics.get(n['node_id'],{})
payload={'meta':{'title':'Buddhist Bridges — Documented Mediation Network MVP','baseline':'frozen V3.0','node_count':len(nodes),'edge_count':len(edges),'note':'Structural visualization of documented mediation; not a ranking of historical importance.'},'nodes':nodes,'edges':edges}
with open(os.path.join(ROOT,'network_mvp_template.html'),encoding='utf-8') as f: html=f.read()
html=html.replace('/*__NETWORK_DATA__*/',json.dumps(payload,ensure_ascii=False,separators=(',',':')))
with open(os.path.join(ROOT,'network_mvp.html'),'w',encoding='utf-8') as f:f.write(html)
print(f'Wrote network_mvp.html ({len(nodes)} nodes, {len(edges)} edges)')
