#!/usr/bin/env python3
"""Produce descriptive, unweighted network statistics and findings."""
import csv, os
from collections import Counter, defaultdict, deque

ROOT = os.path.dirname(os.path.abspath(__file__))
def load(name):
    with open(os.path.join(ROOT,name),encoding='utf-8-sig') as f:return list(csv.DictReader(f))
N,E=load('network_nodes.csv'),load('network_edges.csv'); nodes={n['node_id']:n for n in N}
active=[n for n in N if n['scope']!='LEGENDARY']; active_ids={n['node_id'] for n in active}
edges=[e for e in E if e['legendary']=='0' and e['source_node'] in active_ids and e['target_node'] in active_ids]
adj={x:set() for x in active_ids}
for e in edges: adj[e['source_node']].add(e['target_node']); adj[e['target_node']].add(e['source_node'])

# Brandes betweenness on the undirected projection, explicitly labelled as such.
bc={v:0.0 for v in active_ids}
for s in active_ids:
    stack=[]; pred={v:[] for v in active_ids}; sigma={v:0 for v in active_ids}; sigma[s]=1
    dist={s:0}; q=deque([s])
    while q:
        v=q.popleft(); stack.append(v)
        for w in adj[v]:
            if w not in dist: dist[w]=dist[v]+1; q.append(w)
            if dist[w]==dist[v]+1: sigma[w]+=sigma[v]; pred[w].append(v)
    delta={v:0.0 for v in active_ids}
    while stack:
        w=stack.pop()
        for v in pred[w]: delta[v]+=(sigma[v]/sigma[w])*(1+delta[w])
        if w!=s: bc[w]+=delta[w]
for v in bc: bc[v]/=2

rows=[]
def stat(metric,value,scope='ALL',node_type='',band='',note='',node_id=''):
    rows.append({'metric':metric,'value':value,'scope':scope,'node_type':node_type,'historical_band':band,'node_id':node_id,'note':note})
stat('node_count',len(active),'ALL',note='canonical + event-participant nodes; legendary excluded')
stat('edge_count',len(edges),'ALL',note='unweighted, non-legendary primary graph')
stat('isolated_node_count',sum(not adj[v] for v in active_ids),'ALL',note='no explicit primary-network edge')
for typ,c in sorted(Counter(n['node_type'] for n in active).items()): stat('node_type_count',c,'ALL',typ)
for typ,c in sorted(Counter(e['connection_type'] for e in edges).items()): stat('edge_type_count',c,'ALL',note=typ)
for direction,c in sorted(Counter(e['direction'] for e in edges).items()): stat('direction_count',c,'ALL',note=direction)
for b in ['B1','B2','B3','B4','B5','B6']:
    ns=[n for n in active if n['historical_band']==b]; es=[e for e in edges if e['historical_band']==b]
    stat('node_count',len(ns),'BAND',band=b); stat('edge_count',len(es),'BAND',band=b)
for v in sorted(active_ids):
    stat('degree',len(adj[v]),'NODE',nodes[v]['node_type'],nodes[v].get('historical_band',''),node_id=v)
    stat('betweenness_undirected_projection',f'{bc[v]:.6f}','NODE',nodes[v]['node_type'],nodes[v].get('historical_band',''),node_id=v)
with open(os.path.join(ROOT,'network_statistics.csv'),'w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['metric','value','scope','node_type','historical_band','node_id','note']);w.writeheader();w.writerows(rows)

topdeg=sorted(active_ids,key=lambda x:(len(adj[x]),x),reverse=True)[:10]
topbc=sorted(active_ids,key=lambda x:(bc[x],x),reverse=True)[:10]
lines=['# Network Findings v1 — Descriptive Initial Analysis\n\n',
 '**Scope:** static, unweighted primary multimodal graph; legendary nodes/edges excluded by default. These are descriptive observations, not importance rankings.\n\n',
 f'- The graph contains **{len(active)} active nodes** and **{len(edges)} explicit edges**.\n',
 f'- Isolated active nodes: **{sum(not adj[v] for v in active_ids)}**. Isolation means no edge in this primary architecture, not historical irrelevance.\n',
 f'- Edge types: {dict(Counter(e["connection_type"] for e in edges))}.\n',
 f'- Direction labels: {dict(Counter(e["direction"] for e in edges))}; undirected encounters remain undirected.\n\n',
 '## Mediation observations\n\n',
 '- Institutional edges are the largest explicit edge class in this graph, while textual transmission and person encounters form smaller typed layers. This is a property of the curated edge construction, not a claim that institutions were historically more important.\n',
 '- The primary graph does not include PHYSICAL_MOVEMENT edges because Places are excluded as primary nodes. Travel is therefore not silently converted into person-person or person-event ties.\n',
 '- Degree and betweenness are reported as structural descriptors. A high value identifies a bridge candidate for qualitative review, not an importance ranking.\n\n',
 '## Highest structural values (review candidates, not rankings)\n\n',
 'Degree projection: ' + ', '.join(f'{nodes[x]["label"]} ({len(adj[x])})' for x in topdeg[:5]) + '\n\n',
 'Betweenness in undirected projection: ' + ', '.join(f'{nodes[x]["label"]} ({bc[x]:.3f})' for x in topbc[:5]) + '\n\n',
 '## Period caution\n\n',
 '- B3 is retained as an empty network state because there are no carried records under the current inclusion criteria. This must not be interpreted as an absence of Buddhism.\n',
 '- Band counts should not be read as continuous connectivity or compared without the source-density and inclusion-criteria context established by the Timeline and prosopography reports.\n',
 '- Community detection was not run; the approved design warns that it would overfit this small heterogeneous graph.\n\n',
 '## Key question status\n\n',
 'The data layer supports comparing direct person encounters with institutional, textual, and event-mediated edges. It does not yet establish which mechanism dominated historically; that requires band-aware, source-aware interpretation and review of the explicit edges.\n']
open(os.path.join(ROOT,'network_findings_v1.md'),'w',encoding='utf-8').write(''.join(lines))
print(f'Wrote network_statistics.csv ({len(rows)} rows) and network_findings_v1.md')
