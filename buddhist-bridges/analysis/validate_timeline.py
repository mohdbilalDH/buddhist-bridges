#!/usr/bin/env python3
"""Validate the Timeline MVP against frozen V3.0 and derived-table invariants."""
import csv, hashlib, json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(ROOT, '..', 'v3.0_frozen')
DATA = os.path.join(ROOT, 'data')
errors = []

def load(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def check(ok, msg):
    if not ok:
        errors.append(msg)

with open(os.path.join(DATA, 'timeline_data.json'), encoding='utf-8') as f:
    d = json.load(f)
marks = d['marks']
check(d['meta']['axis'] == {'start': 300, 'end': 2027}, 'axis must be 300–2027')
check([b['id'] for b in d['bands']] == ['B1','B2','B3','B4','B5','B6'], 'bands must be B1–B6')
check('no carried records under current inclusion criteria' in d['meta']['gaps'][0]['label'], 'B3 safeguard text missing')
check('not a claim of zero Buddhist activity' in d['meta']['gaps'][0]['note'], 'B3 qualification missing')
check(len(marks) > 0, 'no timeline marks emitted')
check(all(m['scope'] in ('CARRIED','CONTEXT','EXCLUDE') for m in marks), 'invalid scope emitted')
check(all(m.get('start') is not None and m.get('end') is not None and m['start'] <= m['end'] for m in marks), 'mark has missing or reversed range')
check(all(m['precision'] != 'FLORUIT' or m['kind'] == 'lifeline' for m in marks), 'floruit used outside lifeline')
check(all(m.get('legendary') is not True for m in marks), 'legendary material should remain unplaced in V3.0')
check(all('sources' in m for m in marks), 'mark missing source metadata')
check(len(d['unplaced']) > 0 and all('start' not in u and 'end' not in u for u in d['unplaced']), 'undated record was placed')
check('record_density' in d['ribbons'] and 'source_density' in d['ribbons'], 'density ribbons missing')

cls = load(os.path.join(FROZEN, 'classification_v3.csv'))
people = load(os.path.join(FROZEN, 'people.csv'))
carried_people = {r['record_id'] for r in cls if r['table']=='PEOPLE' and r['scope'] in ('KEEP','ADAPT')}
people_marks = {m['id'] for m in marks if m['lane']=='people' and m['scope']=='CARRIED'}
check(people_marks == carried_people, f'people mismatch: {len(people_marks)} marks vs {len(carried_people)} classified')
check(sum(1 for m in marks if m['scope']=='CARRIED' and m['lane']=='people') == 43, 'expected 43 carried people')
check(sum(1 for m in marks if m['scope']=='CARRIED' and m.get('single_source')) >= 1, 'single-source carried encoding absent')
check(any(m['lane']=='encounters' for m in marks), 'encounter lane empty')
check(any(m['lane']=='events' for m in marks), 'event lane empty')
check(any(m['lane']=='negatives' for m in marks), 'negative lane empty')

# The frozen manifest is authoritative: verify every listed checksum.
manifest = open(os.path.join(FROZEN, 'VERSION.md'), encoding='utf-8').read()
for digest, name in re.findall(r'^([0-9a-f]{64})\s+(\S+)$', manifest, re.M):
    path = os.path.join(FROZEN, name)
    check(os.path.exists(path), f'manifest file missing: {name}')
    if os.path.exists(path):
        got = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        check(got == digest, f'frozen checksum changed: {name}')

html = open(os.path.join(ROOT, 'timeline_mvp.html'), encoding='utf-8').read()
check('const DATA = {' in html, 'HTML does not embed timeline data')
check('PAD_T = 140' in open(os.path.join(ROOT, 'timeline_mvp_template.html'), encoding='utf-8').read(), 'ribbon/lanes spacing fix missing')
check('Show legendary' in html, 'legendary toggle missing')

if errors:
    print(f'FAIL: {len(errors)} checks')
    for e in errors: print(' -', e)
    sys.exit(1)
print('PASS: Timeline MVP validation')
print(f'  marks={len(marks)} carried={sum(m["scope"]=="CARRIED" for m in marks)} unplaced={len(d["unplaced"])}')
print('  lanes=' + ', '.join(f'{k}:{v}' for k,v in sorted(Counter(m['lane'] for m in marks).items())))
print('  frozen manifest checksums verified')
