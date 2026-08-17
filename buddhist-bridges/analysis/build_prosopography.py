#!/usr/bin/env python3
"""
Buddhist Bridges — Phase 2, Step 2: PROSOPOGRAPHY (prosopography_design_v1.md)

Builds the 43-person analytical register and all comparison tables from the
frozen V3.0 dataset + validated derived tables (analysis/data/). Read-only
with respect to V3.0. Descriptive statistics only — no inferential tests,
no importance ranking, source counts are never treated as importance.

Outputs (analysis/data/):
  register.csv                  — 43-person analytical register
  role_x_period.csv             — role taxonomy x period band matrix
  tradition_x_period.csv        — tradition x period band matrix
  movement_mediation_typology.csv — movement x relevance x connection types
  life_course_sequences.csv     — dated activity sequences
  relevance_comparison.csv      — PRIMARY vs SECONDARY vs MEDIATOR
  missingness_summary.csv       — per-field missingness
  typologies.csv                — descriptive typology (n=43, exploratory)
"""
import csv, os, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(ROOT, '..', 'v3.0_frozen')
DATA = os.path.join(ROOT, 'data')

def load(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

PEOPLE = load(os.path.join(FROZEN, 'people.csv'))
CLS = load(os.path.join(FROZEN, 'classification_v3.csv'))
RELS = load(os.path.join(FROZEN, 'person_person.csv'))
PTX = load(os.path.join(FROZEN, 'person_text.csv'))
PE = load(os.path.join(FROZEN, 'person_event.csv'))
TRAVELS = load(os.path.join(FROZEN, 'travels.csv'))
TEXTS = load(os.path.join(FROZEN, 'texts.csv'))
EVENTS = load(os.path.join(FROZEN, 'events.csv'))
FLORUITS = {r['person_id']: r for r in load(os.path.join(DATA, 'person_floruits.csv'))}
TAX = {r['person_id']: r for r in load(os.path.join(DATA, 'tradition_taxonomy.csv'))}
IMAP = {r['person_id']: r for r in load(os.path.join(DATA, 'institution_mapping.csv'))}

PERSON = {p['person_id']: p for p in PEOPLE}
CARRIED = {c['record_id'] for c in CLS if c['scope'] in ('KEEP', 'ADAPT') and c['table'] == 'PEOPLE'}
CLS_BY = {(c['table'], c['record_id']): c for c in CLS}

def cls_of(table, rid):
    return CLS_BY.get((table, rid), {})

def write(name, rows, fields):
    with open(os.path.join(DATA, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: (r.get(k) if r.get(k) is not None else '') for k in fields})
    print(f"  wrote {name} ({len(rows)} rows)")

PROV = "Derived 2026-08-17 from frozen V3.0 + analysis/data derived tables by build_prosopography.py; descriptive only."

# =====================================================================
# ROLE TAXONOMY (12 roles, multi-role allowed) — from profession_role
# =====================================================================
ROLES = {
    'P-0001': ['PILGRIM_MONK'], 'P-0002': ['SCHOLAR_MONK'], 'P-0003': ['SCHOLAR_MONK'],
    'P-0004': ['SCHOLAR_MONK'], 'P-0005': ['SCHOLAR_MONK'], 'P-0006': ['MONK_GENERAL'],
    'P-0009': ['SCHOLAR_MONK'], 'P-0010': ['SCHOLAR_MONK'],
    'P-0011': ['PILGRIM_MONK', 'SCHOLAR_MONK', 'TRANSLATOR'], 'P-0012': ['MONK_GENERAL'],
    'P-0013': ['PILGRIM_MONK'], 'P-0014': ['PILGRIM_MONK'], 'P-0015': ['PILGRIM_MONK'],
    'P-0016': ['PILGRIM_MONK'], 'P-0017': ['PILGRIM_MONK'], 'P-0018': ['PILGRIM_MONK'],
    'P-0020': ['PILGRIM_MONK'], 'P-0021': ['PILGRIM_MONK'], 'P-0022': ['PILGRIM_MONK'],
    'P-0023': ['MASTER_PATRIARCH', 'INSTITUTIONAL_LEADER'],
    'P-0024': ['MASTER_PATRIARCH', 'INSTITUTIONAL_LEADER'],
    'P-0028': ['MODERN_INTELLECTUAL', 'ACADEMIC'], 'P-0029': ['MODERN_INTELLECTUAL'],
    'P-0030': ['LITERARY_FIGURE', 'NON_BUDDHIST_FIGURE'],
    'P-0034': ['LITERARY_FIGURE', 'ACTIVIST', 'MONK_GENERAL'],
    'P-0038': ['ACTIVIST', 'NON_BUDDHIST_FIGURE'],
    'P-0051': ['LITERARY_FIGURE', 'MONK_GENERAL'],
    'P-0052': ['MONK_GENERAL', 'LITERARY_FIGURE'],
    'P-0053': ['ACADEMIC', 'INSTITUTIONAL_LEADER'], 'P-0054': ['ACADEMIC'], 'P-0055': ['ACADEMIC'],
    'P-0062': ['INSTITUTIONAL_LEADER', 'MONK_GENERAL'],
    'P-0063': ['BHIKKHUNI', 'ACADEMIC'], 'P-0064': ['BHIKKHUNI', 'INSTITUTIONAL_LEADER'],
    'P-0065': ['MONK_GENERAL', 'INSTITUTIONAL_LEADER'],
    'P-0068': ['LITERARY_FIGURE', 'ACADEMIC'],
    'P-0071': ['ACTIVIST', 'NON_BUDDHIST_FIGURE'], 'P-0072': ['PILGRIM_MONK'],
    'P-0073': ['ACADEMIC', 'MODERN_INTELLECTUAL'],
    'P-0074': ['MASTER_PATRIARCH', 'INSTITUTIONAL_LEADER'], 'P-0075': ['MASTER_PATRIARCH'],
    'P-0076': ['LITERARY_FIGURE', 'ACADEMIC', 'NON_BUDDHIST_FIGURE'], 'P-0077': ['MASTER_PATRIARCH'],
}
ROLE_NAMES = ['PILGRIM_MONK', 'SCHOLAR_MONK', 'MASTER_PATRIARCH', 'MONK_GENERAL', 'BHIKKHUNI',
              'TRANSLATOR', 'LITERARY_FIGURE', 'ACADEMIC', 'ACTIVIST', 'MODERN_INTELLECTUAL',
              'INSTITUTIONAL_LEADER', 'NON_BUDDHIST_FIGURE']

# =====================================================================
# 1. REGISTER
# =====================================================================
rel_by, rel_kind = collections.Counter(), collections.defaultdict(list)
for r in RELS:
    if r['person_a_id'] in CARRIED and r['person_b_id'] in CARRIED:
        rel_by[r['person_a_id']] += 1; rel_by[r['person_b_id']] += 1
        rel_kind[r['person_a_id']].append(r['relationship_kind']); rel_kind[r['person_b_id']].append(r['relationship_kind'])
ptx_by, ptx_role = collections.Counter(), collections.defaultdict(list)
for l in PTX:
    if l['person_id'] in CARRIED:
        ptx_by[l['person_id']] += 1; ptx_role[l['person_id']].append(l['link_type'])
pe_by, pe_role = collections.Counter(), collections.defaultdict(list)
for e in PE:
    if e['person_id'] in CARRIED:
        pe_by[e['person_id']] += 1; pe_role[e['person_id']].append(e['role'])

rows = []
for pid in sorted(CARRIED):
    p = PERSON[pid]
    c = cls_of('PEOPLE', pid)
    f = FLORUITS.get(pid, {})
    t = TAX.get(pid, {})
    im = IMAP.get(pid, {})
    srcs = [s for s in (p['source_ids'] or '').split(';') if s]
    rows.append({
        'person_id': pid, 'full_name': p['full_name'], 'period': p['period'],
        'band': c.get('period_band', ''), 'nationality_region': p['nationality_region'],
        'profession_role': p['profession_role'],
        'role_1': ROLES[pid][0] if ROLES.get(pid) else '', 'role_2': ROLES[pid][1] if ROLES.get(pid) and len(ROLES[pid]) > 1 else '',
        'role_3': ROLES[pid][2] if ROLES.get(pid) and len(ROLES[pid]) > 2 else '',
        'religious_affiliation': p['religious_affiliation'],
        'tradition_1': t.get('tradition_1', ''), 'tradition_2': t.get('tradition_2', ''), 'tradition_3': t.get('tradition_3', ''),
        'movement_status': c.get('movement_status', ''), 'buddhist_relevance': c.get('buddhist_relevance', ''),
        'scope': c.get('scope', ''), 'direction_of_influence': p['direction_of_influence'],
        'exchange_types': c.get('exchange_types', ''), 'connection_types': c.get('connection_type', ''),
        'institution_status': im.get('mapping_status', ''), 'mapped_institution_ids': im.get('mapped_institution_ids', ''),
        'birth_year': p['birth_year'], 'death_year': p['death_year'],
        'floruit_start': f.get('floruit_start', ''), 'floruit_end': f.get('floruit_end', ''),
        'confidence': p['confidence'], 'status': p['status'],
        'source_count': len(srcs), 'single_source': 'YES' if len(srcs) == 1 else 'NO',
        'n_rels': rel_by.get(pid, 0), 'rel_kinds': ';'.join(sorted(set(rel_kind.get(pid, [])))),
        'n_ptx': ptx_by.get(pid, 0), 'ptx_roles': ';'.join(sorted(set(ptx_role.get(pid, [])))),
        'n_events': pe_by.get(pid, 0), 'event_roles': ';'.join(sorted(set(pe_role.get(pid, [])))),
        'notes': p['notes'],
    })
write('register.csv', rows, ['person_id', 'full_name', 'period', 'band', 'nationality_region', 'profession_role',
    'role_1', 'role_2', 'role_3', 'religious_affiliation', 'tradition_1', 'tradition_2', 'tradition_3',
    'movement_status', 'buddhist_relevance', 'scope', 'direction_of_influence', 'exchange_types', 'connection_types',
    'institution_status', 'mapped_institution_ids', 'birth_year', 'death_year', 'floruit_start', 'floruit_end',
    'confidence', 'status', 'source_count', 'single_source', 'n_rels', 'rel_kinds', 'n_ptx', 'ptx_roles',
    'n_events', 'event_roles', 'notes'])

# =====================================================================
# 2. ROLE x PERIOD MATRIX
# =====================================================================
def band_short(band):
    for b in ('B1', 'B2', 'B3', 'B4', 'B5', 'B6'):
        if band.startswith(b):
            return b
    return '?'

reg = rows  # register rows from section 1
rows = []
for role in ROLE_NAMES:
    for b in ('B1', 'B2', 'B4', 'B5', 'B6'):
        n = sum(1 for r in reg if role in (r['role_1'], r['role_2'], r['role_3']) and band_short(r['band']) == b)
        rows.append({'role': role, 'band': b, 'count': n, 'basis': 'register.csv role_1/2/3 x band', 'provenance': PROV, 'notes': ''})
write('role_x_period.csv', rows, ['role', 'band', 'count', 'basis', 'provenance', 'notes'])

# =====================================================================
# 3. TRADITION x PERIOD MATRIX
# =====================================================================
TRADITIONS = ['SEON_CHAN', 'ESOTERIC', 'YOGACARA', 'VINAYA', 'HWA_EOM', 'PURE_LAND',
              'GENERAL_BUDDHISM', 'LAY_BUDDHIST', 'NON_BUDDHIST', 'THERAVADA_ORIENTED', 'UNKNOWN']
rows = []
for trad in TRADITIONS:
    for b in ('B1', 'B2', 'B4', 'B5', 'B6'):
        n = sum(1 for r in reg if trad in (r['tradition_1'], r['tradition_2'], r['tradition_3']) and band_short(r['band']) == b)
        rows.append({'tradition': trad, 'band': b, 'count': n, 'basis': 'tradition_taxonomy.csv x band', 'provenance': PROV, 'notes': ''})
write('tradition_x_period.csv', rows, ['tradition', 'band', 'count', 'basis', 'provenance', 'notes'])

# =====================================================================
# 4. MOVEMENT / MEDIATION TYPOLOGY
# =====================================================================
def typology_of(r):
    mv, rel, conn = r['movement_status'], r['buddhist_relevance'], r['connection_types']
    if mv == 'visited':
        return 'PILGRIM_VISITOR'
    if mv == 'worked':
        return 'RESIDENT_WORKER'
    if mv == 'studied':
        return 'STUDENT'
    if mv == 'planned':
        return 'PLANNED_PILGRIM'
    if 'TEXTUAL_TRANSMISSION' in conn:
        return 'TEXTUAL_MEDIATOR'
    if 'INSTITUTIONAL' in conn:
        return 'INSTITUTIONAL_ANCHOR'
    if 'PERSON_ENCOUNTER' in conn:
        return 'ENCOUNTER_FIGURE'
    if 'INDIRECT_INFLUENCE' in conn:
        return 'INDIRECT_INFLUENCER'
    return 'UNCLASSIFIED'
rows = []
for r in reg:
    rows.append({'person_id': r['person_id'], 'full_name': r['full_name'], 'typology': typology_of(r),
                 'movement_status': r['movement_status'], 'buddhist_relevance': r['buddhist_relevance'],
                 'connection_types': r['connection_types'], 'direction_of_influence': r['direction_of_influence'],
                 'basis': 'movement_status + connection_type from classification_v3.csv', 'provenance': PROV, 'notes': ''})
write('movement_mediation_typology.csv', rows, ['person_id', 'full_name', 'typology', 'movement_status', 'buddhist_relevance', 'connection_types', 'direction_of_influence', 'basis', 'provenance', 'notes'])

# =====================================================================
# 5. LIFE-COURSE / ACTIVITY SEQUENCES (dated events only)
# =====================================================================
travel_by = collections.defaultdict(list)
for t in TRAVELS:
    if t['person_id'] in CARRIED and t['travel_start_year']:
        travel_by[t['person_id']].append(int(t['travel_start_year']))
text_by = collections.defaultdict(list)
for l in PTX:
    if l['person_id'] in CARRIED:
        d = TEXTS and next((x for x in TEXTS if x['text_id'] == l['text_id']), None)
        if d and d['date'] and d['date'][:4].isdigit():
            text_by[l['person_id']].append((int(d['date'][:4]), l['link_type']))
event_by = collections.defaultdict(list)
for e in PE:
    if e['person_id'] in CARRIED:
        ev = next((x for x in EVENTS if x['event_id'] == e['event_id']), None)
        if ev and ev['start_date'] and ev['start_date'][:4].isdigit():
            event_by[e['person_id']].append((int(ev['start_date'][:4]), e['role']))

rows = []
for r in reg:
    pid = r['person_id']
    seq = []
    if r['birth_year']:
        seq.append(f"BIRTH {r['birth_year']}")
    for y in sorted(travel_by.get(pid, [])):
        seq.append(f"TRAVEL {y}")
    for y, lt in sorted(text_by.get(pid, [])):
        seq.append(f"TEXT {y} ({lt})")
    for y, role in sorted(event_by.get(pid, [])):
        seq.append(f"EVENT {y} ({role})")
    if r['death_year']:
        seq.append(f"DEATH {r['death_year']}")
    rows.append({'person_id': pid, 'full_name': r['full_name'], 'sequence': ' -> '.join(seq) if seq else 'NO DATED ACTIVITY',
                 'n_dated_events': len(seq), 'basis': 'birth/death years + travel_start_year + text dates + event start dates (explicit dates only)',
                 'provenance': PROV, 'notes': 'Floruit-based activity (APPROX) excluded from sequences; see person_floruits.csv'})
write('life_course_sequences.csv', rows, ['person_id', 'full_name', 'sequence', 'n_dated_events', 'basis', 'provenance', 'notes'])
seq_rows = rows

# =====================================================================
# 6. PRIMARY vs SECONDARY vs MEDIATOR COMPARISON
# =====================================================================
rows = []
for rel in ('PRIMARY', 'SECONDARY', 'MEDIATOR'):
    sub = [r for r in reg if r['buddhist_relevance'] == rel]
    rows.append({
        'buddhist_relevance': rel, 'n_people': len(sub),
        'by_band': '; '.join(f"{b}={sum(1 for r in sub if band_short(r['band']) == b)}" for b in ('B1', 'B2', 'B4', 'B5', 'B6')),
        'by_movement': '; '.join(f"{m}={sum(1 for r in sub if r['movement_status'] == m)}" for m in ('visited', 'worked', 'studied', 'planned', '-')),
        'by_direction': '; '.join(f"{d}={sum(1 for r in sub if r['direction_of_influence'] == d)}" for d in ('INDIA_TO_KOREA', 'KOREA_TO_INDIA', 'BIDIRECTIONAL', 'UNCERTAIN')),
        'by_confidence': '; '.join(f"{c}={sum(1 for r in sub if r['confidence'] == c)}" for c in ('HIGH', 'MEDIUM', 'LOW', 'SPECULATIVE')),
        'single_source': sum(1 for r in sub if r['single_source'] == 'YES'),
        'median_source_count': sorted(int(r['source_count']) for r in sub)[len(sub) // 2] if sub else 0,
        'n_with_rels': sum(1 for r in sub if r['n_rels'] > 0),
        'n_with_ptx': sum(1 for r in sub if r['n_ptx'] > 0),
        'n_with_events': sum(1 for r in sub if r['n_events'] > 0),
        'basis': 'register.csv grouped by buddhist_relevance; source counts are evidence metadata, NOT importance',
        'provenance': PROV, 'notes': 'B1 vs B6 counts are NOT directly comparable without source-density qualification (see source_mix_by_band.csv)',
    })
write('relevance_comparison.csv', rows, ['buddhist_relevance', 'n_people', 'by_band', 'by_movement', 'by_direction', 'by_confidence', 'single_source', 'median_source_count', 'n_with_rels', 'n_with_ptx', 'n_with_events', 'basis', 'provenance', 'notes'])

# =====================================================================
# 7. MISSINGNESS SUMMARY
# =====================================================================
rows = []
def miss(field, label, pred):
    n = sum(1 for r in reg if pred(r))
    rows.append({'field': field, 'label': label, 'missing_or_unknown': n, 'of_43': f"{n}/43",
                 'basis': 'register.csv', 'provenance': PROV, 'notes': ''})
miss('birth_year', 'No birth year', lambda r: not r['birth_year'])
miss('death_year', 'No death year', lambda r: not r['death_year'])
miss('floruit', 'No floruit (no birth year and no derived floruit)', lambda r: not r['birth_year'] and not r['floruit_start'])
miss('movement', 'Movement "-" (no physical movement)', lambda r: r['movement_status'] == '-')
miss('direction', 'Direction UNCERTAIN', lambda r: r['direction_of_influence'] == 'UNCERTAIN')
miss('tradition', 'Tradition UNKNOWN', lambda r: r['tradition_1'] == 'UNKNOWN')
miss('institution', 'Institution UNMAPPED or NO_INSTITUTION', lambda r: r['institution_status'] in ('UNMAPPED', 'NO_INSTITUTION'))
miss('rels', 'No person-person relationships', lambda r: r['n_rels'] == 0)
miss('ptx', 'No person-text links', lambda r: r['n_ptx'] == 0)
miss('events', 'No person-event links', lambda r: r['n_events'] == 0)
seq_by = {s['person_id']: int(s['n_dated_events']) for s in seq_rows}
miss('dated_activity', 'No dated activity (empty life-course sequence)', lambda r: seq_by.get(r['person_id'], 0) == 0)
write('missingness_summary.csv', rows, ['field', 'label', 'missing_or_unknown', 'of_43', 'basis', 'provenance', 'notes'])

# =====================================================================
# 8. DESCRIPTIVE TYPOLOGIES (n=43, exploratory)
# =====================================================================
def cluster_of(r):
    b = band_short(r['band'])
    if b == 'B1':
        return 'B1 SILLA MONK COHORT' if r['movement_status'] in ('visited', 'studied') else 'B1 SILLA SCHOLAR'
    if b == 'B2':
        return 'B2 JIKONG CIRCLE' if r['n_rels'] > 0 or r['tradition_1'] == 'SEON_CHAN' else 'B2 GORYEO MONK'
    if b == 'B4':
        return 'B4 COLONIAL INTELLECTUAL' if r['role_1'] in ('MODERN_INTELLECTUAL', 'LITERARY_FIGURE') else 'B4 COLONIAL FIGURE'
    if b == 'B5':
        return 'B5 POSTWAR FIGURE'
    if b == 'B6':
        if r['role_1'] == 'ACADEMIC':
            return 'B6 ACADEMIC'
        if r['role_1'] in ('INSTITUTIONAL_LEADER', 'BHIKKHUNI'):
            return 'B6 INSTITUTIONAL MONASTIC'
        return 'B6 CONTEMPORARY FIGURE'
    return 'UNCLASSIFIED'
rows = []
for r in reg:
    rows.append({'person_id': r['person_id'], 'full_name': r['full_name'], 'cluster': cluster_of(r),
                 'basis': 'Descriptive clustering on band + role + movement + tradition; exploratory, not inferential',
                 'provenance': PROV, 'notes': 'Cluster labels are descriptive groupings for comparison, NOT claims of historical importance'})
write('typologies.csv', rows, ['person_id', 'full_name', 'cluster', 'basis', 'provenance', 'notes'])

print("\nProsopography tables written to", DATA)