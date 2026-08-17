#!/usr/bin/env python3
"""
Buddhist Bridges — Phase 2, Step 3: TIMELINE MVP DATA BUILDER (timeline_design_v1.md)
======================================================================================
Reads frozen V3.0 + validated derived tables + prosopography outputs (register,
tradition taxonomy, translation dates, travel date ranges, density) and emits:

  analysis/data/timeline_data.json   — machine-readable timeline dataset
  analysis/timeline_mvp.html         — single self-contained HTML timeline (data embedded)

Rules enforced here:
  * No invented dates: marks with no explicit date are either fuzzy spans anchored to
    documented ranges (flagged APPROX) or listed as UNPLACED records, never given a date.
  * Event date vs evidence date: encounter marks only use years explicitly stated in the
    evidence field, via an auditable per-relationship map (quoted below), never a blanket regex.
  * Floruit estimates are rendered as fuzzy lifelines, never as event dates.
  * Legendary material flagged `legendary:true` (off by default in the UI).
  * Source counts are metadata; single-source records are flagged for hatching, never used
    as importance.
  * Frozen V3.0 is read-only here.
"""
import csv, hashlib, json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
FROZEN = os.path.join(ROOT, '..', 'v3.0_frozen')
DATA = os.path.join(ROOT, 'data')

def load(base, name):
    with open(os.path.join(base, name), encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

F = lambda n: load(FROZEN, n)
D = lambda n: load(DATA, n)

PEOPLE, CLS, RELS, PTX, PE = F('people.csv'), F('classification_v3.csv'), F('person_person.csv'), F('person_text.csv'), F('person_event.csv')
TRAVELS, TEXTS, EVENTS, INSTS, PLACES, SOURCES = F('travels.csv'), F('texts.csv'), F('events.csv'), F('institutions.csv'), F('places.csv'), F('sources.csv')
FLORUITS = {r['person_id']: r for r in D('person_floruits.csv')}
TAX = {r['person_id']: r for r in D('tradition_taxonomy.csv')}
TRAVEL_RANGES = {r['travel_id']: r for r in D('travel_date_ranges.csv')}
TRANS_DATES = {r['link_id']: r for r in D('translation_dates.csv')}
REGISTER = {r['person_id']: r for r in D('register.csv')}

PERSON = {p['person_id']: p for p in PEOPLE}
PLACE = {p['place_id']: p for p in PLACES}
CLS_BY = {(c['table'], c['record_id']): c for c in CLS}
TEXT_BY = {t['text_id']: t for t in TEXTS}
EVENT_BY = {e['event_id']: e for e in EVENTS}

def cls(table, rid):
    return CLS_BY.get((table, rid), {})

# Scope normalization: classification KEEP/ADAPT == carried population (UI filter "Carried")
def norm_scope(s):
    return {'KEEP': 'CARRIED', 'ADAPT': 'CARRIED'}.get(s, s)

def srcs_of(p):
    return [s for s in (p.get('source_ids') or '').split(';') if s]

SRC_LABEL = {}
for s in SOURCES:
    title = s.get('title') or s.get('source_title') or s.get('name') or s['source_id']
    SRC_LABEL[s['source_id']] = str(title)[:60]

def band_of(table, rid):
    c = cls(table, rid)
    b = c.get('period_band', '')
    return b[:2] if b.startswith('B') else ''

BANDS = [
    {'id': 'B1', 'label': 'B1 Ancient / early-medieval', 'start': 300, 'end': 900},
    {'id': 'B2', 'label': 'B2 Silla / Goryeo', 'start': 900, 'end': 1392},
    {'id': 'B3', 'label': 'B3 Joseon', 'start': 1392, 'end': 1900},
    {'id': 'B4', 'label': 'B4 Modern / colonial', 'start': 1900, 'end': 1945},
    {'id': 'B5', 'label': 'B5 1945–1990', 'start': 1945, 'end': 1990},
    {'id': 'B6', 'label': 'B6 1990–2026', 'start': 1990, 'end': 2027},
]

# ---------------------------------------------------------------- encounters
# Auditable map: relationship_id -> (year, quoted evidence). Years are only taken
# where the evidence states an explicit event year (not a publication year).
ENCOUNTER_YEARS = {
    'R-0002': (531,  '"(531)" — Gyeomik\'s return voyage with Baedalta'),
    'R-0004': (1916, '"Tokyo 1916 Imperial University lecture meeting"'),
    'R-0005': (1916, '"Two meetings at Yokohama 1916"'),
    'R-0013': (1971, '"1971 ashram visit"'),
}

# ---------------------------------------------------------------- negatives
# Documented negatives with dates (from freeze review; see unresolved_v3.0.md).
NEGATIVES = [
    {'id': 'N-0001', 'year': 1929, 'label': 'Tagore → Korea visit: planned, never realised',
     'detail': 'CONTEXT link L-0016: Rabindranath Tagore → Korea (Seoul) (VISITED) planned 1929 — Tagore never visited Korea.',
     'sources': []},
    {'id': 'N-0002', 'year': 1981, 'label': 'Kelaniya–Bongeunsa sisterhood: agreed, never realised',
     'detail': 'Temple twinning agreed Dec 1981 (Dong-A 1982); never realised. Documented negative from unresolved_v3.0.md.',
     'sources': []},
]

marks, unplaced = [], []

def add(m):
    marks.append(m)

def unplaced_add(rec):
    unplaced.append(rec)

# ---------------------------------------------------------------- people
def person_mark(pid, scope):
    p = PERSON[pid]
    c = cls('PEOPLE', pid)
    reg = REGISTER.get(pid, {})
    fl = FLORUITS.get(pid, {})
    ss = [s for s in srcs_of(p)]
    legend = p['status'] == 'LEGENDARY'
    birth, death = p['birth_year'] or '', p['death_year'] or ''
    floruit = bool(fl.get('floruit_start'))
    explicit_span = bool(birth and death)
    start = int(birth) if birth else (int(fl['floruit_start']) if floruit else None)
    # Some derived floruits have only a documented activity start. Keep that
    # explicit approximate anchor as a point rather than inventing an end year.
    end = int(death) if death else (int(fl['floruit_end']) if fl.get('floruit_end') else start)
    if start is None:
        unplaced_add({'id': pid, 'label': p['full_name'], 'reason': 'no birth year and no derived floruit',
                      'legendary': legend, 'scope': scope, 'note': (p['notes'] or '')[:120]})
        return
    # activity ticks: dated travels / author texts / event participation
    ticks = []
    for t in TRAVELS:
        if t['person_id'] == pid and t['travel_start_year']:
            ticks.append({'year': int(t['travel_start_year']), 'kind': 'travel', 'ref': t['travel_id']})
    for l in PTX:
        if l['person_id'] == pid and l['link_type'] == 'AUTHOR':
            tx = TEXT_BY.get(l['text_id'])
            if tx and tx['date'] and tx['date'][:4].isdigit():
                ticks.append({'year': int(tx['date'][:4]), 'kind': 'text', 'ref': l['text_id']})
    for e in PE:
        if e['person_id'] == pid:
            ev = EVENT_BY.get(e['event_id'])
            if ev and ev['start_date'] and ev['start_date'][:4].isdigit():
                ticks.append({'year': int(ev['start_date'][:4]), 'kind': 'event', 'ref': e['event_id']})
    ticks = sorted(set((t['year'], t['kind'], t['ref']) for t in ticks))
    add({
        'id': pid, 'lane': 'people', 'kind': 'lifeline',
        'start': start, 'end': end,
        'precision': 'EXPLICIT' if explicit_span else 'FLORUIT',
        'label': p['full_name'], 'sub': (reg.get('role_1') or ''),
        'confidence': p['confidence'], 'status': p['status'], 'legendary': legend,
        'direction': p['direction_of_influence'],
        'tradition': (reg.get('tradition_1') or ''), 'connection_types': c.get('connection_type', ''),
        'band': band_of('PEOPLE', pid), 'scope': scope,
        'single_source': len(ss) == 1, 'source_count': len(ss),
        'sources': ss,
        'ticks': [{'year': y, 'kind': k, 'ref': r} for (y, k, r) in ticks],
        'card': {'full_name': p['full_name'], 'period': p['period'], 'profession_role': p['profession_role'],
                 'religious_affiliation': p['religious_affiliation'], 'nationality_region': p['nationality_region'],
                 'institution_org': p['institution_org'], 'birth_year': birth, 'death_year': death,
                 'floruit': f"{fl.get('floruit_start','')}-{fl.get('floruit_end','')}" if floruit else '',
                 'travel_summary': p['travel_summary'], 'evidence_of_influence': p['evidence_of_influence'],
                 'historical_significance': p['historical_significance'], 'notes': p['notes'],
                 'rationale': c.get('rationale', ''), 'movement_status': c.get('movement_status', ''),
                 'buddhist_relevance': c.get('buddhist_relevance', ''), 'exchange_types': c.get('exchange_types', ''),
                 'roles': ' + '.join(x for x in (reg.get('role_1',''), reg.get('role_2',''), reg.get('role_3','')) if x),
                 'rels': reg.get('n_rels', ''), 'ptx': reg.get('n_ptx', ''), 'events': reg.get('n_events', '')},
    })

carried_people = sorted({c['record_id'] for c in CLS if c['scope'] in ('KEEP', 'ADAPT') and c['table'] == 'PEOPLE'})
for pid in carried_people:
    person_mark(pid, 'CARRIED')
# context/exclude people (dimmed; off by default) — legendary first (undated → unplaced)
ctx_people = sorted({c['record_id'] for c in CLS if c['scope'] in ('CONTEXT', 'EXCLUDE') and c['table'] == 'PEOPLE'})
for pid in ctx_people:
    person_mark(pid, norm_scope(cls('PEOPLE', pid).get('scope', 'EXCLUDE')))

# ---------------------------------------------------------------- travels
def travel_mark(t, scope):
    pid = t['person_id']
    p = PERSON.get(pid, {})
    pr = t['travel_dates_precision']
    sy = t['travel_start_year']
    ey = t['travel_end_year']
    rng = TRAVEL_RANGES.get(t['travel_id'], {})
    start = int(sy) if sy else None
    end = int(ey) if ey else None
    if start is None:
        if rng.get('range_start'):
            start, end = int(rng['range_start']), int(rng['range_end'] or rng['range_start'])
            pr = 'APPROX'
        else:
            unplaced_add({'id': t['travel_id'], 'label': f"{t['travel_id']} ({p.get('full_name','')})",
                          'reason': 'no dated activity in frozen data (UNDOCUMENTED)',
                          'legendary': False, 'scope': scope, 'note': (t['notes'] or '')[:120]})
            return
    origin = PLACE.get(t['origin_place_id'], {}).get('place_name', t['origin_place_id'])
    dest = PLACE.get(t['destination_place_id'], {}).get('place_name', t['destination_place_id'])
    add({
        'id': t['travel_id'], 'lane': 'travels', 'kind': 'travel',
        'start': start, 'end': end or start,
        'precision': pr, 'label': f"{p.get('full_name','')} — {origin} → {dest}",
        'sub': t['purpose'], 'confidence': t['confidence'], 'status': 'VERIFIED',
        'legendary': False, 'direction': p.get('direction_of_influence', ''),
        'tradition': '', 'connection_types': 'PHYSICAL_MOVEMENT',
        'band': band_of('TRAVELS', t['travel_id']), 'scope': scope,
        'single_source': False, 'source_count': 0, 'sources': [],
        'ticks': [], 'card': {'travel_id': t['travel_id'], 'person': p.get('full_name', ''),
                              'origin': origin, 'destination': dest, 'route': t['route_description'],
                              'purpose': t['purpose'], 'start_year': sy or '', 'end_year': ey or '',
                              'precision': pr, 'evidence': t['evidence'], 'notes': t['notes'],
                              'rationale': cls('TRAVELS', t['travel_id']).get('rationale', '')},
    })

for t in TRAVELS:
    scope = norm_scope(cls('TRAVELS', t['travel_id']).get('scope', 'KEEP'))
    travel_mark(t, scope)

# ---------------------------------------------------------------- texts
def text_mark(tx, scope):
    date = tx['date']
    if not (date and date[:4].isdigit()):
        unplaced_add({'id': tx['text_id'], 'label': tx['title'], 'reason': 'no date in frozen record',
                      'legendary': False, 'scope': scope, 'note': ''})
        return
    add({
        'id': tx['text_id'], 'lane': 'texts', 'kind': 'text', 'start': int(date[:4]), 'end': int(date[:4]),
        'precision': 'YEAR', 'label': tx['title'], 'sub': tx['text_type'],
        'confidence': tx['confidence'], 'status': 'VERIFIED', 'legendary': False,
        'direction': '', 'tradition': '', 'connection_types': 'TEXTUAL_TRANSMISSION',
        'band': band_of('TEXTS', tx['text_id']), 'scope': scope,
        'single_source': False, 'source_count': 0, 'sources': [],
        'ticks': [], 'card': {'text_id': tx['text_id'], 'title': tx['title'],
                              'author': PERSON.get(tx['author_person_id'], {}).get('full_name', '') or '',
                              'language': tx['language'], 'date': date, 'text_type': tx['text_type'],
                              'india_relevance': tx['india_relevance'], 'korea_relevance': tx['korea_relevance'],
                              'translation_info': tx['translation_info'], 'notes': tx['notes'],
                              'rationale': cls('TEXTS', tx['text_id']).get('rationale', '')},
    })
    # translation markers (validated translation_dates table)
    for l in PTX:
        if l['text_id'] == tx['text_id'] and l['link_type'] == 'TRANSLATOR':
            td = TRANS_DATES.get(l['link_id'], {})
            if td.get('year'):
                add({
                    'id': f"{l['link_id']}@tr", 'lane': 'texts', 'kind': 'translation',
                    'start': int(td['year']), 'end': int(td['year']), 'precision': 'YEAR',
                    'label': f"Translation: {PERSON.get(l['person_id'], {}).get('full_name', '')} — {tx['title']}",
                    'sub': 'TRANSLATOR', 'confidence': l['confidence'], 'status': 'VERIFIED',
                    'legendary': False, 'direction': '', 'tradition': '', 'connection_types': 'TEXTUAL_TRANSMISSION',
                    'band': band_of('TEXTS', tx['text_id']), 'scope': scope,
                    'single_source': False, 'source_count': 0, 'sources': [],
                    'ticks': [], 'card': {'link': l['link_id'], 'translator': PERSON.get(l['person_id'], {}).get('full_name', ''),
                                          'text': tx['title'], 'year': td['year'], 'note': td.get('note', '')},
                })

for tx in TEXTS:
    text_mark(tx, norm_scope(cls('TEXTS', tx['text_id']).get('scope', 'KEEP')))

# ---------------------------------------------------------------- institutions
def inst_mark(i, scope):
    fy = i['founded_year']
    if not fy or not str(fy).lstrip('-').isdigit():
        unplaced_add({'id': i['institution_id'], 'label': i['name'], 'reason': 'no founded_year in frozen record',
                      'legendary': False, 'scope': scope, 'note': ''})
        return
    fy = int(fy)
    band = band_of('INSTITUTIONS', i['institution_id'])
    band_end = next((b['end'] for b in BANDS if b['id'] == band), 2027)
    add({
        'id': i['institution_id'], 'lane': 'institutions', 'kind': 'institution',
        'start': fy, 'end': max(fy, band_end - 1),
        'precision': 'APPROX', 'label': i['name'], 'sub': i['institution_type'],
        'confidence': 'MEDIUM', 'status': 'VERIFIED', 'legendary': False,
        'direction': '', 'tradition': '', 'connection_types': 'INSTITUTIONAL',
        'band': band, 'scope': scope,
        'single_source': False, 'source_count': 0, 'sources': [],
        'ticks': [], 'card': {'institution_id': i['institution_id'], 'name': i['name'],
                              'founded_year': i['founded_year'], 'type': i['institution_type'],
                              'location': PLACE.get(i['location_place_id'], {}).get('place_name', ''),
                              'india_relevance': i['india_relevance'], 'korea_relevance': i['korea_relevance'],
                              'notes': i['notes'], 'rationale': cls('INSTITUTIONS', i['institution_id']).get('rationale', '')},
    })

for i in INSTS:
    inst_mark(i, norm_scope(cls('INSTITUTIONS', i['institution_id']).get('scope', 'KEEP')))

# ---------------------------------------------------------------- events
for e in EVENTS:
    sd, ed = e['start_date'], e['end_date'] or e['start_date']
    sy = int(sd[:4]) if sd[:4].isdigit() else None
    ey = int(ed[:4]) if ed[:4].isdigit() else sy
    if sy is None:
        unplaced_add({'id': e['event_id'], 'label': e['title'], 'reason': 'no start date in frozen record',
                      'legendary': False, 'scope': 'KEEP', 'note': ''})
        continue
    ss = srcs_of(e)
    add({
        'id': e['event_id'], 'lane': 'events', 'kind': 'event',
        'start': sy, 'end': ey, 'precision': 'YEAR',
        'label': e['title'], 'sub': e['event_type'],
        'confidence': e['confidence'], 'status': e['status'], 'legendary': False,
        'direction': '', 'tradition': '', 'connection_types': 'EVENT',
        'band': band_of('EVENTS', e['event_id']), 'scope': norm_scope(cls('EVENTS', e['event_id']).get('scope', 'KEEP')),
        'single_source': len(ss) == 1, 'source_count': len(ss), 'sources': ss,
        'ticks': [], 'card': {'event_id': e['event_id'], 'title': e['title'], 'event_type': e['event_type'],
                              'start_date': e['start_date'], 'end_date': e['end_date'],
                              'location': PLACE.get(e['location_place_id'], {}).get('place_name', ''),
                              'description': e['description'], 'significance': e['significance'],
                              'evidence': e['evidence'],
                              'rationale': cls('EVENTS', e['event_id']).get('rationale', '')},
    })

# ---------------------------------------------------------------- encounters (lane 6)
for r in RELS:
    if r['relationship_kind'] not in ('MET_IN_PERSON', 'TEACHER_STUDENT'):
        continue
    if r['relationship_id'] not in ENCOUNTER_YEARS:
        continue  # undated encounter → not placed (no invented dates)
    year, quote = ENCOUNTER_YEARS[r['relationship_id']]
    a, b = PERSON.get(r['person_a_id'], {}), PERSON.get(r['person_b_id'], {})
    in_pop = r['person_a_id'] in carried_people and r['person_b_id'] in carried_people
    scope = 'CARRIED' if in_pop else 'CONTEXT'
    add({
        'id': r['relationship_id'], 'lane': 'encounters', 'kind': 'encounter',
        'start': year, 'end': year, 'precision': 'YEAR',
        'label': f"{a.get('full_name','')} ⇄ {b.get('full_name','')}",
        'sub': r['relationship_kind'], 'confidence': r['confidence'], 'status': 'VERIFIED',
        'legendary': False, 'direction': '', 'tradition': '', 'connection_types': 'PERSON_ENCOUNTER',
        'band': band_of('PEOPLE', r['person_a_id']) or band_of('PEOPLE', r['person_b_id']),
        'scope': scope, 'single_source': False, 'source_count': 0, 'sources': [],
        'ticks': [], 'card': {'relationship_id': r['relationship_id'], 'kind': r['relationship_kind'],
                              'type': r['relationship_type'], 'person_a': a.get('full_name', ''),
                              'person_b': b.get('full_name', ''), 'evidence': r['evidence'],
                              'year_source': quote, 'notes': r['notes']},
    })

# ---------------------------------------------------------------- negatives (lane 8)
for n in NEGATIVES:
    add({'id': n['id'], 'lane': 'negatives', 'kind': 'negative', 'start': n['year'], 'end': n['year'],
         'precision': 'YEAR', 'label': n['label'], 'sub': 'documented negative', 'confidence': 'HIGH',
         'status': 'VERIFIED', 'legendary': False, 'direction': '', 'tradition': '',
         'connection_types': 'NEGATIVE', 'band': '', 'scope': 'CONTEXT',
         'single_source': False, 'source_count': 0, 'sources': n['sources'],
         'ticks': [], 'card': {'id': n['id'], 'label': n['label'], 'detail': n['detail']}})

# ---------------------------------------------------------------- ribbons
# Record density per decade: explicit dates only (derived table).
rec_density = {}
for r in D('density_by_decade.csv'):
    dec = r['decade'].replace('s', '')
    rec_density.setdefault(int(dec), 0)
    rec_density[int(dec)] += int(r['count'])
# Source density per decade: distinct source_ids on dated carried people (birth year) + events.
src_density = {}
for pid in carried_people:
    p = PERSON[pid]
    if p['birth_year']:
        d = int(int(p['birth_year']) / 10) * 10
        for s in srcs_of(p):
            src_density.setdefault(d, set()).add(s)
for e in EVENTS:
    if cls('EVENTS', e['event_id']).get('scope') in ('KEEP', 'ADAPT') and e['start_date'][:4].isdigit():
        d = int(int(e['start_date'][:4]) / 10) * 10
        for s in srcs_of(e):
            src_density.setdefault(d, set()).add(s)
src_density = {d: len(v) for d, v in src_density.items()}

# ---------------------------------------------------------------- emit
meta = {
    'generated': '2026-08-17',
    'title': 'Buddhist Bridges — India–Korea Buddhist Connections: Interactive Timeline (MVP)',
    'axis': {'start': 300, 'end': 2027},
    'frozen_baseline': 'v3.0_frozen (SHA-256 manifest in VERSION.md)',
    'basis': 'Frozen V3.0 + validated derived tables (analysis/data) + prosopography outputs. '
             'Explicit dates only; APPROX ranges are visually fuzzy; undated records are unplaced, never dated.',
    'gaps': [
        {'label': 'B3 Joseon (1392–1900): no carried records under current inclusion criteria',
         'start': 1392, 'end': 1900,
         'note': '11 classified rows exist (P-0025/26/27, PL-0006, TX-0004/05/06, L-0014, L-0104/05/06), all EXCLUDE. '
                 'This is a finding about the dataset, not a claim of zero Buddhist activity.'},
        {'label': 'No documented events 1370 → 1981', 'start': 1370, 'end': 1981,
         'note': 'EV-0017 (relic enshrinement 1370) is the last event before EV-0015 (1981 delegation).'},
    ],
}
data = {
    'meta': meta, 'bands': BANDS,
    'marks': marks, 'unplaced': unplaced,
    'ribbons': {'record_density': rec_density, 'source_density': src_density,
                'basis': 'record_density: carried records with explicit dates per decade (density_by_decade.csv); '
                         'source_density: distinct source_ids on dated carried people+events per decade (people/events only carry source_ids in V3.0)'},
    'sources': SRC_LABEL,
    'lane_order': ['people', 'travels', 'texts', 'institutions', 'events', 'encounters', 'context', 'negatives'],
}
out = os.path.join(DATA, 'timeline_data.json')
with open(out, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print(f"  wrote timeline_data.json ({len(marks)} marks, {len(unplaced)} unplaced)")

# ---------------------------------------------------------------- HTML template
TPL = os.path.join(ROOT, 'timeline_mvp_template.html')
with open(TPL, encoding='utf-8') as f:
    html = f.read()
html = html.replace('/*__TIMELINE_DATA__*/', json.dumps(data, ensure_ascii=False))
out_html = os.path.join(ROOT, 'timeline_mvp.html')
with open(out_html, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"  wrote timeline_mvp.html ({len(html)//1024} KiB)")
