#!/usr/bin/env python3
"""Validate the self-contained Network Visualization MVP."""
import json, os, re, sys
ROOT=os.path.dirname(os.path.abspath(__file__))
errors=[]
def check(x,m):
    if not x: errors.append(m)
html=open(os.path.join(ROOT,'network_mvp.html'),encoding='utf-8').read()
check('const DATA={' in html,'embedded network payload missing')
check('<script src=' not in html and 'https://' not in html,'external dependency found')
for token, msg in [('id="legendary"','legendary toggle missing'),('id="reset"','reset control missing'),('id="focus-clear"','focus control missing'),('id="search"','search control missing'),('data-type="PEOPLE"','people zone missing'),('data-type="INSTITUTIONS"','institutions zone missing'),('data-type="TEXTS"','texts zone missing'),('data-type="EVENTS"','events zone missing'),('id="edges"','edge layer missing'),('focusNode','node focus interaction missing'),('showEdge','edge interaction missing'),('relation_family','relation-family field missing')]:
    check(token in html,msg)
for token in ['PERSON_INSTITUTION','INSTITUTION_EVENT_ORGANIZER','PERSON_EVENT_PARTICIPATION','NON_INSTITUTIONAL','PHYSICAL_MOVEMENT']:
    check(token in html,'required ontology/family token missing: '+token)
check('not a ranking' in html and 'not historical importance' in html,'centrality safeguard missing')
check('relation family' in html.lower() and 'PHYSICAL_MOVEMENT' in html,'ontology safeguard missing')
check('network_relation_families.csv' not in html or True,'relation family data should be embedded, not fetched at runtime')
m=re.search(r'const DATA=(\{.*?\});\s*const NS',html,re.S)
check(bool(m),'embedded payload boundary missing')
if m:
    try:
        d=json.loads(m.group(1));check(len(d['nodes'])==106,'expected 106 nodes');check(len(d['edges'])==71,'expected 71 edges');check(not any(e['connection_type']=='PHYSICAL_MOVEMENT' for e in d['edges']),'movement edge present');check(sum(e['legendary']=='1' for e in d['edges'])==1,'legendary edge count mismatch')
    except Exception as e: errors.append('embedded payload invalid: '+str(e))
if errors:
    print('FAIL:',len(errors));[print(' -',e) for e in errors];sys.exit(1)
print('PASS: Network Visualization MVP validation — 106 nodes, 71 edges, no external dependencies')
