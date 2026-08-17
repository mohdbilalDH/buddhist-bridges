#!/usr/bin/env python3
"""Validate Phase 3 network tables and frozen-baseline integrity."""
import csv, hashlib, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(ROOT)
FROZEN = os.path.join(BASE, '..', 'v3.0_frozen')
errors = []
def load(name):
    with open(os.path.join(ROOT, name), encoding='utf-8-sig') as f: return list(csv.DictReader(f))
def check(ok, msg):
    if not ok: errors.append(msg)

nodes, edges = load('network_nodes.csv'), load('network_edges.csv')
node_ids = {n['node_id'] for n in nodes}
valid_types = {'PHYSICAL_MOVEMENT','INSTITUTIONAL','TEXTUAL_TRANSMISSION','INDIRECT_INFLUENCE','PERSON_ENCOUNTER','LEGENDARY'}
valid_directions = {'INDIA_TO_KOREA','KOREA_TO_INDIA','BIDIRECTIONAL','UNCERTAIN','UNDIRECTED','PERSON_TO_TEXT','PERSON_TO_INSTITUTION','INSTITUTION_TO_EVENT','PERSON_TO_EVENT'}
check(len(node_ids) == len(nodes), 'duplicate node IDs')
check(all(e['source_node'] in node_ids and e['target_node'] in node_ids for e in edges), 'orphaned edge endpoint')
check(all(e['connection_type'] in valid_types for e in edges), 'unapproved connection type')
check(not any(e['connection_type']=='PHYSICAL_MOVEMENT' for e in edges), 'unexpected PHYSICAL_MOVEMENT edge in primary graph')
check(all(e['direction'] in valid_directions for e in edges), 'invalid direction value')
check(all(e['legendary'] in ('0','1') for e in edges), 'invalid legendary flag')
check(all(n['scope'] in ('CARRIED','EVENT_PARTICIPANT','LEGENDARY') for n in nodes), 'invalid node scope')
check(all(e['source_type'] == next(n['node_type'] for n in nodes if n['node_id']==e['source_node']) for e in edges), 'source type mismatch')
check(all(e['target_type'] == next(n['node_type'] for n in nodes if n['node_id']==e['target_node']) for e in edges), 'target type mismatch')

keys = [(e['source_node'],e['target_node'],e['connection_type'],e['subtype'],e['direction'],e['historical_band']) for e in edges]
check(len(keys) == len(set(keys)), 'duplicated edge key')
for e in edges:
    if e['evidence_source_ids']:
        # Source keys are validated against the immutable source registry.
        sources = {r['source_id'] for r in csv.DictReader(open(os.path.join(FROZEN,'sources.csv'),encoding='utf-8-sig'))}
        check(all(x in sources for x in e['evidence_source_ids'].split(';')), f"unreconciled source ID in {e['edge_id']}")

cls = list(csv.DictReader(open(os.path.join(FROZEN,'classification_v3.csv'),encoding='utf-8-sig')))
for table, typ, expected in [('PEOPLE','PEOPLE',43),('INSTITUTIONS','INSTITUTIONS',19),('TEXTS','TEXTS',13),('EVENTS','EVENTS',19)]:
    actual = sum(n['node_type']==typ and n['scope']=='CARRIED' for n in nodes)
    check(actual == expected, f'{typ} carried count {actual}, expected {expected}')
check(sum(n['scope']=='EVENT_PARTICIPANT' for n in nodes) == 10, 'event participant count mismatch')
check(sum(n['scope']=='LEGENDARY' for n in nodes) == 2, 'legendary node count mismatch')
check(sum(e['connection_type']=='LEGENDARY' for e in edges) == 1, 'legendary edge count mismatch')
check(all(e['connection_type']=='LEGENDARY' and e['legendary']=='1' for e in edges if e['legendary']=='1'), 'legendary edge incorrectly flagged')
audit_path = os.path.join(ROOT, 'network_edge_audit.csv')
sens_path = os.path.join(ROOT, 'network_sensitivity.csv')
check(os.path.exists(audit_path), 'Network Audit v2 edge audit is missing')
check(os.path.exists(sens_path), 'Network Audit v2 sensitivity table is missing')
if os.path.exists(audit_path):
    audit = load('network_edge_audit.csv')
    check(len(audit) == len(edges), 'edge audit does not cover all network edges')
    check(all(x['audit_status']=='SUPPORTED' for x in audit), 'edge audit contains unsupported/review rows')
if os.path.exists(sens_path):
    sens = load('network_sensitivity.csv')
    check({x['network'] for x in sens} == {'A_FULL_DOCUMENTED','B_NON_INSTITUTIONAL','C_PERSON_PERSON','D_PERSON_INSTITUTION','E_PERSON_TEXT','F_PERSON_EVENT'}, 'sensitivity network set mismatch')
    check(not any(x['metric']=='edge_count' and x['value'] != '0' and x['network']=='A_FULL_DOCUMENTED' and x.get('note')=='PHYSICAL_MOVEMENT' for x in sens), 'unexpected physical movement sensitivity row')
family_path = os.path.join(ROOT, 'network_relation_families.csv')
family_centrality_path = os.path.join(ROOT, 'network_relation_family_centrality.csv')
check(os.path.exists(family_path), 'relation-family table is missing')
check(os.path.exists(family_centrality_path), 'relation-family centrality table is missing')
if os.path.exists(family_path):
    fr = load('network_relation_families.csv')
    check(len(fr) == len(edges), 'relation-family table does not cover all edges')
    check(set(x['relation_family'] for x in fr) <= {'NON_INSTITUTIONAL','PERSON_INSTITUTION','INSTITUTION_EVENT_ORGANIZER','PERSON_EVENT_PARTICIPATION'}, 'invalid relation family')
    check(sum(x['relation_family']=='PERSON_INSTITUTION' for x in fr) == 14, 'person-institution family count mismatch')
    check(sum(x['relation_family']=='INSTITUTION_EVENT_ORGANIZER' for x in fr) == 22, 'organizer family count mismatch')
    check(sum(x['relation_family']=='PERSON_EVENT_PARTICIPATION' for x in fr) == 13, 'participation family count mismatch')
if os.path.exists(family_centrality_path):
    fc = load('network_relation_family_centrality.csv')
    check({x['relation_family'] for x in fc} == {'PERSON_INSTITUTION','INSTITUTION_EVENT_ORGANIZER','PERSON_EVENT_PARTICIPATION'}, 'relation-family centrality set mismatch')

# Frozen checksums from VERSION.md.
manifest = open(os.path.join(FROZEN,'VERSION.md'),encoding='utf-8').read()
for digest,name in re.findall(r'^([0-9a-f]{64})\s+(\S+)$',manifest,re.M):
    path=os.path.join(FROZEN,name); check(os.path.exists(path),f'missing frozen file {name}')
    if os.path.exists(path): check(hashlib.sha256(open(path,'rb').read()).hexdigest()==digest,f'frozen checksum changed: {name}')

if errors:
    print(f'FAIL: {len(errors)} checks')
    for e in errors: print(' -',e)
    sys.exit(1)
print(f'PASS: network validation — {len(nodes)} nodes, {len(edges)} edges; frozen checksums verified')
print('  node types:', dict(Counter(n['node_type'] for n in nodes)))
print('  edge types:', dict(Counter(e['connection_type'] for e in edges)))
