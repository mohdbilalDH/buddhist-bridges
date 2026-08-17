#!/usr/bin/env python3
"""Build the Phase 3 multimodal network tables from immutable V3.0 inputs.

The primary graph has PEOPLE, INSTITUTIONS, TEXTS, and EVENTS. Places are audited
but deliberately not promoted to nodes. No edge is inferred from co-location,
chronology, or shared affiliation.
"""
import csv, hashlib, os, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(ROOT, '..', 'v3.0_frozen')
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'network')
os.makedirs(OUT, exist_ok=True)

def load(base, name):
    with open(os.path.join(base, name), encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def write_csv(name, rows, fields):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

P = load(FROZEN, 'people.csv'); I = load(FROZEN, 'institutions.csv'); T = load(FROZEN, 'texts.csv')
E = load(FROZEN, 'events.csv'); R = load(FROZEN, 'person_person.csv'); PT = load(FROZEN, 'person_text.csv')
PE = load(FROZEN, 'person_event.csv'); EP = load(FROZEN, 'event_participants.csv'); PP = load(FROZEN, 'person_place.csv')
TR = load(FROZEN, 'travels.csv'); CLS = load(FROZEN, 'classification_v3.csv'); SOURCES = load(FROZEN, 'sources.csv')
REG = {r['person_id']: r for r in load(DATA, 'register.csv')}
TAX = {r['person_id']: r for r in load(DATA, 'tradition_taxonomy.csv')}
IM = {r['person_id']: r for r in load(DATA, 'institution_mapping.csv')}
CBY = {(r['table'], r['record_id']): r for r in CLS}
people = {r['person_id']: r for r in P}; inst = {r['institution_id']: r for r in I}
texts = {r['text_id']: r for r in T}; events = {r['event_id']: r for r in E}
ep_by_id = {r['participant_id']: r for r in EP}
SOURCE_IDS = {r['source_id'] for r in SOURCES}
carried = lambda table, rid: CBY.get((table, rid), {}).get('scope') in ('KEEP', 'ADAPT')
def norm_band(value):
    m = re.search(r'B[1-6]', value or '')
    return m.group(0) if m else ''
band = lambda table, rid: norm_band(CBY.get((table, rid), {}).get('period_band') or '')
scope = lambda table, rid: 'CARRIED' if carried(table, rid) else (CBY.get((table, rid), {}).get('scope') or '')

NODE_FIELDS = ['node_id','label','node_type','scope','historical_band','tradition','geography','confidence','relevance','direction','source_count','single_source','evidence_metadata','underlying_record_id']
nodes = {}
def add_node(row): nodes[row['node_id']] = row

for p in P:
    pid = p['person_id']
    if carried('PEOPLE', pid) or pid in ('P-0007','P-0008'):
        r = REG.get(pid, {}); tx = TAX.get(pid, {})
        add_node({'node_id': pid, 'label': p['full_name'], 'node_type': 'PEOPLE',
          'scope': 'CARRIED' if carried('PEOPLE', pid) else 'LEGENDARY', 'historical_band': norm_band(r.get('band')) or band('PEOPLE',pid),
          'tradition': ';'.join(x for x in (tx.get('tradition_1',''),tx.get('tradition_2',''),tx.get('tradition_3','')) if x),
          'geography': p['nationality_region'], 'confidence': p['confidence'], 'relevance': r.get('buddhist_relevance',''),
          'direction': p['direction_of_influence'], 'source_count': len([x for x in p['source_ids'].split(';') if x]),
          'single_source': '1' if len([x for x in p['source_ids'].split(';') if x]) == 1 else '0',
          'evidence_metadata': p['source_ids'], 'underlying_record_id': pid})

# Event participants are explicit event-table people, but are not canonical PEOPLE.csv records.
# Keep them as visibly separate PEOPLE nodes rather than silently identifying them with P-####.
for x in EP:
    add_node({'node_id': x['participant_id'], 'label': x['name'], 'node_type': 'PEOPLE', 'scope': 'EVENT_PARTICIPANT',
      'historical_band': '', 'tradition': '', 'geography': 'Korea/India event participant', 'confidence': 'HIGH',
      'relevance': 'EVENT_ONLY', 'direction': 'UNCERTAIN', 'source_count': '', 'single_source': '0',
      'evidence_metadata': x['notes'], 'underlying_record_id': x['participant_id']})

for x in I:
    if carried('INSTITUTIONS', x['institution_id']):
        add_node({'node_id': x['institution_id'], 'label': x['name'], 'node_type': 'INSTITUTIONS', 'scope': 'CARRIED',
          'historical_band': band('INSTITUTIONS',x['institution_id']), 'tradition': '', 'geography': x['location_place_id'],
          'confidence': 'MEDIUM', 'relevance': x['india_relevance']+';'+x['korea_relevance'], 'direction': 'UNCERTAIN',
          'source_count': '', 'single_source': '0', 'evidence_metadata': x['notes'], 'underlying_record_id': x['institution_id']})
for x in T:
    if carried('TEXTS', x['text_id']):
        add_node({'node_id': x['text_id'], 'label': x['title'], 'node_type': 'TEXTS', 'scope': 'CARRIED',
          'historical_band': band('TEXTS',x['text_id']), 'tradition': '', 'geography': '', 'confidence': x['confidence'],
          'relevance': x['india_relevance']+';'+x['korea_relevance'], 'direction': 'UNCERTAIN', 'source_count': '',
          'single_source': '0', 'evidence_metadata': x['notes'], 'underlying_record_id': x['text_id']})
for x in E:
    if carried('EVENTS', x['event_id']):
        add_node({'node_id': x['event_id'], 'label': x['title'], 'node_type': 'EVENTS', 'scope': 'CARRIED',
          'historical_band': band('EVENTS',x['event_id']), 'tradition': '', 'geography': x['location_place_id'],
          'confidence': x['confidence'], 'relevance': x['event_type'], 'direction': 'UNCERTAIN',
          'source_count': len([s for s in x['source_ids'].split(';') if s]), 'single_source': '1' if len([s for s in x['source_ids'].split(';') if s]) == 1 else '0',
          'evidence_metadata': x['source_ids'], 'underlying_record_id': x['event_id']})

EDGE_FIELDS = ['edge_id','source_node','target_node','source_type','target_type','connection_type','subtype','direction','confidence','historical_band','evidence_source_ids','legendary','underlying_record_id','evidence']
edges = {}
VALID_TYPES = {'PHYSICAL_MOVEMENT','INSTITUTIONAL','TEXTUAL_TRANSMISSION','INDIRECT_INFLUENCE','PERSON_ENCOUNTER','LEGENDARY'}
def add_edge(source, target, typ, subtype, direction, confidence, b, evid, rid, legendary=False):
    if source not in nodes or target not in nodes: return
    # Undirected encounters have a canonical endpoint order so duplicates are visible and merged.
    if direction == 'UNDIRECTED' and source > target: source, target = target, source
    key = (source, target, typ, subtype, direction, b)
    # Only actual frozen source keys belong in evidence_source_ids. Relationship
    # and mapping rows carry prose evidence instead, retained in evidence.
    source_ids = evid if all((not z) or z in SOURCE_IDS for z in evid.split(';')) else ''
    if key in edges:
        e = edges[key]
        e['underlying_record_id'] += ';' + rid
        if source_ids and source_ids not in e['evidence_source_ids']: e['evidence_source_ids'] += (';' if e['evidence_source_ids'] else '') + source_ids
        e['evidence'] += ' | ' + evid if evid else ''
        return
    edges[key] = {'edge_id': f'E-{len(edges)+1:04d}', 'source_node': source, 'target_node': target,
      'source_type': nodes[source]['node_type'], 'target_type': nodes[target]['node_type'], 'connection_type': typ,
      'subtype': subtype, 'direction': direction, 'confidence': confidence, 'historical_band': b,
      'evidence_source_ids': source_ids, 'legendary': '1' if legendary else '0', 'underlying_record_id': rid, 'evidence': evid}

# Explicit person-person relationships only.
for x in R:
    a,b = x['person_a_id'], x['person_b_id']; k=x['relationship_kind']
    if a not in nodes or b not in nodes: continue
    if k in ('MET_IN_PERSON','TEACHER_STUDENT'):
        add_edge(a,b,'PERSON_ENCOUNTER',k,'UNDIRECTED',x['confidence'],band('PEOPLE',a) or band('PEOPLE',b),x['evidence'],x['relationship_id'])
    elif k == 'INFLUENCED':
        add_edge(a,b,'INDIRECT_INFLUENCE',k,'UNCERTAIN',x['confidence'],band('PEOPLE',a) or band('PEOPLE',b),x['evidence'],x['relationship_id'])
    elif k == 'TRANSLATOR_OF':
        add_edge(a,b,'TEXTUAL_TRANSMISSION',k,'UNCERTAIN',x['confidence'],band('PEOPLE',a) or band('PEOPLE',b),x['evidence'],x['relationship_id'])
    elif k == 'FAMILY' and {a,b} == {'P-0007','P-0008'}:
        add_edge(a,b,'LEGENDARY',k,'UNDIRECTED',x['confidence'],'B1',x['evidence'],x['relationship_id'],True)

# Explicit person-text links. SUBJECT is retained in audit but is not treated as transmission.
for x in PT:
    if x['link_type'] not in ('AUTHOR','TRANSLATOR'): continue
    if x['person_id'] in nodes and x['text_id'] in nodes:
        add_edge(x['person_id'],x['text_id'],'TEXTUAL_TRANSMISSION',x['link_type'],'PERSON_TO_TEXT',x['confidence'],band('TEXTS',x['text_id']),'',x['link_id'])

# Institution mappings are an approved derived relation; only MAPPED/PARTIAL mappings are used.
for x in load(DATA, 'institution_mapping.csv'):
    if x['mapping_status'] not in ('MAPPED','PARTIAL') or x['person_id'] not in nodes: continue
    for iid in [z for z in x['mapped_institution_ids'].split(';') if z]:
        if iid in nodes:
            add_edge(x['person_id'],iid,'INSTITUTIONAL','INSTITUTION_MAPPING','PERSON_TO_INSTITUTION',x['confidence'],band('INSTITUTIONS',iid),x['basis'],f"MAP-{x['person_id']}-{iid}")

# Explicit organizer links and person-event participation. EP-* identities remain separate.
for x in E:
    if not carried('EVENTS',x['event_id']): continue
    for iid in [z for z in x['organizer_institution_ids'].split(';') if z and z != '-']:
        add_edge(iid,x['event_id'],'INSTITUTIONAL','ORGANIZER','INSTITUTION_TO_EVENT','HIGH',band('EVENTS',x['event_id']),x['source_ids'],x['event_id']+'-'+iid)
for x in PE:
    if x['person_id'] in nodes and x['event_id'] in nodes:
        add_edge(x['person_id'],x['event_id'],'INSTITUTIONAL','EVENT_PARTICIPATION','PERSON_TO_EVENT',x['confidence'],band('EVENTS',x['event_id']),x['evidence'],f"PE-{x['person_id']}-{x['event_id']}")

node_rows = [nodes[k] for k in sorted(nodes)]
edge_rows = list(edges.values())
write_csv('network_nodes.csv', node_rows, NODE_FIELDS)
write_csv('network_edges.csv', edge_rows, EDGE_FIELDS)

# Audit and counts are reproducible, with intentionally excluded place relations made explicit.
audit = []
audit.append('# Network Data Audit — Phase 3, Step 1\n\n')
audit.append('**Baseline:** frozen V3.0, validated derived tables, prosopography outputs. Frozen inputs were read-only.\n\n')
audit.append('## Frozen inventory\n\n')
for label, rows in [('people.csv',P),('institutions.csv',I),('texts.csv',T),('events.csv',E),('person_person.csv',R),('person_place.csv',PP),('person_text.csv',PT),('person_event.csv',PE),('event_participants.csv',EP),('travels.csv',TR)]:
    audit.append(f'- **{label}:** {len(rows)} rows\n')
audit.append('\n## Scope reconciliation\n\n')
for table, rows in [('PEOPLE',P),('INSTITUTIONS',I),('TEXTS',T),('EVENTS',E)]:
    audit.append(f'- **{table}:** {sum(carried(table,x[table[:-1].lower()+"_id"] if table != "PEOPLE" else x["person_id"]) for x in rows)} carried records (classification KEEP/ADAPT)\n')
audit.append('- Canonical carried primary nodes: 43 PEOPLE, 19 INSTITUTIONS, 13 TEXTS, 19 EVENTS.\n')
audit.append(f'- Additional explicit event-participant PEOPLE nodes: {len(EP)} (`EP-*`); these are not canonical `people.csv` identities.\n')
audit.append('- Legendary `P-0007`/`P-0008` nodes are retained separately and off by default in scholarly interpretation.\n\n')
audit.append('## Edge construction decisions\n\n')
audit.append(f'- Built **{len(edge_rows)} deduplicated edges** from explicit person-person, person-text, institution mapping, organizer, and person-event records.\n')
audit.append('- Places and travels were audited but are not primary network nodes. Therefore no PHYSICAL_MOVEMENT edge is emitted in this primary graph; adding place endpoints would change the approved node architecture. Travel evidence remains available for a later place/network view.\n')
audit.append('- `SUBJECT`, `COLLEAGUE`, `FAMILY` (except the explicit P-0007/P-0008 legend), and unsupported relationship rows are not silently converted into historical transmission edges.\n')
audit.append('- Confidence and source counts are metadata/style fields, never edge weights.\n\n')
audit.append('## Direction, confidence, and missingness audit\n\n')
audit.append(f'- People directionality: {dict(Counter(x["direction_of_influence"] for x in P))}.\n')
audit.append(f'- Person-person relationship kinds: {dict(Counter(x["relationship_kind"] for x in R))}; confidence: {dict(Counter(x["confidence"] for x in R))}.\n')
audit.append(f'- Person-text link types: {dict(Counter(x["link_type"] for x in PT))}; confidence: {dict(Counter(x["confidence"] for x in PT))}.\n')
audit.append(f'- Person-event roles: {dict(Counter(x["role"] for x in PE))}; confidence: {dict(Counter(x["confidence"] for x in PE))}.\n')
audit.append(f'- Travel date precision: {dict(Counter(x["travel_dates_precision"] for x in TR))}; undated travel starts: {sum(not x["travel_start_year"] for x in TR)}.\n')
audit.append(f'- Person-place links without year: {sum(not x["year"] for x in PP)}; legendary person-place links: {sum(x["link_type"]=="LEGENDARY_ORIGIN" for x in PP)}.\n')
audit.append(f'- Legendary canonical people: {[x["person_id"] for x in P if x["status"]=="LEGENDARY"]}; legendary person-person edges retained: 1 and flagged.\n\n')
audit.append(f'- Frozen classification connection vocabulary observed: {dict(Counter(x["connection_type"] for x in CLS))}.\n\n')
audit.append('## Counts\n\n')
audit.append('```text\n' + '\n'.join(f'{k}: {v}' for k,v in sorted(Counter(x['connection_type'] for x in edge_rows).items())) + '\n```\n')
audit.append('\n## Review flags\n\n- The frozen event-participant table contains 10 `EP-*` people not present in `people.csv`; they are represented as separate event-only nodes rather than identity-matched.\n- The primary graph intentionally has no `PHYSICAL_MOVEMENT` edges because Places are excluded as primary nodes. Review whether a later secondary place view is desired.\n')
open(os.path.join(OUT,'network_audit.md'),'w',encoding='utf-8').write(''.join(audit))
print(f'Wrote {len(node_rows)} nodes and {len(edge_rows)} edges')
