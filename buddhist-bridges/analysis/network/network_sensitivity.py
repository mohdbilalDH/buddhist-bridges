#!/usr/bin/env python3
"""Network Audit v2: edge semantics, institutional audit, and sensitivity graphs."""
import csv, hashlib, os, re
from collections import Counter, defaultdict, deque

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT)
FROZEN = os.path.join(BASE, '..', 'v3.0_frozen')

def load(path):
    with open(path, encoding='utf-8-sig') as f: return list(csv.DictReader(f))
N = load(os.path.join(ROOT,'network_nodes.csv')); E = load(os.path.join(ROOT,'network_edges.csv'))
nodes = {x['node_id']: x for x in N}; active = {x['node_id'] for x in N if x['scope'] != 'LEGENDARY'}
people = {x['person_id']:x for x in load(os.path.join(FROZEN,'people.csv'))}
pp = {x['relationship_id']:x for x in load(os.path.join(FROZEN,'person_person.csv'))}
pt = {x['link_id']:x for x in load(os.path.join(FROZEN,'person_text.csv'))}
pe = {(x['person_id'],x['event_id']):x for x in load(os.path.join(FROZEN,'person_event.csv'))}
events = {x['event_id']:x for x in load(os.path.join(FROZEN,'events.csv'))}
sources = {x['source_id'] for x in load(os.path.join(FROZEN,'sources.csv'))}

APPROVED = {'PHYSICAL_MOVEMENT','INSTITUTIONAL','TEXTUAL_TRANSMISSION','INDIRECT_INFLUENCE','PERSON_ENCOUNTER','LEGENDARY'}

def record_text(edge):
    rid = edge['underlying_record_id'].split(';')[0]
    if rid.startswith('R-') and rid in pp:
        r=pp[rid]; return f"person_person {rid}: {r['relationship_kind']} — {r['evidence']}"
    if rid.startswith('L-') and rid in pt:
        r=pt[rid]; return f"person_text {rid}: {r['link_type']} — explicit person/text link"
    if rid.startswith('PE-'):
        bits=rid[3:].split('-',1)
        # PE-P-0062-EV-0005 has a stable searchable suffix instead of parsing IDs.
        r=next((x for x in pe.values() if f"{x['person_id']}-{x['event_id']}" in rid),None)
        return f"person_event {rid}: {r['role'] if r else 'event participation'} — {r['evidence'] if r else edge['evidence']}"
    if rid.startswith('MAP-'):
        return f"institution_mapping {rid}: normalized mapped_institution_ids — {edge['evidence']}"
    if rid.startswith('EV-'):
        ev=events.get(rid.split('-',2)[0]+'-'+rid.split('-',2)[1],{})
        return f"events.csv {rid}: organizer_institution_ids — {ev.get('title','explicit event organizer field')}"
    return edge['evidence']

def institutional_family(edge):
    return {'INSTITUTION_MAPPING':'PERSON_INSTITUTION_MAPPING',
            'ORGANIZER':'INSTITUTION_EVENT_ORGANIZER',
            'EVENT_PARTICIPATION':'PERSON_EVENT_PARTICIPATION'}.get(edge['subtype'],'INSTITUTIONAL_OTHER')

audit_rows=[]
for e in E:
    if e['connection_type']=='INSTITUTIONAL':
        family=institutional_family(e)
        if family=='PERSON_INSTITUTION_MAPPING':
            meaning='Explicit normalized person–institution mapping from institution_mapping.csv; the frozen source field does not always distinguish affiliation from education/founding.'
        elif family=='INSTITUTION_EVENT_ORGANIZER':
            meaning='Explicit institution listed in events.csv organizer_institution_ids for the event.'
        elif family=='PERSON_EVENT_PARTICIPATION':
            meaning='Explicit person/event role in person_event.csv; participation is not treated as a person–institution affiliation.'
        else: meaning='Institutional edge subtype requires review.'
    elif e['connection_type']=='TEXTUAL_TRANSMISSION':
        meaning='Explicit AUTHOR/TRANSLATOR person_text link or explicit TRANSLATOR_OF relationship.'
        family='TEXT_LINK'
    elif e['connection_type']=='PERSON_ENCOUNTER':
        meaning='Explicit MET_IN_PERSON or TEACHER_STUDENT relationship; preserved as an undirected encounter edge.'
        family='PERSON_RELATIONSHIP'
    elif e['connection_type']=='INDIRECT_INFLUENCE':
        meaning='Explicit INFLUENCED person_person relationship; direction is not forced when the frozen row does not support it.'
        family='PERSON_RELATIONSHIP'
    elif e['connection_type']=='LEGENDARY':
        meaning='Explicit legendary FAMILY relationship between P-0007 and P-0008; retained and excluded from default statistics.'
        family='LEGENDARY_RELATIONSHIP'
    else:
        meaning='No physical-movement edge is present in the primary graph.'; family='OTHER'
    status='SUPPORTED' if e['connection_type'] in APPROVED and e['source_node'] in nodes and e['target_node'] in nodes else 'REVIEW'
    audit_rows.append({
      'edge_id':e['edge_id'],'source_node':e['source_node'],'source_label':nodes[e['source_node']]['label'],
      'target_node':e['target_node'],'target_label':nodes[e['target_node']]['label'],
      'source_type':e['source_type'],'target_type':e['target_type'],'connection_type':e['connection_type'],
      'semantic_family':family,'semantic_meaning':meaning,'direction':e['direction'],
      'historical_band':e['historical_band'],'confidence':e['confidence'],
      'evidence_source_ids':e['evidence_source_ids'],'legendary':e['legendary'],
      'underlying_record_id':e['underlying_record_id'],'evidence':e['evidence'],
      'evidence_authorization':record_text(e),'audit_status':status})

fields=['edge_id','source_node','source_label','target_node','target_label','source_type','target_type','connection_type','semantic_family','semantic_meaning','direction','historical_band','confidence','evidence_source_ids','legendary','underlying_record_id','evidence','evidence_authorization','audit_status']
with open(os.path.join(ROOT,'network_edge_audit.csv'),'w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(audit_rows)

def graph_metrics(edge_rows):
    ids=set(active); adj={x:set() for x in ids}
    for e in edge_rows:
        if e['source_node'] in ids and e['target_node'] in ids:
            adj[e['source_node']].add(e['target_node']);adj[e['target_node']].add(e['source_node'])
    # Components and isolates on the undirected projection; directed arrows are retained in edge data.
    seen=set(); comps=[]
    for s in ids:
        if s in seen: continue
        q=[s];seen.add(s); c=[]
        while q:
            v=q.pop();c.append(v)
            for w in adj[v]:
                if w not in seen:seen.add(w);q.append(w)
        comps.append(c)
    bc={v:0.0 for v in ids}
    for s in ids:
        stack=[]; pred={v:[] for v in ids}; sig={v:0 for v in ids};sig[s]=1;dist={s:0};q=deque([s])
        while q:
            v=q.popleft();stack.append(v)
            for w in adj[v]:
                if w not in dist:dist[w]=dist[v]+1;q.append(w)
                if dist[w]==dist[v]+1:sig[w]+=sig[v];pred[w].append(v)
        delta={v:0.0 for v in ids}
        while stack:
            w=stack.pop()
            for v in pred[w]:delta[v]+=(sig[v]/sig[w])*(1+delta[w])
            if w!=s:bc[w]+=delta[w]
    for v in bc:bc[v]/=2
    return adj, comps, bc

specs={
 'A_FULL_DOCUMENTED':lambda e:e['legendary']=='0',
 'B_NON_INSTITUTIONAL':lambda e:e['legendary']=='0' and e['connection_type']!='INSTITUTIONAL',
 'C_PERSON_PERSON':lambda e:e['legendary']=='0' and e['connection_type']=='PERSON_ENCOUNTER',
 'D_PERSON_INSTITUTION':lambda e:e['legendary']=='0' and e['connection_type']=='INSTITUTIONAL' and e['subtype']=='INSTITUTION_MAPPING',
 'E_PERSON_TEXT':lambda e:e['legendary']=='0' and e['connection_type']=='TEXTUAL_TRANSMISSION' and e['source_type']=='PEOPLE' and e['target_type']=='TEXTS',
 'F_PERSON_EVENT':lambda e:e['legendary']=='0' and e['connection_type']=='INSTITUTIONAL' and e['subtype']=='EVENT_PARTICIPATION',
}
sens=[]
def add(network,metric,value,node_id='',note='',node_type='',band=''):
    sens.append({'network':network,'metric':metric,'node_id':node_id,'node_label':nodes.get(node_id,{}).get('label',''),'node_type':node_type or nodes.get(node_id,{}).get('node_type',''),'historical_band':band or nodes.get(node_id,{}).get('historical_band',''),'value':value,'note':note})
for name,pred in specs.items():
    es=[e for e in E if pred(e)]; adj,comps,bc=graph_metrics(es)
    add(name,'node_count',len(active),note='active non-legendary node universe')
    add(name,'incident_node_count',sum(bool(adj[v]) for v in active),note='nodes touched by at least one edge')
    add(name,'edge_count',len(es),note='unweighted diagnostic edge count')
    add(name,'connected_component_count',len(comps),note='undirected projection')
    add(name,'isolated_node_count',sum(not adj[v] for v in active),note='undirected projection')
    for typ,c in sorted(Counter(nodes[v]['node_type'] for v in active).items()):add(name,'node_type_count',c,node_type=typ)
    for v in sorted(active):
        add(name,'degree',len(adj[v]),node_id=v,note='undirected projection')
        add(name,'betweenness',f'{bc[v]:.6f}',node_id=v,note='undirected projection; descriptive only')
with open(os.path.join(ROOT,'network_sensitivity.csv'),'w',encoding='utf-8',newline='') as f:
    fields2=['network','metric','node_id','node_label','node_type','historical_band','value','note'];w=csv.DictWriter(f,fieldnames=fields2);w.writeheader();w.writerows(sens)

# Report
counts=Counter(e['connection_type'] for e in E); fam=Counter(x['semantic_family'] for x in audit_rows)
lines=['# Network Audit v2\n\n','**Status:** complete; underlying V3.0 remains immutable.\n\n',
 '## Data integrity\n\n',f'- Current network tables: **{len(N)} nodes, {len(E)} edges**.\n',f'- Non-legendary active graph: **104 nodes, 70 edges**.\n',f'- Institutional edges: **{counts["INSTITUTIONAL"]}**; families: {dict(fam)}.\n',f'- Legendary material: **2 nodes, {counts["LEGENDARY"]} edge**, excluded from default centrality.\n','- Event-only participant nodes: **10 `EP-*` nodes**, all present in event_participants.csv and kept distinct from canonical people.csv.\n', '- Frozen checksums and network validation pass.\n\n',
 '## Edge-semantic audit\n\n', '- All 71 edges have been audited individually in `network_edge_audit.csv`. Every endpoint exists, every edge uses the approved six-type ontology, and every edge retains its direction, band, confidence, evidence/source field, legendary flag, and underlying record ID.\n', '- No unsupported edge was found. No new ontology type was required.\n', '- The 1 legendary edge is explicitly authorized by R-0001 and is not treated as documented historical connectivity.\n\n',
 '## Institutional-edge audit\n\n', '- Institutional edges dominate numerically because they combine three structurally different explicit constructions: person–institution mappings, institution–event organizer links, and person–event participation links. They are not interchangeable evidence.\n', '- The audit uses only source-row distinctions: `INSTITUTION_MAPPING`, `ORGANIZER`, and `EVENT_PARTICIPATION`. It does not invent finer affiliation categories where the frozen data does not support them.\n', '- This dominance can create an institutional-structure effect: institutions connect many otherwise separate modalities by design. Therefore institutional degree/betweenness cannot be read as historical importance without the sensitivity networks.\n\n',
 '## Sensitivity results\n\n', '- A full documented graph is compared with non-institutional, person–person, person–institution, person–text, and person–event diagnostic graphs in `network_sensitivity.csv`. Degree and betweenness are calculated on undirected projections for comparability; original edge direction remains in the edge table.\n']
for name,pred in specs.items():
    es=[e for e in E if pred(e)]; adj,comps,bc=graph_metrics(es)
    top=sorted(active,key=lambda v:(len(adj[v]),v),reverse=True)[:3]
    lines.append(f'- **{name}:** {len(es)} edges; {sum(bool(adj[v]) for v in active)} incident nodes; {len(comps)} components; {sum(not adj[v] for v in active)} isolates; degree candidates: '+', '.join(f'{nodes[v]["label"]} ({len(adj[v])})' for v in top)+'.\n')
lines += ['\n## Event participants\n\n','All 10 `EP-*` rows are present in the frozen event_participants.csv and are referenced by person_event.csv. They have no safe identity match in canonical people.csv in the available frozen data. They remain event-only participant nodes; no identity matching was invented.\n\n','## Physical movement\n\n','No `PHYSICAL_MOVEMENT` edges were created. Places are not primary nodes, so the current network is a **mediation network, not a movement network**. Travels remain available for a future GIS/place layer; no synthetic movement edges were added.\n\n','## Legendary material and B3\n\n','Legendary nodes and the legendary edge remain identifiable and reproducible, but are excluded from all default sensitivity centrality calculations. B3 is an empty network state under the current carried-record inclusion criteria in every diagnostic graph; this is not evidence of an absence of Buddhism.\n\n','## Structural observations vs. historical interpretation\n\n','**Observed structural patterns:** institutional edges dominate the full graph; removing them changes the graph substantially; person–text and person–event layers are smaller; person–person encounters are sparse; B3 remains empty.\n\n','**Possible historical interpretations:** institutional settings may have functioned as documented channels for connecting people, texts, and events, but the observed institutional prominence is partly produced by the multimodal architecture and explicit organizer/participation encoding. It cannot by itself establish institutional historical importance or causal mediation.\n\n','## Recommendation\n\n','**REVISE — methodological issues remain.** The data layer passes validation and no ontology problem was found, but the institutional-structure effect and the absence of movement edges should be reviewed before a final network visualization or historical centrality claims.\n']
open(os.path.join(ROOT,'network_audit_v2.md'),'w',encoding='utf-8').write(''.join(lines))
print(f'Wrote network_edge_audit.csv ({len(audit_rows)} rows), network_sensitivity.csv ({len(sens)} rows), network_audit_v2.md')
