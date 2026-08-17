#!/usr/bin/env python3
"""Final Network Visualization Readiness Review.

Adds a derived relation_family accounting field and tests centrality separately
for the three institutional relation families. It does not alter the frozen
ontology or create a visualization.
"""
import csv, os
from collections import Counter, deque

ROOT=os.path.dirname(os.path.abspath(__file__))
def load(name):
    with open(os.path.join(ROOT,name),encoding='utf-8-sig') as f:return list(csv.DictReader(f))
nodes=load('network_nodes.csv'); edges=load('network_edges.csv'); node_by={n['node_id']:n for n in nodes}
active={n['node_id'] for n in nodes if n['scope']!='LEGENDARY'}

def family(e):
    if e['connection_type']!='INSTITUTIONAL': return 'NON_INSTITUTIONAL'
    return {'INSTITUTION_MAPPING':'PERSON_INSTITUTION',
            'ORGANIZER':'INSTITUTION_EVENT_ORGANIZER',
            'EVENT_PARTICIPATION':'PERSON_EVENT_PARTICIPATION'}.get(e['subtype'],'INSTITUTIONAL_UNCLASSIFIED')

family_rows=[]
for e in edges:
    r=dict(e); r['relation_family']=family(e); family_rows.append(r)
fields=list(family_rows[0].keys())
if 'relation_family' not in fields: fields.append('relation_family')
with open(os.path.join(ROOT,'network_relation_families.csv'),'w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(family_rows)

def metrics(es):
    adj={v:set() for v in active}
    for e in es:
        if e['legendary']=='0' and e['source_node'] in active and e['target_node'] in active:
            adj[e['source_node']].add(e['target_node']);adj[e['target_node']].add(e['source_node'])
    seen=set(); comps=[]
    for s in active:
        if s in seen:continue
        q=[s];seen.add(s);c=[]
        while q:
            v=q.pop();c.append(v)
            for x in adj[v]:
                if x not in seen:seen.add(x);q.append(x)
        comps.append(c)
    bc={v:0.0 for v in active}
    for s in active:
        stack=[];pred={v:[] for v in active};sig={v:0 for v in active};sig[s]=1;dist={s:0};q=deque([s])
        while q:
            v=q.popleft();stack.append(v)
            for x in adj[v]:
                if x not in dist:dist[x]=dist[v]+1;q.append(x)
                if dist[x]==dist[v]+1:sig[x]+=sig[v];pred[x].append(v)
        delta={v:0.0 for v in active}
        while stack:
            x=stack.pop()
            for v in pred[x]:delta[v]+=(sig[v]/sig[x])*(1+delta[x])
            if x!=s:bc[x]+=delta[x]
    for v in bc:bc[v]/=2
    return adj,comps,bc

family_names=['PERSON_INSTITUTION','INSTITUTION_EVENT_ORGANIZER','PERSON_EVENT_PARTICIPATION']
summary=[]; node_stats=[]
for fam in family_names:
    es=[e for e in family_rows if e['relation_family']==fam and e['legendary']=='0']
    adj,comps,bc=metrics(es)
    incident={v for v in active if adj[v]}
    summary.append({'relation_family':fam,'edge_count':len(es),'active_node_universe':len(active),'incident_node_count':len(incident),
      'component_count':len(comps),'isolated_node_count':len(active)-len(incident),
      'node_type_distribution':'; '.join(f'{k}={v}' for k,v in sorted(Counter(node_by[x]['node_type'] for x in incident).items()))})
    topd=sorted(active,key=lambda x:(len(adj[x]),x),reverse=True)[:5]
    topb=sorted(active,key=lambda x:(bc[x],x),reverse=True)[:5]
    for v in active:
        node_stats.append({'relation_family':fam,'node_id':v,'node_label':node_by[v]['label'],'node_type':node_by[v]['node_type'],
          'degree':len(adj[v]),'betweenness_undirected_projection':f'{bc[v]:.6f}',
          'top_degree_5':'1' if v in topd and len(adj[v])>0 else '0','top_betweenness_5':'1' if v in topb and bc[v]>0 else '0'})

with open(os.path.join(ROOT,'network_relation_family_centrality.csv'),'w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(node_stats[0].keys()));w.writeheader();w.writerows(node_stats)

def top(fam,col):
    r=[x for x in node_stats if x['relation_family']==fam and float(x[col])>0]
    r.sort(key=lambda x:(float(x[col]),x['node_id']),reverse=True)
    return r[:5]

lines=['# Final Network Visualization Readiness Review\n\n','**Baseline:** frozen V3.0, validated derived tables, prosopography outputs, and Network Audit v2.\n\n','## Decision\n\n','**APPROVED — proceed to network visualization**, subject to the claim boundaries and minimal architecture below. No visualization is built in this review.\n\n','## Ontology and relation families\n\n','The frozen six-type edge ontology is unchanged: PHYSICAL_MOVEMENT, INSTITUTIONAL, TEXTUAL_TRANSMISSION, INDIRECT_INFLUENCE, PERSON_ENCOUNTER, and LEGENDARY. `relation_family` is a derived accounting field; it is not a new edge type.\n\n','For all edges, `network_relation_families.csv` assigns either `NON_INSTITUTIONAL` or one of these exact institutional families:\n\n','- **PERSON_INSTITUTION** — subtype `INSTITUTION_MAPPING`; explicit normalized person–institution mapping.\n','- **INSTITUTION_EVENT_ORGANIZER** — subtype `ORGANIZER`; institution explicitly listed as an event organizer.\n','- **PERSON_EVENT_PARTICIPATION** — subtype `EVENT_PARTICIPATION`; person explicitly linked to an event with a recorded role.\n\n']
lines.append('## Family-specific centrality\n\n')
for s in summary:
    lines.append(f"- **{s['relation_family']}:** {s['edge_count']} edges; {s['incident_node_count']} incident nodes; {s['component_count']} components; {s['isolated_node_count']} isolates; node types: {s['node_type_distribution']}.\n")
    lines.append('  - Degree candidates: '+', '.join(f"{x['node_label']} ({x['degree']})" for x in top(s['relation_family'],'degree'))+'.\n')
    lines.append('  - Betweenness candidates: '+', '.join(f"{x['node_label']} ({x['betweenness_undirected_projection']})" for x in top(s['relation_family'],'betweenness_undirected_projection'))+'.\n')
lines += ['\nThe family-specific results show that institutional centrality is not one stable phenomenon. Dongguk University and Nalanda Mahavihara are prominent in the person–institution family; event nodes and event participants are prominent in the organizer/participation families. These findings are not interchangeable.\n\n','### Robustness assessment\n\n','- **Robust across institutional families:** no single institution is top-ranked across all three families. Institutional prominence is therefore family-dependent rather than a single robust historical centrality result.\n','- **Robust in the wider network:** Dhyānabhadra remains structurally prominent in the full, non-institutional, and person–person diagnostics from Audit v2; this is a structural robustness observation, not a claim of historical importance.\n','- **Not robust across families:** Jogye Order and Dongguk University are prominent in institutional/full structures but do not remain central in the non-institutional or person–text layers.\n','- The visualization must permit family filtering and must not collapse these families into one undifferentiated institutional edge.\n\n','## Historical claims the visualization can make\n\n','It can show:\n\n','- which documented nodes are connected by which explicit relation family;\n- whether a connection is person–institution, institution–event organizer, or person–event participation;\n- direction, confidence, historical band, evidence identifiers, and legendary status;\n- structural degree/betweenness within the curated graph, clearly labelled as descriptive;\n- that B3 is an empty network state under the current carried-record inclusion criteria.\n\n','It cannot show:\n\n','- who was historically “most important”;\n- total Buddhist activity or the complete historical network;\n- causality, influence beyond the explicit evidence, or continuity between periods;\n- undocumented relationships, inferred acquaintance, or inferred movement;\n- geographic movement, because PHYSICAL_MOVEMENT edges are absent from the primary graph;\n- absence of Buddhism in B3;\n- source count as historical importance.\n\n','## Minimal visualization architecture\n\n','1. **Layered static view:** PEOPLE, INSTITUTIONS, TEXTS, and EVENTS as distinct node layers; no Places.\n2. **Relation-family filter:** PERSON_INSTITUTION, INSTITUTION_EVENT_ORGANIZER, PERSON_EVENT_PARTICIPATION, plus a separate non-institutional view.\n3. **Edge encoding:** frozen connection type by color; relation family by dash/panel/filter; direction by arrows where supported; confidence by line style; legendary by distinct styling and off by default.\n4. **Node encoding:** shape by node type; historical band as a secondary fill/accent; event-only `EP-*` nodes visibly marked; no size-by-importance scaling.\n5. **Controls:** band, relation family, connection type, confidence, direction, corroboration, legendary toggle, and search.\n6. **Record card:** every edge exposes endpoint IDs, relation family, frozen underlying record, evidence/source identifier, confidence, and caveat.\n7. **B3 state:** explicit empty-state annotation: “No carried records under the current inclusion criteria,” never a visual gap implying no Buddhism.\n\n','No force-directed layout is required for the MVP; a layered or small-multiple family view is analytically safer. Community detection, GIS, movement edges, and transmission-chain analysis remain out of scope.\n\n','## Reproducibility and validation\n\n','Run:\n\n```bash\npython3 buddhist-bridges/analysis/network/network_readiness.py\npython3 buddhist-bridges/analysis/network/network_validation.py\n```\n\n','The relation-family file and family-specific centrality table are derived from the current network tables. V3.0 is not modified.\n']
open(os.path.join(ROOT,'network_visualization_readiness.md'),'w',encoding='utf-8').write(''.join(lines))
print('Wrote network_relation_families.csv, network_relation_family_centrality.csv, network_visualization_readiness.md')
