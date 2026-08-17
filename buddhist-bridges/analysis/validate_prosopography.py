#!/usr/bin/env python3
"""
Buddhist Bridges — Phase 2, Step 2: PROSOPOGRAPHY VALIDATION
============================================================
Validates the 8 prosopography tables against the frozen V3.0 baseline and the
derived tables. Also re-verifies the frozen SHA-256 manifest is unchanged.

Run:  python3 buddhist-bridges/analysis/validate_prosopography.py
Exit: 0 if all checks pass, 1 otherwise. Prints PASS/FAIL per check.
"""
import csv, collections, hashlib, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(ROOT, '..', 'v3.0_frozen')
DATA = os.path.join(ROOT, 'data')
n_fail = 0

def check(label, ok, detail=''):
    global n_fail
    if not ok:
        n_fail += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {label}" + (f"  [{detail}]" if detail and not ok else ''))

def load(p):
    with open(p, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

reg = load(os.path.join(DATA, 'register.csv'))
role = load(os.path.join(DATA, 'role_x_period.csv'))
trad = load(os.path.join(DATA, 'tradition_x_period.csv'))
typ = load(os.path.join(DATA, 'movement_mediation_typology.csv'))
seq = load(os.path.join(DATA, 'life_course_sequences.csv'))
relc = load(os.path.join(DATA, 'relevance_comparison.csv'))
miss = load(os.path.join(DATA, 'missingness_summary.csv'))
clu = load(os.path.join(DATA, 'typologies.csv'))

print("== Row counts ==")
check('register.csv = 43', len(reg) == 43, f"got {len(reg)}")
check('role_x_period.csv = 60', len(role) == 60, f"got {len(role)}")
check('tradition_x_period.csv = 55', len(trad) == 55, f"got {len(trad)}")
check('movement_mediation_typology.csv = 43', len(typ) == 43, f"got {len(typ)}")
check('life_course_sequences.csv = 43', len(seq) == 43, f"got {len(seq)}")
check('relevance_comparison.csv = 3', len(relc) == 3, f"got {len(relc)}")
check('missingness_summary.csv = 11', len(miss) == 11, f"got {len(miss)}")
check('typologies.csv = 43', len(clu) == 43, f"got {len(clu)}")

print("== Register vs frozen classification ==")
CLS = load(os.path.join(FROZEN, 'classification_v3.csv'))
carried = sorted({c['record_id'] for c in CLS if c['scope'] in ('KEEP', 'ADAPT') and c['table'] == 'PEOPLE'})
ids = [r['person_id'] for r in reg]
check('register covers exactly the carried people', ids == carried,
      f"missing={set(carried)-set(ids)} extra={set(ids)-set(carried)}")
PEOPLE = {p['person_id']: p for p in load(os.path.join(FROZEN, 'people.csv'))}
CLS_BY = {(c['table'], c['record_id']): c for c in CLS}
for r in reg:
    p, c = PEOPLE[r['person_id']], CLS_BY[('PEOPLE', r['person_id'])]
    n = len([s for s in (p['source_ids'] or '').split(';') if s])
    check(f"{r['person_id']} band", r['band'] == c['period_band'], f"{r['band']} vs {c['period_band']}")
    check(f"{r['person_id']} movement", r['movement_status'] == c['movement_status'])
    check(f"{r['person_id']} relevance", r['buddhist_relevance'] == c['buddhist_relevance'])
    check(f"{r['person_id']} source_count", int(r['source_count']) == n)
    check(f"{r['person_id']} role_1 present", bool(r['role_1']))
    check(f"{r['person_id']} tradition_1 present", bool(r['tradition_1']))

print("== Link counts vs frozen link tables ==")
print("    (rule: only relationships with BOTH endpoints carried count — network edges within the carried population, matching build_prosopography.py)")
RELS = load(os.path.join(FROZEN, 'person_person.csv'))
PTX = load(os.path.join(FROZEN, 'person_text.csv'))
PE = load(os.path.join(FROZEN, 'person_event.csv'))
carried_set = set(carried)
rel_c = collections.Counter()
for l in RELS:
    if l['person_a_id'] in carried_set and l['person_b_id'] in carried_set:
        rel_c[l['person_a_id']] += 1
        rel_c[l['person_b_id']] += 1
ptx_c = collections.Counter(l['person_id'] for l in PTX if l['person_id'] in carried_set)
pe_c = collections.Counter(e['person_id'] for e in PE if e['person_id'] in carried_set)
for r in reg:
    check(f"{r['person_id']} n_rels", int(r['n_rels']) == rel_c.get(r['person_id'], 0))
    check(f"{r['person_id']} n_ptx", int(r['n_ptx']) == ptx_c.get(r['person_id'], 0))
    check(f"{r['person_id']} n_events", int(r['n_events']) == pe_c.get(r['person_id'], 0))

print("== Matrix totals (multi-role / multi-tradition are expected) ==")
n_roles = sum(1 for r in reg if r['role_1']) + sum(1 for r in reg if r['role_2']) + sum(1 for r in reg if r['role_3'])
n_rm = sum(int(r['count']) for r in role)
check('role matrix total == role assignments in register', n_rm == n_roles, f"{n_rm} vs {n_roles}")
n_trads = sum(1 for r in reg if r['tradition_1']) + sum(1 for r in reg if r['tradition_2']) + sum(1 for r in reg if r['tradition_3'])
n_tm = sum(int(r['count']) for r in trad)
check('tradition matrix total == tradition assignments in register', n_tm == n_trads, f"{n_tm} vs {n_trads}")
# every band in register appears in matrices
bands = sorted({r['band'][:2] for r in reg})
check('matrices cover all register bands', bands == ['B1', 'B2', 'B4', 'B5', 'B6'], str(bands))

print("== Typology consistency (deterministic from movement + connection_type) ==")
def typ_of(r):
    mv, conn = r['movement_status'], r['connection_types']
    if mv == 'visited': return 'PILGRIM_VISITOR'
    if mv == 'worked': return 'RESIDENT_WORKER'
    if mv == 'studied': return 'STUDENT'
    if mv == 'planned': return 'PLANNED_PILGRIM'
    if 'TEXTUAL_TRANSMISSION' in conn: return 'TEXTUAL_MEDIATOR'
    if 'INSTITUTIONAL' in conn: return 'INSTITUTIONAL_ANCHOR'
    if 'PERSON_ENCOUNTER' in conn: return 'ENCOUNTER_FIGURE'
    if 'INDIRECT_INFLUENCE' in conn: return 'INDIRECT_INFLUENCER'
    return 'UNCLASSIFIED'
exp = collections.Counter(typ_of(r) for r in reg)
got = collections.Counter(t['typology'] for t in typ)
check('typology assignment matches classification rules', exp == got, f"{got} vs expected {exp}")
mv_counts = collections.Counter(r['movement_status'] for r in reg)
check('PILGRIM_VISITOR == visited', got['PILGRIM_VISITOR'] == mv_counts['visited'])
check('STUDENT == studied', got['STUDENT'] == mv_counts['studied'])
check('RESIDENT_WORKER == worked', got['RESIDENT_WORKER'] == mv_counts['worked'])
check('PLANNED_PILGRIM == planned', got['PLANNED_PILGRIM'] == mv_counts['planned'])

print("== Relevance comparison internal consistency ==")
for rel in ('PRIMARY', 'SECONDARY', 'MEDIATOR'):
    row = next(r for r in relc if r['buddhist_relevance'] == rel)
    n = sum(1 for r in reg if r['buddhist_relevance'] == rel)
    check(f"{rel} n_people", int(row['n_people']) == n)
    check(f"{rel} by_band sums", sum(int(x.split('=')[1]) for x in row['by_band'].split('; ')) == n)
    check(f"{rel} by_movement sums", sum(int(x.split('=')[1]) for x in row['by_movement'].split('; ')) == n)
    check(f"{rel} by_direction sums", sum(int(x.split('=')[1]) for x in row['by_direction'].split('; ')) == n)

print("== Missingness internal consistency ==")
def find(label):
    return next(m for m in miss if m['label'] == label)
check('No birth year = 20', int(find('No birth year')['missing_or_unknown']) == sum(1 for r in reg if not r['birth_year']))
check('No death year = 24', int(find('No death year')['missing_or_unknown']) == sum(1 for r in reg if not r['death_year']))
check('All 43 covered by floruit (no birth-year-only gap)', int(find('No floruit (no birth year and no derived floruit)')['missing_or_unknown']) == 0)
check('Movement "-" = 18', int(find('Movement "-" (no physical movement)')['missing_or_unknown']) == mv_counts['-'])
check('Direction UNCERTAIN = 1', int(find('Direction UNCERTAIN')['missing_or_unknown']) == sum(1 for r in reg if r['direction_of_influence'] == 'UNCERTAIN'))
check('Tradition UNKNOWN = 1', int(find('Tradition UNKNOWN')['missing_or_unknown']) == sum(1 for r in reg if r['tradition_1'] == 'UNKNOWN'))
check('No rels = 26', int(find('No person-person relationships')['missing_or_unknown']) == sum(1 for r in reg if int(r['n_rels']) == 0))
check('No ptx = 31', int(find('No person-text links')['missing_or_unknown']) == sum(1 for r in reg if int(r['n_ptx']) == 0))
check('No events = 41', int(find('No person-event links')['missing_or_unknown']) == sum(1 for r in reg if int(r['n_events']) == 0))
check('No dated activity = 10', int(find('No dated activity (empty life-course sequence)')['missing_or_unknown']) == sum(1 for s in seq if s['n_dated_events'] == '0'))

print("== Life-course sequences internal consistency ==")
for s in seq:
    n = len([x for x in s['sequence'].split(' -> ') if x not in ('', 'NO DATED ACTIVITY')])
    check(f"{s['person_id']} n_dated_events", int(s['n_dated_events']) == n)
check('sequence rows == register ids', [s['person_id'] for s in seq] == ids)

print("== Frozen baseline integrity (SHA-256 manifest) ==")
version = open(os.path.join(FROZEN, 'VERSION.md'), encoding='utf-8').read()
checksums = {}
for m in re.finditer(r'`([a-f0-9]{64})`\s*\|\s*`([^`]+)`|([a-f0-9]{64})  ([^\s]+)', version):
    h, f = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
    checksums[f] = h
if not checksums:
    for line in version.splitlines():
        parts = line.split()
        if len(parts) == 2 and re.fullmatch(r'[a-f0-9]{64}', parts[0]):
            checksums[parts[1]] = parts[0]
for fname, expected in checksums.items():
    fp = os.path.join(FROZEN, fname)
    if os.path.exists(fp):
        h = hashlib.sha256(open(fp, 'rb').read()).hexdigest()
        check(f"frozen {fname} unchanged", h == expected)
    else:
        check(f"frozen {fname} present", False, 'file missing')

print()
if n_fail == 0:
    print("ALL PROSOPOGRAPHY CHECKS PASSED")
    sys.exit(0)
else:
    print(f"{n_fail} CHECK(S) FAILED")
    sys.exit(1)
