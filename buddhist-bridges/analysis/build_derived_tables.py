#!/usr/bin/env python3
"""
Buddhist Bridges — Phase 2, Step 1: Data-Preparation Layer (blueprint §7)

Builds all derived tables from the FROZEN V3.0 dataset (read-only) into
buddhist-bridges/analysis/data/. Never modifies the frozen data.

Derived tables:
  1. region_centroids.csv        — 9 non-point places
  2. person_floruits.csv         — 20 carried people without birth years
  3. travel_date_ranges.csv      — 14 undated travels
  4. tradition_taxonomy.csv      — 43 carried people, multi-affiliation allowed
  5. institution_mapping.csv     — 43 carried people, institution_org -> I-####
  6. translation_dates.csv       — 6 PTX TRANSLATOR links
  7. event_end_dates.csv         — verification: all 19 events already carry end dates
  8. density_by_decade.csv + source_mix_by_band.csv

Rules: never invent dates/coordinates; every derived value carries provenance,
precision, and confidence; historical event dates are never conflated with
evidence/source dates.
"""
import csv, os, sys, collections

ROOT = os.path.dirname(os.path.abspath(__file__))          # .../buddhist-bridges/analysis
FROZEN = os.path.join(ROOT, '..', 'v3.0_frozen')           # frozen V3.0
OUT = os.path.join(ROOT, 'data')
os.makedirs(OUT, exist_ok=True)

def load(name):
    with open(os.path.join(FROZEN, name), encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

PEOPLE = load('people.csv')
PLACES = load('places.csv')
TRAVELS = load('travels.csv')
TEXTS = load('texts.csv')
INSTS = load('institutions.csv')
RELS = load('person_person.csv')
PPL = load('person_place.csv')
PTX = load('person_text.csv')
EVENTS = load('events.csv')
SOURCES = load('sources.csv')
CLS = load('classification_v3.csv')

CARRIED = {c['record_id'] for c in CLS if c['scope'] in ('KEEP', 'ADAPT')}
CARRIED_PEOPLE = {c['record_id'] for c in CLS if c['scope'] in ('KEEP', 'ADAPT') and c['table'] == 'PEOPLE'}
PERSON = {p['person_id']: p for p in PEOPLE}
PLACE = {p['place_id']: p for p in PLACES}
TEXT = {t['text_id']: t for t in TEXTS}
INST = {i['institution_id']: i for i in INSTS}
SRC_TYPE = {s['source_id']: s['source_type'] for s in SOURCES}

BAND_RANGE = {
    'B1': (0, 900), 'B2': (900, 1392), 'B3': (1392, 1900),
    'B4': (1900, 1945), 'B5': (1945, 1990), 'B6': (1990, 2027),
}
def band_of(period_band):
    for b in BAND_RANGE:
        if period_band.startswith(b):
            return b
    return None

def write(name, rows, fields):
    with open(os.path.join(OUT, name), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: (r.get(k) if r.get(k) is not None else '') for k in fields})
    print(f"  wrote {name} ({len(rows)} rows)")

PROV = "Derived 2026-08-17 from frozen V3.0 (read-only) by build_derived_tables.py; no new historical research."

# =====================================================================
# 1. REGION CENTROIDS — 9 non-point places
#    Basis: standard geographic knowledge of historical capitals/regions.
#    All are REGION_CENTROID approximations, never precise site points.
# =====================================================================
CENTROIDS = [
    # place_id, name, lat, lon, radius_km, basis
    ('PL-0001', 'Korea (Silla)', 35.856, 129.224, 100, 'Historical capital Seorabeol (Gyeongju), 57 BCE-935 CE'),
    ('PL-0002', 'Korea (Baekje)', 36.282, 126.913, 100, 'Final capital Sabi (Buyeo), 538-660 CE'),
    ('PL-0004', 'Korea (Goguryeo)', 39.031, 125.754, 150, 'Capital Pyongyang, 427-668 CE'),
    ('PL-0005', 'Korea (Goryeo)', 37.971, 126.564, 100, 'Capital Gaegyeong (Kaesong), 919-1392'),
    ('PL-0006', 'Korea (Joseon)', 37.566, 126.978, 100, 'Capital Hanseong (Seoul), 1394-1910'),
    ('PL-0008', 'India (Gandhara)', 33.746, 72.839, 150, 'Core region Taxila-Peshawar (Gandhara)'),
    ('PL-0012', 'India (Central India / Sangana)', 23.170, 79.940, 250, 'Central India region; exact site of Sangana unknown (data place_type=MONASTERY but it is a region)'),
    ('PL-0019', 'Central Asia (Serindia/Western Regions)', 38.500, 84.500, 400, 'Tarim Basin (Serindia) region centroid'),
    ('PL-0031', 'India (unspecified)', 22.500, 79.000, 600, 'National centroid of India (unspecified location)'),
]
rows = []
for pid, name, lat, lon, r, basis in CENTROIDS:
    rows.append({
        'place_id': pid, 'place_name': name, 'modern_country': PLACE[pid]['modern_country'],
        'place_type': PLACE[pid]['place_type'], 'centroid_lat': lat, 'centroid_lon': lon,
        'geometry_type': 'REGION_CENTROID', 'uncertainty_radius_km': r,
        'precision': 'APPROX', 'confidence': 'MEDIUM',
        'basis': basis, 'provenance': PROV,
        'notes': 'Approximate centroid for cartographic anchoring only; not a precise site point. Do not use for distance measurements below the uncertainty radius.',
    })
write('region_centroids.csv', rows, ['place_id', 'place_name', 'modern_country', 'place_type', 'centroid_lat', 'centroid_lon', 'geometry_type', 'uncertainty_radius_km', 'precision', 'confidence', 'basis', 'provenance', 'notes'])

# =====================================================================
# 2. PERSON FLORUITS — 20 carried people without birth years
#    Basis: dated activities documented in the frozen records (reigns,
#    journeys, degrees, publications). Floruit = documented activity window.
# =====================================================================
FLORUITS = [
    # person_id, start, end, precision, basis, confidence, notes
    ('P-0004', 681, 692, 'APPROX', 'Reign of King Sinmun (681-692) per record notes ("lived during King Sinmun\'s reign")', 'MEDIUM', 'Ordained at 18; exact dates unrecorded'),
    ('P-0005', 742, 765, 'APPROX', 'Reign of King Gyeongdeok (742-765) per record notes (tradition)', 'MEDIUM', 'Some scholars date him later'),
    ('P-0006', 384, 384, 'APPROX', 'Documented arrival in Baekje 384 CE (Samguk Sagi)', 'MEDIUM', 'Single documented date'),
    ('P-0010', 705, 774, 'APPROX', 'Disciple of Amoghavajra (705-774) per record', 'MEDIUM', '8th-century Silla esoteric monk'),
    ('P-0011', 526, 531, 'APPROX', 'Documented: departed for India 526 (Seongwang 4), returned 531', 'MEDIUM', 'Dates from Korean Buddhist tradition (later compilations)'),
    ('P-0012', 531, 531, 'APPROX', 'Documented: accompanied Gyeomik to Baekje 531', 'MEDIUM', 'Single documented date'),
    ('P-0013', 671, 695, 'APPROX', 'Recorded by Yijing, who visited India 671-695', 'MEDIUM', 'Died at Nalanda aged 70+'),
    ('P-0014', 671, 695, 'APPROX', 'Yijing era (671-695); manuscripts seen at Nalanda by Yijing\'s party', 'MEDIUM', 'Died in India aged ~60'),
    ('P-0015', 671, 695, 'APPROX', 'Yijing era (671-695)', 'MEDIUM', 'Died in China'),
    ('P-0016', 627, 649, 'APPROX', 'Zhenguan era (627-649) per record ("accompanied Xuanzhao in the Zhenguan era")', 'MEDIUM', 'Died at Bodhgaya in his 40s'),
    ('P-0017', 671, 695, 'APPROX', 'Yijing era (671-695); recorded with the Silla contingent in Yijing', 'MEDIUM', ''),
    ('P-0018', 671, 695, 'APPROX', 'Yijing era (671-695); included in Yijing\'s Da Tang Xiyu qiufa gaoseng zhuan', 'MEDIUM', 'Silla vs Koguryo identity debated'),
    ('P-0020', 785, 798, 'APPROX', 'Went to Tang with Hyeil c. 789, King Wonseong era (785-798)', 'MEDIUM', 'Died in Tibet'),
    ('P-0021', 742, 765, 'APPROX', 'King Gyeongdeok era (742-765) per record', 'MEDIUM', 'Died in China'),
    ('P-0022', 671, 695, 'APPROX', 'Yijing era (671-695); followed Chinese monk Sengche', 'MEDIUM', 'Ordained in Sri Lanka; South Asian not mainland-India connection'),
    ('P-0054', 1980, 1991, 'APPROX', 'Documented degrees: MA 1980, PhD 1991 (Dongguk) per institution_org field', 'HIGH', 'Career scholar of Indian philosophy; NOT India-trained. Documented window (1980-1991) crosses the B6 boundary (1990-2026): band = India-exchange activity, floruit = documented activity; overlap is expected, not an error'),
    ('P-0055', 2001, 2019, 'APPROX', 'Documented: MA c. 2001 (Delhi), article 2019-03-19', 'HIGH', 'Residence in Delhi documented; exact years approximate'),
    ('P-0062', 2026, 2026, 'APPROX', 'Documented activity: MOU 2026-04-23; Beopbo 2026-07-08', 'MEDIUM', 'Long-term Bodh Gaya residence documented but undated; floruit = documented activity window only'),
    ('P-0064', 2005, 2015, 'APPROX', 'Documented: 5+ years in India; PhD completion 2010 (newer source 2022 says "수료")', 'HIGH', 'Discrepancy between sources noted in record'),
    ('P-0073', 1962, 1963, 'APPROX', 'Documented survey journey 1962-01-21 to 1963-05-09', 'HIGH', 'Career spans decades; floruit = documented India activity window'),
]
rows = []
for pid, s, e, prec, basis, conf, note in FLORUITS:
    p = PERSON[pid]
    rows.append({
        'person_id': pid, 'full_name': p['full_name'], 'period': p['period'],
        'birth_year': p['birth_year'] or '', 'death_year': p['death_year'] or '',
        'floruit_start': s, 'floruit_end': e, 'precision': prec,
        'confidence': conf, 'basis': basis, 'provenance': PROV, 'notes': note,
    })
write('person_floruits.csv', rows, ['person_id', 'full_name', 'period', 'birth_year', 'death_year', 'floruit_start', 'floruit_end', 'precision', 'confidence', 'basis', 'provenance', 'notes'])

# =====================================================================
# 3. TRAVEL DATE RANGES — 14 undated travels
#    Basis: person floruit (table 2) where derivable; NULL where the frozen
#    data contains no dated activity (never invented).
# =====================================================================
FLORUIT = {r['person_id']: r for r in rows}
TRAVEL_RANGES = [
    # travel_id, start, end, confidence, basis, notes
    ('T-0005', 671, 695, 'MEDIUM', 'Person floruit P-0013 (Yijing era)', ''),
    ('T-0006', 671, 695, 'MEDIUM', 'Person floruit P-0014 (Yijing era)', ''),
    ('T-0007', 671, 695, 'MEDIUM', 'Person floruit P-0015 (Yijing era)', ''),
    ('T-0008', 627, 649, 'MEDIUM', 'Person floruit P-0016 (Zhenguan era)', ''),
    ('T-0009', 671, 695, 'MEDIUM', 'Person floruit P-0017 (Yijing era)', ''),
    ('T-0012', 671, 695, 'MEDIUM', 'Person floruit P-0022 (Yijing era)', ''),
    ('T-0029', 2010, 2010, 'LOW', 'Person\'s only documented activity: Tamas translation dated 2010 (TX-0025)', 'Travel date itself undocumented; weak anchor'),
    ('T-0030', None, None, 'LOW', 'No dated activity in frozen record', 'UNDOCUMENTED — cannot be derived from frozen data'),
    ('T-0032', 2000, 2015, 'MEDIUM', 'Person floruit P-0061 ("built the Korean language program at JNU since 2000"; engagements incl. 2015)', ''),
    ('T-0033', 2026, 2026, 'MEDIUM', 'Person floruit P-0062 (documented activity 2026)', 'Residence start undocumented'),
    ('T-0034', None, None, 'LOW', 'No dated activity in frozen record (born 1970 only)', 'UNDOCUMENTED — cannot be derived from frozen data'),
    ('T-0035', 2005, 2015, 'MEDIUM', 'Person floruit P-0064 (5+ years in India; PhD 2010)', ''),
    ('T-0039', 671, 695, 'MEDIUM', 'Person floruit P-0018 (Yijing era)', ''),
    ('T-0041', None, None, 'LOW', 'No dated activity in frozen record', 'UNDOCUMENTED — cannot be derived from frozen data'),
]
rows = []
SCOPE = {c['record_id']: c['scope'] for c in CLS if c['table'] == 'TRAVELS'}
for tid, s, e, conf, basis, note in TRAVEL_RANGES:
    t = next(x for x in TRAVELS if x['travel_id'] == tid)
    p = PERSON[t['person_id']]
    rows.append({
        'travel_id': tid, 'person_id': t['person_id'], 'person_name': p['full_name'],
        'origin_place_id': t['origin_place_id'], 'destination_place_id': t['destination_place_id'],
        'scope': SCOPE.get(tid, ''),
        'range_start': s if s else '', 'range_end': e if e else '',
        'precision': 'APPROX' if s else 'UNDOCUMENTED',
        'confidence': conf, 'basis': basis, 'provenance': PROV, 'notes': note,
    })
write('travel_date_ranges.csv', rows, ['travel_id', 'person_id', 'person_name', 'origin_place_id', 'destination_place_id', 'scope', 'range_start', 'range_end', 'precision', 'confidence', 'basis', 'provenance', 'notes'])

# =====================================================================
# 4. TRADITION TAXONOMY — 43 carried people (multi-affiliation allowed)
#    Categories: SEON_CHAN, ESOTERIC, YOGACARA, VINAYA, HWA_EOM, PURE_LAND,
#    GENERAL_BUDDHISM, LAY_BUDDHIST, NON_BUDDHIST, THERAVADA_ORIENTED, UNKNOWN
# =====================================================================
TAXONOMY = {
    # person_id: (t1, t2, t3, basis, notes)
    'P-0001': ('ESOTERIC', '', '', 'Raw: "Buddhism (Esoteric/Vajrayana; disciple of Vajrabodhi and Amoghavajra)"', ''),
    'P-0002': ('YOGACARA', '', '', 'Raw: "Buddhism (East Asian Yogacara/Cittamatra)"', ''),
    'P-0003': ('HWA_EOM', 'GENERAL_BUDDHISM', '', 'Raw: "Buddhism (Hwaeom/Huayan and broader Mahayana)"', 'Multi-affiliation: Hwaeom + broader Mahayana'),
    'P-0004': ('PURE_LAND', '', '', 'Raw: "Buddhism (specialized in Pure Land/Amitabha commentary)"', ''),
    'P-0005': ('YOGACARA', '', '', 'Raw: "Buddhism (Yogacara; later revered as founder of Goryeo Yugajong)"', ''),
    'P-0006': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0009': ('SEON_CHAN', '', '', 'Raw: "Buddhism (Seon)"', ''),
    'P-0010': ('ESOTERIC', '', '', 'Raw: "Buddhism (Esoteric/Vajrayana); disciple of Amoghavajra (705-774)"', ''),
    'P-0011': ('VINAYA', '', '', 'Raw: "Buddhism (Vinaya)"', ''),
    'P-0012': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0013': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0014': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0015': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0016': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0017': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0018': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0020': ('ESOTERIC', '', '', 'Raw: "Buddhism (Esoteric)"', ''),
    'P-0021': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0022': ('GENERAL_BUDDHISM', '', '', 'Raw: "Buddhism" (unspecified)', ''),
    'P-0023': ('SEON_CHAN', '', '', 'Raw: "Buddhism (Chan/Seon transmission)"', ''),
    'P-0024': ('SEON_CHAN', '', '', 'Raw: "Buddhism (Seon)"', ''),
    'P-0028': ('NON_BUDDHIST', '', '', 'Raw: "None (studied all religions comparatively)"', 'Scholar of religions incl. Buddhism; not a Buddhist practitioner per record'),
    'P-0029': ('NON_BUDDHIST', '', '', 'Raw: "None (wrote on Buddhism as national culture)"', 'Wrote on Buddhism as national culture; not a practitioner per record'),
    'P-0030': ('NON_BUDDHIST', '', '', 'Raw: "Brahmoism-influenced Hindu humanist universalism"', 'Hindu/Brahmo'),
    'P-0034': ('SEON_CHAN', '', '', 'Raw: "Buddhism (Seon; colonial-era reform)"', ''),
    'P-0038': ('NON_BUDDHIST', '', '', 'Raw: "Hindu (Vaishnava with Jain influences); secularist in politics"', 'Hindu'),
    'P-0051': ('SEON_CHAN', '', '', 'Raw: "Buddhism (ordained monk 1952-1962)"', 'Ordained 1952-1962; later left monastic life'),
    'P-0052': ('SEON_CHAN', '', '', 'Raw: "Buddhism (Korean Seon; Songgwangsa lineage)"', ''),
    'P-0053': ('LAY_BUDDHIST', '', '', 'Raw: "Buddhist-heritage scholarship (Buddhism specialist)"', 'Scholar, not monk'),
    'P-0054': ('UNKNOWN', '', '', 'Raw: NULL', 'No affiliation recorded'),
    'P-0055': ('LAY_BUDDHIST', '', '', 'Raw: "Buddhism (lay scholar)"', ''),
    'P-0062': ('SEON_CHAN', 'THERAVADA_ORIENTED', '', 'Raw: "Buddhism (Korean Jogye Order; Theravada-oriented early-Buddhist meditation)"', 'Multi-affiliation: Jogye Seon + Theravada-oriented meditation'),
    'P-0063': ('SEON_CHAN', '', '', 'Raw: "Buddhism (Jogye Order bhikkhuni)"', ''),
    'P-0064': ('SEON_CHAN', '', '', 'Raw: "Buddhism (Jogye Order bhikkhuni; trained at Bongnyeongsa)"', ''),
    'P-0065': ('SEON_CHAN', '', '', 'Raw: "Buddhism (Jogye Order)"', ''),
    'P-0068': ('LAY_BUDDHIST', '', '', 'Raw: "Buddhism (studied at Gaewunsa; Dongguk Buddhist college)"', 'Poet; studied Buddhism; not ordained'),
    'P-0071': ('NON_BUDDHIST', '', '', 'Raw: "Hindu (Gandhian)"', 'Hindu'),
    'P-0072': ('SEON_CHAN', '', '', 'Raw: "Buddhism (ordained 1918 at Beopjusa; studied under Nampa and Paek Ch\'owŏl sunims)"', ''),
    'P-0073': ('LAY_BUDDHIST', '', '', 'Raw: "Buddhist scholar (lay)"', ''),
    'P-0074': ('SEON_CHAN', '', '', 'Raw: "Seon Buddhist monk"', ''),
    'P-0075': ('SEON_CHAN', '', '', 'Raw: "Seon Buddhist monk"', ''),
    'P-0076': ('NON_BUDDHIST', '', '', 'Raw: "Hindu"', ''),
    'P-0077': ('SEON_CHAN', '', '', 'Raw: "Seon Buddhist monk"', ''),
}
CATS = ['SEON_CHAN', 'ESOTERIC', 'YOGACARA', 'VINAYA', 'HWA_EOM', 'PURE_LAND', 'GENERAL_BUDDHISM', 'LAY_BUDDHIST', 'NON_BUDDHIST', 'THERAVADA_ORIENTED', 'UNKNOWN']
rows = []
for pid in sorted(CARRIED_PEOPLE):
    p = PERSON[pid]
    t1, t2, t3, basis, note = TAXONOMY[pid]
    rows.append({
        'person_id': pid, 'full_name': p['full_name'],
        'raw_affiliation': p['religious_affiliation'] or '',
        'tradition_1': t1, 'tradition_2': t2, 'tradition_3': t3,
        'mapping_basis': basis, 'confidence': 'HIGH',
        'provenance': PROV, 'notes': note,
    })
write('tradition_taxonomy.csv', rows, ['person_id', 'full_name', 'raw_affiliation', 'tradition_1', 'tradition_2', 'tradition_3', 'mapping_basis', 'confidence', 'provenance', 'notes'])

# =====================================================================
# 5. INSTITUTION MAPPING — 43 carried people, institution_org -> I-####
#    MAPPED = all institutions in the value exist in institutions.csv
#    PARTIAL = some exist, some do not   UNMAPPED = none exist
#    NO_INSTITUTION = field empty/"-"/NULL
# =====================================================================
INST_MAP = {
    'P-0013': ('I-0002', 'MAPPED', 'Nalanda Mahavihara'),
    'P-0014': ('I-0002', 'PARTIAL', 'Nalanda mapped; "Bodhi temple (Bodhgaya)" not in institutions.csv'),
    'P-0023': ('I-0002;I-0003', 'MAPPED', 'Ordained at Nalanda; founded Hoeamsa 1328'),
    'P-0030': ('I-0004', 'MAPPED', 'Visva-Bharati (Santiniketan)'),
    'P-0052': ('I-0020', 'MAPPED', 'Songgwangsa lineage'),
    'P-0054': ('I-0010', 'MAPPED', 'Dongguk University (MA 1980, PhD 1991)'),
    'P-0055': ('I-0010', 'MAPPED', 'Dongguk University Gyeongju campus -> I-0010 (note: campus)'),
    'P-0062': ('I-0015;I-0014', 'MAPPED', 'Bunhwangsa India; Bodh Gaya International College of Buddhist Studies'),
    'P-0063': ('I-0021', 'PARTIAL', 'Bongnyeongsa mapped; "Seoul Beopryongsa bhikkhuni hall" not in institutions.csv'),
    'P-0064': ('I-0016', 'PARTIAL', 'Mahayeon Temple Food Culture Center mapped; "Bongwonsa" not in institutions.csv'),
    'P-0068': ('I-0010', 'MAPPED', 'Dongguk University (professor)'),
    'P-0073': ('I-0010', 'MAPPED', 'Dongguk University'),
    'P-0074': ('I-0003', 'MAPPED', 'Hoeamsa'),
}
rows = []
for pid in sorted(CARRIED_PEOPLE):
    p = PERSON[pid]
    raw = (p['institution_org'] or '').strip()
    if pid in INST_MAP:
        ids, status, note = INST_MAP[pid]
    elif raw in ('', '-', 'NULL'):
        ids, status, note = '', 'NO_INSTITUTION', 'No institution recorded in frozen data'
    else:
        ids, status, note = '', 'UNMAPPED', 'Institution(s) not present in institutions.csv; keep as free-text node'
    rows.append({
        'person_id': pid, 'full_name': p['full_name'],
        'raw_institution_org': raw, 'mapped_institution_ids': ids,
        'mapping_status': status, 'basis': note,
        'confidence': 'HIGH' if status in ('MAPPED', 'NO_INSTITUTION') else 'MEDIUM',
        'provenance': PROV, 'notes': '',
    })
write('institution_mapping.csv', rows, ['person_id', 'full_name', 'raw_institution_org', 'mapped_institution_ids', 'mapping_status', 'basis', 'confidence', 'provenance', 'notes'])

# =====================================================================
# 6. TRANSLATION DATES — 6 PTX TRANSLATOR links
#    Basis: texts.csv date field (the translation record's own date).
#    Historical event dates only; evidence dates noted separately.
# =====================================================================
rows = []
for l in PTX:
    if l['link_type'] == 'TRANSLATOR':
        t = TEXT[l['text_id']]
        note = ''
        if l['link_id'] == 'L-0113':
            note = ("DISCREPANCY: L-0113 evidence note says 1921, but TX-0013 date=1923 and P-0032 notes "
                    "document March 1923 (Choi Dong-ho) vs April 1923 (Jeong Ji-yong Literary Museum). "
                    "Derived date follows the text record (1923).")
        rows.append({
            'link_id': l['link_id'], 'person_id': l['person_id'],
            'person_name': PERSON[l['person_id']]['full_name'],
            'text_id': l['text_id'], 'text_title': t['title'],
            'translation_date': t['date'], 'precision': 'YEAR',
            'confidence': 'HIGH', 'basis': 'texts.csv date field (the translation record)',
            'provenance': PROV, 'notes': note,
        })
write('translation_dates.csv', rows, ['link_id', 'person_id', 'person_name', 'text_id', 'text_title', 'translation_date', 'precision', 'confidence', 'basis', 'provenance', 'notes'])

# =====================================================================
# 7. EVENT END DATES — verification table
#    Finding: all 19 events already carry end dates in the frozen data;
#    blueprint §7 item 7 requires no derivation.
# =====================================================================
rows = []
for e in EVENTS:
    rows.append({
        'event_id': e['event_id'], 'title': e['title'],
        'start_date': e['start_date'], 'end_date': e['end_date'],
        'status': 'ALREADY_PRESENT',
        'basis': 'frozen events.csv end_date field; no derivation needed',
        'provenance': PROV, 'notes': '',
    })
write('event_end_dates.csv', rows, ['event_id', 'title', 'start_date', 'end_date', 'status', 'basis', 'provenance', 'notes'])

# =====================================================================
# 8a. DENSITY BY DECADE — dated carried records only (explicit dates)
#     Undated records counted separately; never imputed into decades.
# =====================================================================
def decade(y):
    return (int(y) // 10) * 10

density = collections.Counter()
undated = collections.Counter()
for c in CLS:
    if c['scope'] not in ('KEEP', 'ADAPT'):
        continue
    rid, table = c['record_id'], c['table']
    y = None
    if table == 'PEOPLE' and PERSON[rid]['birth_year']:
        y = PERSON[rid]['birth_year']
    elif table == 'TRAVELS' and next((t for t in TRAVELS if t['travel_id'] == rid), None) and \
            next(t for t in TRAVELS if t['travel_id'] == rid)['travel_start_year']:
        y = next(t for t in TRAVELS if t['travel_id'] == rid)['travel_start_year']
    elif table == 'TEXTS' and TEXT[rid]['date']:
        y = TEXT[rid]['date'][:4]
    elif table == 'INSTITUTIONS' and INST[rid]['founded_year']:
        y = INST[rid]['founded_year']
    elif table == 'EVENTS' and next((e for e in EVENTS if e['event_id'] == rid), None) and \
            next(e for e in EVENTS if e['event_id'] == rid)['start_date']:
        y = next(e for e in EVENTS if e['event_id'] == rid)['start_date'][:4]
    if y and y.isdigit():
        density[(decade(y), table)] += 1
    else:
        undated[table] += 1

rows = []
for (dec, table), n in sorted(density.items()):
    rows.append({'decade': f"{dec}s", 'entity_type': table, 'count': n,
                 'basis': 'Explicit dates only (birth_year, travel_start_year, text date, founded_year, event start_date)',
                 'provenance': PROV, 'notes': ''})
write('density_by_decade.csv', rows, ['decade', 'entity_type', 'count', 'basis', 'provenance', 'notes'])

rows = []
for table, n in sorted(undated.items()):
    rows.append({'entity_type': table, 'undated_count': n,
                 'basis': 'Carried records without explicit dates (floruits/travel ranges in derived tables 2-3 are APPROX and excluded from decade counts)',
                 'provenance': PROV, 'notes': ''})
write('undated_counts.csv', rows, ['entity_type', 'undated_count', 'basis', 'provenance', 'notes'])

# =====================================================================
# 8b. SOURCE MIX BY BAND — source types cited by carried records per band
#     NOTE: only PEOPLE and EVENTS carry source_ids in the frozen schema;
#     TRAVELS/TEXTS/INSTITUTIONS/RELS/PPL/PTX do not (documented limitation).
# =====================================================================
mix = collections.Counter()
for c in CLS:
    if c['scope'] not in ('KEEP', 'ADAPT'):
        continue
    band = band_of(c['period_band'])
    if not band:
        continue
    rid, table = c['record_id'], c['table']
    srcs = []
    if table == 'PEOPLE':
        srcs = (PERSON[rid]['source_ids'] or '').split(';')
    elif table == 'EVENTS':
        srcs = (next(e for e in EVENTS if e['event_id'] == rid)['source_ids'] or '').split(';')
    for s in srcs:
        s = s.strip()
        if s in SRC_TYPE:
            mix[(band, SRC_TYPE[s])] += 1

rows = []
for (band, stype), n in sorted(mix.items()):
    rows.append({'band': band, 'source_type': stype, 'count': n,
                 'basis': 'source_ids of carried PEOPLE and EVENTS resolved against sources.csv source_type (only tables with source_ids in the frozen schema)',
                 'provenance': PROV, 'notes': ''})
write('source_mix_by_band.csv', rows, ['band', 'source_type', 'count', 'basis', 'provenance', 'notes'])

print("\nAll derived tables written to", OUT)