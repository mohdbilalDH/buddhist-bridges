# -*- coding: utf-8 -*-
"""Buddhist Bridges V3.0 — Final audit script (2026-08-17).

Runs the full pre-freeze audit over the V2 data modules + classification_v3.py:

  A. Identity / duplicate detection (people, places, institutions, texts)
  B. Classification consistency (band vs dates, movement vs travel, conns vs rel)
  C. Source traceability (records without sources; sources without URLs)
  D. Relationship logic (kind -> conns mapping; DIRECT/INDIRECT/MEDIATED logic)
  E. Travel vs encounter (T records vs movement; crossing logic)
  F. Events (India-Korea relevance, person-event links, participants)
  G. Places & periods (place types, period vs band consistency)
  H. Coverage profile (bands, connection types, exchange types, relevance)

Usage:  python3 buddhist-bridges/audit_v3.py   (run from the project root)
Exit code 0 = no ERRORS (warnings are informational).
"""
import os, sys, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "buddhist-bridges"))

from data_people_1 import PEOPLE_1
from data_people_2 import PEOPLE_2
from data_people_3 import PEOPLE_3
from data_people_4 import PEOPLE_4
from data_people_5 import PEOPLE_5
from data_people_6 import PEOPLE_6
from data_people_7 import PEOPLE_7
from data_people_8 import PEOPLE_8
from data_sources import SOURCES
from data_links_1 import PLACES, TRAVELS, TEXTS
from data_links_2 import INSTITUTIONS, RELS, PPL, PTX
from data_events import EVENTS, PERSON_EVENT, EVENT_PARTICIPANTS, EVENT_TYPES
import classification_v3 as C

PEOPLE = [p for mod in (PEOPLE_1, PEOPLE_2, PEOPLE_3, PEOPLE_4, PEOPLE_5,
                        PEOPLE_6, PEOPLE_7, PEOPLE_8) for p in mod]
person_lookup = {p["id"]: p for p in PEOPLE}
place_lookup = {t[0]: t for t in PLACES}
text_lookup = {t[0]: t for t in TEXTS}
inst_lookup = {t[0]: t for t in INSTITUTIONS}
event_lookup = {t[0]: t for t in EVENTS}
participant_lookup = {t[0]: t for t in EVENT_PARTICIPANTS}

errors, warnings, notes = [], [], []

def E(msg): errors.append(msg)
def W(msg): warnings.append(msg)
def N(msg): notes.append(msg)

def band_for_year(y):
    if y is None:
        return None
    if isinstance(y, str):
        m = re.match(r"(\d{4})", y)
        y = int(m.group(1)) if m else None
    if y is None:
        return None
    if y < 900: return "B1"
    if y < 1392: return "B2"
    if y < 1900: return "B3"
    if y < 1945: return "B4"
    if y < 1990: return "B5"
    return "B6"

PERIOD_TO_BAND = {"ANCIENT": "B1", "MEDIEVAL": "B2", "EARLY_MODERN": "B3",
                  "MODERN": "B4", "CONTEMPORARY": ("B5", "B6")}

def norm(s):
    return re.sub(r"[^a-z0-9\uac00-\ud7af]", "", (s or "").lower())

# ============================================================================
# A. IDENTITY / DUPLICATES
# ============================================================================
print("=" * 72); print("A. IDENTITY / DUPLICATE DETECTION"); print("=" * 72)

# A1. people: same hangul / hanja / normalized full name
hangul_map, hanja_map, name_map = defaultdict(list), defaultdict(list), defaultdict(list)
for p in PEOPLE:
    if p.get("hangul"):
        k = norm(p["hangul"])
        if k: hangul_map[k].append(p["id"])
    if p.get("hanja"):
        k = norm(p["hanja"])
        if k: hanja_map[k].append(p["id"])
    k = norm(p["full"])
    if k: name_map[k].append(p["id"])
    for v in (p.get("variants") or "").split(";"):
        v = v.strip()
        if v:
            k = norm(v)
            if k: name_map[k].append(p["id"])
for label, m in [("hangul", hangul_map), ("hanja", hanja_map), ("name", name_map)]:
    for k, ids in m.items():
        ids = sorted(set(ids))
        if len(ids) > 1:
            W(f"A1 {label} collision {k!r}: {ids}")

# A2. places: same normalized name
pname_map = defaultdict(list)
for t in PLACES:
    k = norm(t[1])
    if k: pname_map[k].append(t[0])
    for v in (t[2] or "").split(";"):
        if v.strip():
            k = norm(v)
            if k: pname_map[k].append(t[0])
for k, ids in pname_map.items():
    ids = sorted(set(ids))
    if len(ids) > 1:
        W(f"A2 place name collision {k!r}: {ids}")

# A3. institutions: same normalized name
iname_map = defaultdict(list)
for t in INSTITUTIONS:
    k = norm(t[1])
    if k: iname_map[k].append(t[0])
    for v in (t[2] or "").split(";"):
        if v.strip():
            k = norm(v)
            if k: iname_map[k].append(t[0])
for k, ids in iname_map.items():
    ids = sorted(set(ids))
    if len(ids) > 1:
        W(f"A3 institution name collision {k!r}: {ids}")

# A4. texts: same normalized title
tname_map = defaultdict(list)
for t in TEXTS:
    k = norm(t[1])
    if k: tname_map[k].append(t[0])
    for v in (t[2] or "").split(";"):
        if v.strip():
            k = norm(v)
            if k: tname_map[k].append(t[0])
for k, ids in tname_map.items():
    ids = sorted(set(ids))
    if len(ids) > 1:
        W(f"A4 text title collision {k!r}: {ids}")

# A5. known duplicate flagged in classification_audit.md: TX-0030 dup of TX-0016
if "TX-0030" in text_lookup:
    N("A5 TX-0030 exists (flagged as duplicate of TX-0016 in classification_audit.md; scope EXCLUDE)")

# ============================================================================
# B. CLASSIFICATION CONSISTENCY
# ============================================================================
print("=" * 72); print("B. CLASSIFICATION CONSISTENCY"); print("=" * 72)

india_places = {t[0] for t in PLACES if t[3] == "India"}
korea_places = {t[0] for t in PLACES if t[3] == "Korea"}

def is_crossing(t):
    o, d = t[2], t[3]
    return (o in india_places and d in korea_places) or (o in korea_places and d in india_places)

# B1. every record classified
for p in PEOPLE:
    if p["id"] not in C.PERSON: E(f"B1 PERSON missing classification: {p['id']}")
for t in PLACES:
    if t[0] not in C.PLACE: E(f"B1 PLACE missing classification: {t[0]}")
for t in TRAVELS:
    if t[0] not in C.TRAVEL: E(f"B1 TRAVEL missing classification: {t[0]}")
for t in TEXTS:
    if t[0] not in C.TEXT: E(f"B1 TEXT missing classification: {t[0]}")
for t in INSTITUTIONS:
    if t[0] not in C.INSTITUTION: E(f"B1 INSTITUTION missing classification: {t[0]}")
for t in RELS:
    if t[0] not in C.REL: E(f"B1 REL missing classification: {t[0]}")
for t in PPL:
    if t[0] not in C.PPL: E(f"B1 PPL missing classification: {t[0]}")
for t in PTX:
    if t[0] not in C.PTX: E(f"B1 PTX missing classification: {t[0]}")
for t in EVENTS:
    if t[0] not in C.EVENT: E(f"B1 EVENT missing classification: {t[0]}")

# B2. person period vs classification band
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if not e: continue
    band = e[2]
    period = p.get("period")
    if period == "CONTEMPORARY":
        ok = band in ("B5", "B6")
    else:
        ok = band == PERIOD_TO_BAND.get(period)
    if not ok:
        W(f"B2 {p['id']} {p['full']}: period={period} but band={band}")

# B3. person band vs birth/death years — only flag IMPOSSIBLE bands
# (band earlier than the birth-year band; band = principal activity, not lifespan)
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if not e: continue
    band = e[2]
    birth = p.get("birth")
    if isinstance(birth, int):
        yband = band_for_year(birth)
        if yband and band < yband:
            E(f"B3 {p['id']} {p['full']}: band={band} earlier than birth-year band {yband} (impossible)")

# B4. movement status vs travel field
MV_TO_TRAVEL = {"planned": "NO", "visited": "YES", "worked": "YES",
                "studied": "YES", "legendary": "UNCERTAIN", "-": "NO"}
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if not e: continue
    mv = e[4]
    travel = p.get("travel")
    if mv == "-" and travel == "YES":
        W(f"B4 {p['id']} {p['full']}: movement='-' but travel=YES")
    if mv in ("visited", "worked", "studied") and travel != "YES":
        W(f"B4 {p['id']} {p['full']}: movement={mv} but travel={travel}")
    if mv == "legendary" and travel not in ("UNCERTAIN", "YES"):
        W(f"B4 {p['id']} {p['full']}: movement=legendary but travel={travel}")

# B5. movement vs T records (physical movement should have a crossing T record)
travel_by_person = defaultdict(list)
for t in TRAVELS:
    travel_by_person[t[1]].append(t[0])
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if not e: continue
    mv = e[4]
    crossing_ts = [tid for tid in travel_by_person.get(p["id"], [])
                   if is_crossing(next(t for t in TRAVELS if t[0] == tid))]
    if mv in ("visited", "worked", "studied") and not travel_by_person.get(p["id"]):
        W(f"B5 {p['id']} {p['full']}: movement={mv} but no T-#### record")
    if mv == "-" and crossing_ts:
        W(f"B5 {p['id']} {p['full']}: movement='-' but has India<->Korea T-#### record(s) {crossing_ts}")

# B6. conns vs rel field (people) — only flag genuine contradictions:
# physical movement with INDIRECT/MEDIATED rel, or DIRECT rel with only INDIRECT/LEGENDARY conns
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if not e: continue
    conns = set(e[3])
    rel = p.get("rel")
    if "PHYSICAL" in conns and rel in ("INDIRECT", "MEDIATED"):
        W(f"B6 {p['id']} {p['full']}: PHYSICAL conns but rel={rel}")
    if rel == "DIRECT" and conns and conns <= {"INDIRECT", "LEGENDARY"}:
        W(f"B6 {p['id']} {p['full']}: rel=DIRECT but conns={conns}")

# B7. relevance vs scope mapping (should be enforced by builder; double-check)
SCOPE_DERIVED = {"PRIMARY": "KEEP", "SECONDARY": "ADAPT", "MEDIATOR": "ADAPT",
                 "CONTEXTUAL": "CONTEXT", "NONE": "EXCLUDE"}
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if not e: continue
    rel, scope = e[0], e[1]
    if scope != "REVIEW" and SCOPE_DERIVED.get(rel) != scope:
        E(f"B7 {p['id']}: relevance {rel} -> scope {scope} (expected {SCOPE_DERIVED.get(rel)})")

# B8. REVIEW scope should be empty at freeze
review_ids = [p["id"] for p in PEOPLE if C.PERSON.get(p["id"]) and C.PERSON[p["id"]][1] == "REVIEW"]
if review_ids:
    E(f"B8 REVIEW-scope records remain at freeze: {review_ids}")

# ============================================================================
# C. SOURCE TRACEABILITY
# ============================================================================
print("=" * 72); print("C. SOURCE TRACEABILITY"); print("=" * 72)

def check_srcs(rid, label, srcs):
    if not srcs:
        W(f"C1 {rid} ({label}): no sources listed")
        return
    for s in srcs:
        if s not in SOURCES:
            E(f"C1 {rid}: unknown source key {s!r}")

for p in PEOPLE:
    check_srcs(p["id"], p["full"], p.get("srcs") or [])
for t in EVENTS:
    check_srcs(t[0], t[1], t[12] or [])
for t in TRAVELS:
    if not t[10]:
        W(f"C1 {t[0]}: no evidence text")
for t in RELS:
    if not t[5]:
        W(f"C1 {t[0]}: no evidence text")
for t in PPL:
    if not t[6] and t[3] not in ("BIRTH", "RESIDENCE"):
        W(f"C1 {t[0]}: no notes/evidence")
for t in PTX:
    if not t[5] and t[3] != "AUTHOR":
        W(f"C1 {t[0]}: no notes/evidence")

# C2. sources without URL
for slug, (citation, stype, url, adb, rel) in SOURCES.items():
    if not url:
        E(f"C2 source {slug}: missing URL")

# C3. source type / reliability distribution sanity
stypes = Counter(s[1] for s in SOURCES.values())
N(f"C3 source types: {dict(stypes)}")

# C4. high-confidence claims should have >=1 source
for p in PEOPLE:
    if p.get("conf") == "HIGH" and not p.get("srcs"):
        E(f"C4 {p['id']} {p['full']}: HIGH confidence but no sources")

# ============================================================================
# D. RELATIONSHIP LOGIC
# ============================================================================
print("=" * 72); print("D. RELATIONSHIP LOGIC"); print("=" * 72)

REL_CONN_BY_KIND = {"MET_IN_PERSON": "ENCOUNTER", "TEACHER_STUDENT": "ENCOUNTER",
                    "INFLUENCED": "INDIRECT", "TRANSLATOR_OF": "TEXTUAL",
                    "DOCUMENTED": "TEXTUAL", "COLLEAGUE": "ENCOUNTER",
                    "FAMILY": "LEGENDARY", "CONTEMPORARY": "ENCOUNTER",
                    "CORRESPONDENT": "ENCOUNTER", "SUBJECT_OF": "TEXTUAL"}
for t in RELS:
    rid, pa, pb, kind, rtype, evid, conf, rnotes = t
    e = C.REL.get(rid)
    if not e: continue
    rel, scope, conns, why = e
    # D1. kind -> expected conns (skip tradition-based links: conns INDIRECT is deliberate)
    expected = REL_CONN_BY_KIND.get(kind)
    if expected and conns != ("-",) and expected not in conns and "per tradition" not in why:
        W(f"D1 {rid} ({kind}): conns {conns} don't include kind-derived {expected}")
    # D2. relationship_type vs kind
    if rtype == "DIRECT" and kind in ("INFLUENCED",):
        W(f"D2 {rid}: kind={kind} but relationship_type=DIRECT (influence is usually INDIRECT)")
    if rtype == "INDIRECT" and kind in ("MET_IN_PERSON", "TEACHER_STUDENT", "COLLEAGUE"):
        W(f"D2 {rid}: kind={kind} but relationship_type=INDIRECT (in-person kinds are DIRECT)")
    # D3. both endpoints classified consistently
    for pid in (pa, pb):
        pe = C.PERSON.get(pid)
        if pe and pe[1] == "EXCLUDE" and scope != "EXCLUDE":
            W(f"D3 {rid}: endpoint {pid} is EXCLUDE but rel scope={scope}")

# D4. person-place link types vs conns (skip EXCLUDE-scope links: physical types expected)
PPL_CONN_BY_LTYPE = {"BIRTH": "-", "RESIDENCE": "PHYSICAL", "VISITED": "PHYSICAL",
                     "STUDIED": "PHYSICAL", "WORKED": "INSTITUTIONAL",
                     "LEGENDARY_ORIGIN": "LEGENDARY", "DIED": "PHYSICAL", "OTHER": "-"}
for t in PPL:
    lid, pid, plid, ltype, year, conf, lnotes = t
    e = C.PPL.get(lid)
    if not e: continue
    rel, scope, why = e
    if scope == "EXCLUDE":
        continue
    expected = PPL_CONN_BY_LTYPE.get(ltype)
    if expected == "PHYSICAL" and rel == "NONE":
        W(f"D4 {lid}: link_type={ltype} (physical) but relevance=NONE")
    # D5. person travel vs PPL physical links (only India-country places)
    pe = C.PERSON.get(pid)
    pl = place_lookup.get(plid)
    if pe and pl and pl[3] == "India" and pe[4] == "-" and ltype in ("VISITED", "STUDIED", "WORKED", "RESIDENCE"):
        W(f"D5 {lid}: person {pid} movement='-' but has {ltype} link to {pl[1]}")

# ============================================================================
# E. TRAVEL vs ENCOUNTER
# ============================================================================
print("=" * 72); print("E. TRAVEL vs ENCOUNTER"); print("=" * 72)

for t in TRAVELS:
    tid, pid, origin, dest, inter, s, e_, prec, purpose, route, evid, conf, tnotes = t
    # E1. crossing travels must have a person with movement != '-'
    pe = C.PERSON.get(pid)
    if is_crossing(t) and pe and pe[4] == "-":
        W(f"E1 {tid}: India<->Korea crossing but person {pid} movement='-'")
    # E2. purpose vs movement (planned pilgrimage is consistent)
    if purpose == "PILGRIMAGE" and pe and pe[4] not in ("visited", "worked", "studied", "planned"):
        W(f"E2 {tid}: purpose=PILGRIMAGE but person {pid} movement={pe[4] if pe else '?'}")
    # E3. travel dates vs band
    band = band_for_year(e_ or s)
    ce = C.TRAVEL.get(tid)
    if ce and band and ce[2] != "-":
        pass  # movement checked elsewhere

# E4. encounter-only people (movement '-', conns ENCOUNTER) — verify no travel claim
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if not e: continue
    if e[4] == "-" and "ENCOUNTER" in e[3] and p.get("travel") == "YES":
        W(f"E4 {p['id']} {p['full']}: encounter-only but travel=YES")

# ============================================================================
# F. EVENTS
# ============================================================================
print("=" * 72); print("F. EVENTS"); print("=" * 72)

for t in EVENTS:
    eid, title, etype, start, end, loc, orgs, desc, sig, evid, conf, status, srcs = t
    # F1. India-Korea relevance: description should reference both sides
    d = (desc or "") + " " + (sig or "")
    has_india = any(k in d for k in ("India", "Indian", "인도", "Bodh Gaya", "Sarnath", "Delhi", "Nalanda", "Buddha"))
    has_korea = any(k in d for k in ("Korea", "Korean", "한국", "Jogye", "Bongeunsa", "Bunhwangsa", "Sangwol", "Jungto", "Seoul"))
    if not (has_india and has_korea):
        W(f"F1 {eid} {title}: description may lack India or Korea side (India={has_india}, Korea={has_korea})")
    # F2. event band vs dates
    band = band_for_year(end or start)
    ce = C.EVENT.get(eid)
    if ce and band and ce[2] != band:
        W(f"F2 {eid}: dates imply band {band} but classified {ce[2]}")
    # F3. event type vocabulary
    if etype not in EVENT_TYPES:
        E(f"F3 {eid}: event_type {etype!r} not in {sorted(EVENT_TYPES)}")
    # F4. location place exists (builder validates; double-check country)
    if loc in place_lookup:
        pl = place_lookup[loc]
        if pl[3] not in ("India", "Korea", "Nepal", "Sri Lanka"):
            W(f"F4 {eid}: location {loc} ({pl[1]}) is in {pl[3]} — not India/Korea/Nepal/Sri Lanka")

# F5. person_event links: every event with participants should have person_event rows
pe_by_event = defaultdict(list)
for t in PERSON_EVENT:
    pe_by_event[t[1]].append(t[0])
for t in EVENT_PARTICIPANTS:
    pid, name, hangul, role_hint, epnotes = t
    if pid not in person_lookup:
        N(f"F5 participant {pid} ({name}) is event-level only (not a PEOPLE record) — by design")
    # F6. participant referenced in person_event?
    if pid not in [x for v in pe_by_event.values() for x in v]:
        N(f"F6 participant {pid} ({name}) has no PERSON_EVENT row")

# F7. events with no person_event rows at all
for t in EVENTS:
    if not pe_by_event.get(t[0]):
        N(f"F7 {t[0]} {t[1]}: no PERSON_EVENT rows (organizer-only or no named persons)")

# ============================================================================
# G. PLACES & PERIODS
# ============================================================================
print("=" * 72); print("G. PLACES & PERIODS"); print("=" * 72)

# G1. place types sanity (MONASTERY should be an actual monastery)
MONASTERY_OK = ("Nalanda", "Sangana", "Hoeamsa", "Ximing", "Sungsusa", "Wangryunsa",
                "Chwiamsa", "Beopwonsa", "Silleuksa", "Daegaksa", "Bongeunsa",
                "Bunhwangsa", "Yeoraesunwon", "Mahayeon", "Songgwangsa", "Bongnyeongsa")
for t in PLACES:
    plid, name, variants, country, hregion, lat, lon, ptype, pnotes = t
    if ptype == "MONASTERY" and not any(k in name for k in MONASTERY_OK):
        W(f"G1 {plid} {name}: type=MONASTERY — verify name")
    if ptype == "UNIVERSITY" and not any(k in name for k in ("Nalanda", "Delhi", "Pune")):
        W(f"G1 {plid} {name}: type=UNIVERSITY — verify")

# G2. place band vs historical region (only flag clear anachronisms)
for t in PLACES:
    e = C.PLACE.get(t[0])
    if not e: continue
    band = e[2]
    hregion = t[4] or ""
    if band == "B1" and "Joseon" in hregion:
        W(f"G2 {t[0]} {t[1]}: band B1 but region {hregion!r}")

# G3. institutions: founded_year vs band — NOTE only (band = India-exchange activity, by design)
for t in INSTITUTIONS:
    iid, name, variants, loc, fy, itype, irel, krel, inotes = t
    e = C.INSTITUTION.get(iid)
    if not e: continue
    band = e[2]
    if isinstance(fy, int) and band_for_year(fy) and band_for_year(fy) != band:
        N(f"G3 {iid} {name}: founded {fy} ({band_for_year(fy)}) but band={band} — by design (band = India-exchange activity)")

# G4. texts: date vs band
for t in TEXTS:
    tid, title, variants, author, lang, date, ttype, irel, krel, tinfo, conf, tnotes = t
    e = C.TEXT.get(tid)
    if not e: continue
    band = e[2]
    if isinstance(date, int) and band_for_year(date) and band_for_year(date) != band:
        W(f"G4 {tid} {title}: date {date} implies {band_for_year(date)} but band={band}")

# ============================================================================
# H. COVERAGE PROFILE
# ============================================================================
print("=" * 72); print("H. COVERAGE PROFILE"); print("=" * 72)

rows = []
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if e: rows.append(("PEOPLE", p["id"], e[0], e[1], e[2], e[3], e[4], p.get("exch") or "-"))
for t in PLACES:
    e = C.PLACE.get(t[0])
    if e: rows.append(("PLACES", t[0], e[0], e[1], e[2], e[3], "-", "-"))
for t in TRAVELS:
    e = C.TRAVEL.get(t[0])
    if e: rows.append(("TRAVELS", t[0], e[0], e[1], band_for_year(t[6] or t[5]) or "?", ("PHYSICAL",), e[2], "-"))
for t in TEXTS:
    e = C.TEXT.get(t[0])
    if e: rows.append(("TEXTS", t[0], e[0], e[1], e[2], e[3], "-", "-"))
for t in INSTITUTIONS:
    e = C.INSTITUTION.get(t[0])
    if e: rows.append(("INSTITUTIONS", t[0], e[0], e[1], e[2], e[3], "-", "-"))
for t in RELS:
    e = C.REL.get(t[0])
    if e: rows.append(("RELS", t[0], e[0], e[1], "?", e[2], "-", "-"))
for t in PPL:
    e = C.PPL.get(t[0])
    if e: rows.append(("PPL", t[0], e[0], e[1], "?", ("-",), "-", "-"))
for t in PTX:
    e = C.PTX.get(t[0])
    if e: rows.append(("PTX", t[0], e[0], e[1], "?", ("TEXTUAL",), "-", "-"))
for t in EVENTS:
    e = C.EVENT.get(t[0])
    if e: rows.append(("EVENTS", t[0], e[0], e[1], e[2], e[3], "-", "-"))

carried = [r for r in rows if r[3] in ("KEEP", "ADAPT")]
print(f"total classified rows: {len(rows)}  (carried KEEP+ADAPT: {len(carried)})")
band_c = Counter(r[4] for r in carried)
print("carried rows by band: " + ", ".join(f"{k}={v}" for k, v in sorted(band_c.items())))
conn_c = Counter(c for r in carried for c in r[5] if c != "-")
print("carried rows by connection type: " + ", ".join(f"{k}={v}" for k, v in sorted(conn_c.items())))
exch_c = Counter(x for r in carried for x in (r[7] or "-").split(";") if x and x != "-")
print("carried rows by exchange type: " + ", ".join(f"{k}={v}" for k, v in sorted(exch_c.items())))
rel_c = Counter(r[2] for r in carried)
print("carried rows by relevance: " + ", ".join(f"{k}={v}" for k, v in sorted(rel_c.items())))
# people-only coverage
people_carried = [r for r in carried if r[0] == "PEOPLE"]
print(f"people carried: {len(people_carried)}")
print("people by band: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(r[4] for r in people_carried).items())))
print("people by movement: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(r[6] for r in people_carried).items())))
# events by type
print("events by type: " + ", ".join(f"{k}={v}" for k, v in sorted(Counter(t[2] for t in EVENTS).items())))

# ============================================================================
# REPORT
# ============================================================================
print("=" * 72)
print(f"ERRORS:   {len(errors)}")
for e in errors: print(f"  [E] {e}")
print(f"WARNINGS: {len(warnings)}")
for w in warnings: print(f"  [W] {w}")
print(f"NOTES:    {len(notes)}")
for n in notes: print(f"  [N] {n}")
print("=" * 72)
print("AUDIT " + ("FAILED" if errors else "PASSED"))
sys.exit(1 if errors else 0)