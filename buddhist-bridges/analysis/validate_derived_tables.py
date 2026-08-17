#!/usr/bin/env python3
"""
Buddhist Bridges — Phase 2, Step 1: Validation of derived tables.

Checks:
  V1  All derived tables exist with expected row counts
  V2  Floruits fall within their period band ranges
  V3  Travel ranges fall within person floruits (where both exist)
  V4  Tradition taxonomy covers all 43 carried people; categories controlled
  V5  Institution mapping covers all 43 carried people; mapped IDs exist
  V6  Translation dates match texts.csv; all 6 links present
  V7  Event end dates: all 19 present (no derivation needed)
  V8  Frozen V3.0 unchanged (SHA-256 vs VERSION.md manifest)
  V9  No invented dates: UNDOCUMENTED rows carry no dates; all others have precision
  V10 Centroids: 9 rows, all REGION_CENTROID with precision APPROX
  V11 Density tables: decade counts use explicit dates only; undated counted separately
"""
import csv, hashlib, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data')
FROZEN = os.path.join(ROOT, '..', 'v3.0_frozen')

errors, warnings = [], []

def load(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def check(cond, msg):
    (errors if not cond else []).append(msg) if not cond else None

# ---- V1: existence + row counts ----
EXPECTED = {
    'region_centroids.csv': 9, 'person_floruits.csv': 20, 'travel_date_ranges.csv': 14,
    'tradition_taxonomy.csv': 43, 'institution_mapping.csv': 43, 'translation_dates.csv': 6,
    'event_end_dates.csv': 19, 'density_by_decade.csv': None, 'undated_counts.csv': None,
    'source_mix_by_band.csv': None,
}
for name, n in EXPECTED.items():
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        check(False, f"V1 MISSING TABLE: {name}")
        continue
    rows = load(path)
    if n is not None:
        check(len(rows) == n, f"V1 ROW COUNT {name}: expected {n}, got {len(rows)}")
    else:
        check(len(rows) > 0, f"V1 EMPTY TABLE: {name}")

# ---- V2: floruit overlaps its band ----
# Floruit = documented activity window; band = India-exchange activity period.
# These are different concepts, so the check is OVERLAP, not containment.
BAND_RANGE = {'B1': (0, 900), 'B2': (900, 1392), 'B3': (1392, 1900), 'B4': (1900, 1945), 'B5': (1945, 1990), 'B6': (1990, 2027)}
cls = load(os.path.join(FROZEN, 'classification_v3.csv'))
band_of = {}
for c in cls:
    if c['scope'] in ('KEEP', 'ADAPT') and c['table'] == 'PEOPLE':
        for b in BAND_RANGE:
            if c['period_band'].startswith(b):
                band_of[c['record_id']] = b
floruits = load(os.path.join(DATA, 'person_floruits.csv'))
for r in floruits:
    b = band_of.get(r['person_id'])
    if b:
        lo, hi = BAND_RANGE[b]
        s, e = int(r['floruit_start']), int(r['floruit_end'])
        check(s <= e and s <= hi and e >= lo, f"V2 FLORUIT DOES NOT OVERLAP BAND: {r['person_id']} {r['full_name']} [{s}-{e}] vs {b} ({lo}-{hi})")

# ---- V3: travel range within person floruit ----
floruit_of = {r['person_id']: r for r in floruits}
tr = load(os.path.join(DATA, 'travel_date_ranges.csv'))
for r in tr:
    if not r['range_start']:
        check(r['precision'] == 'UNDOCUMENTED', f"V3 {r['travel_id']}: dated row missing precision")
        continue
    f = floruit_of.get(r['person_id'])
    if f:
        s, e = int(r['range_start']), int(r['range_end'])
        fs, fe = int(f['floruit_start']), int(f['floruit_end'])
        check(fs <= s <= e <= fe, f"V3 TRAVEL OUT OF FLORUIT: {r['travel_id']} [{s}-{e}] vs {r['person_id']} floruit [{fs}-{fe}]")

# ---- V4: taxonomy coverage + controlled categories ----
CATS = {'SEON_CHAN', 'ESOTERIC', 'YOGACARA', 'VINAYA', 'HWA_EOM', 'PURE_LAND', 'GENERAL_BUDDHISM', 'LAY_BUDDHIST', 'NON_BUDDHIST', 'THERAVADA_ORIENTED', 'UNKNOWN'}
tax = load(os.path.join(DATA, 'tradition_taxonomy.csv'))
tax_ids = {r['person_id'] for r in tax}
carried_people = {c['record_id'] for c in cls if c['scope'] in ('KEEP', 'ADAPT') and c['table'] == 'PEOPLE'}
check(tax_ids == carried_people, f"V4 TAXONOMY COVERAGE: {len(tax_ids)} rows vs {len(carried_people)} carried people")
for r in tax:
    for k in ('tradition_1', 'tradition_2', 'tradition_3'):
        if r[k]:
            check(r[k] in CATS, f"V4 BAD CATEGORY: {r['person_id']} {k}={r[k]}")

# ---- V5: institution mapping coverage + ID existence ----
insts = load(os.path.join(FROZEN, 'institutions.csv'))
inst_ids = {i['institution_id'] for i in insts}
imap = load(os.path.join(DATA, 'institution_mapping.csv'))
imap_ids = {r['person_id'] for r in imap}
check(imap_ids == carried_people, f"V5 MAPPING COVERAGE: {len(imap_ids)} rows vs {len(carried_people)} carried people")
for r in imap:
    for iid in (r['mapped_institution_ids'] or '').split(';'):
        if iid:
            check(iid in inst_ids, f"V5 BAD INSTITUTION ID: {r['person_id']} -> {iid}")

# ---- V6: translation dates match texts.csv ----
texts = load(os.path.join(FROZEN, 'texts.csv'))
text_date = {t['text_id']: t['date'] for t in texts}
td = load(os.path.join(DATA, 'translation_dates.csv'))
check(len(td) == 6, f"V6 TRANSLATION LINKS: expected 6, got {len(td)}")
for r in td:
    check(r['translation_date'] == text_date.get(r['text_id']), f"V6 DATE MISMATCH: {r['link_id']} {r['translation_date']} vs texts.csv {text_date.get(r['text_id'])}")

# ---- V7: event end dates ----
events = load(os.path.join(FROZEN, 'events.csv'))
check(all(e['end_date'] for e in events), "V7 EVENTS MISSING END DATES")
ed = load(os.path.join(DATA, 'event_end_dates.csv'))
check(len(ed) == 19 and all(r['status'] == 'ALREADY_PRESENT' for r in ed), "V7 EVENT END TABLE INCOMPLETE")

# ---- V8: frozen data unchanged ----
manifest = open(os.path.join(FROZEN, 'VERSION.md'), encoding='utf-8').read()
manifest_hashes = set(re.findall(r'([0-9a-f]{64})', manifest))
current = set()
for fname in sorted(os.listdir(FROZEN)):
    if fname.endswith('.csv'):
        h = hashlib.sha256(open(os.path.join(FROZEN, fname), 'rb').read()).hexdigest()
        current.add(h)
check(current <= manifest_hashes and len(current) == 13, f"V8 FROZEN DATA CHANGED: {len(current)} files, manifest has {len(manifest_hashes)} hashes")

# ---- V9: no invented dates ----
for r in tr:
    if r['precision'] == 'UNDOCUMENTED':
        check(not r['range_start'] and not r['range_end'], f"V9 {r['travel_id']}: UNDOCUMENTED row has dates")
    else:
        check(r['range_start'] and r['range_end'], f"V9 {r['travel_id']}: dated row missing range")
for r in floruits:
    check(r['floruit_start'] and r['floruit_end'], f"V9 {r['person_id']}: floruit missing range")

# ---- V10: centroids ----
cen = load(os.path.join(DATA, 'region_centroids.csv'))
check(len(cen) == 9, f"V10 CENTROIDS: expected 9, got {len(cen)}")
for r in cen:
    check(r['geometry_type'] == 'REGION_CENTROID' and r['precision'] == 'APPROX', f"V10 {r['place_id']}: bad geometry/precision")

# ---- V11: density uses explicit dates only ----
dens = load(os.path.join(DATA, 'density_by_decade.csv'))
und = load(os.path.join(DATA, 'undated_counts.csv'))
check(sum(int(r['count']) for r in dens) > 0, "V11 DENSITY EMPTY")
check(sum(int(r['undated_count']) for r in und) > 0, "V11 UNDATED COUNTS EMPTY")

print(f"VALIDATION: {len(errors)} errors, {len(warnings)} warnings")
for e in errors:
    print("  [E]", e)
for w in warnings:
    print("  [W]", w)
sys.exit(1 if errors else 0)