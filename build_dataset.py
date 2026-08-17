# -*- coding: utf-8 -*-
"""Build the India-Korea Mediators master dataset from the data_*.py modules.

Emits 9 CSVs (+ one XLSX workbook if openpyxl is available) into data/,
after running validation: controlled vocabularies, ID uniqueness, FK integrity.

Usage:  python3 build_dataset.py   (run from the project root)
"""
import csv, os, sys, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

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
from data_events import EVENTS, PERSON_EVENT, EVENT_PARTICIPANTS, EVENT_TYPES, PE_ROLES

ACCESSED = "2026-08-16"
DATA_DIR = os.path.join(ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ----------------------------------------------------------------------------
# Controlled vocabularies (mirror schema/controlled_vocabularies.md)
# ----------------------------------------------------------------------------
REL_TYPES = {"DIRECT", "INDIRECT", "MEDIATED", "UNCERTAIN"}
EXCH_TYPES = {"RELIGIOUS","LITERARY","INTELLECTUAL","POLITICAL","ARTISTIC","LINGUISTIC",
              "CULTURAL","DIPLOMATIC","ECONOMIC","MILITARY","ACADEMIC","MUSICAL","CINEMATIC",
              "HUMANITARIAN","JOURNALISM","OTHER"}
PERIODS = {"ANCIENT","MEDIEVAL","EARLY_MODERN","MODERN","CONTEMPORARY"}
DIRECTIONS = {"INDIA_TO_KOREA","KOREA_TO_INDIA","BIDIRECTIONAL","UNCERTAIN"}
CONFIDENCE = {"HIGH","MEDIUM","LOW","SPECULATIVE"}
SOURCE_TYPES = {"PRIMARY","SECONDARY","TERTIARY","ARCHIVAL","DATABASE","NEWS","WEBSITE","OTHER"}
RELIABILITY = {"AUTHORITATIVE","ACADEMIC","INSTITUTIONAL","POPULAR","UNVERIFIED"}
PLACE_TYPES = {"CITY","REGION","KINGDOM","MONASTERY","PORT","MOUNTAIN","COUNTRY","UNIVERSITY","SITE","OTHER"}
PURPOSES = {"PILGRIMAGE","DIPLOMATIC","STUDY","TRADE","EXILE","MISSIONARY","WAR","BUSINESS","ACADEMIC","OTHER","UNKNOWN"}
TEXT_TYPES = {"TRAVELOGUE","COMMENTARY","POEM","LETTER","TREATISE","BIOGRAPHY","TRANSLATION",
              "NEWSPAPER_ARTICLE","SUTRA","HISTORY","MEMOIR","OTHER"}
INST_TYPES = {"MONASTERY","UNIVERSITY","GOVERNMENT","EMBASSY","COMPANY","NGO","MEDIA","MILITARY","OTHER"}
REL_KINDS = {"TEACHER_STUDENT","CONTEMPORARY","CORRESPONDENT","TRANSLATOR_OF","SUBJECT_OF","COLLEAGUE",
             "FAMILY","MET_IN_PERSON","INFLUENCED","DOCUMENTED","OTHER"}
PPL_LINK_TYPES = {"BIRTH","RESIDENCE","VISITED","STUDIED","WORKED","LEGENDARY_ORIGIN","DIED","OTHER"}
PTX_LINK_TYPES = {"AUTHOR","TRANSLATOR","SUBJECT","MENTIONED_IN","COMMENTATOR","OTHER"}
STATUSES = {"VERIFIED","PARTIAL","UNRESOLVED","LEGENDARY"}
TRAVELED = {"YES","NO","UNCERTAIN"}

event_ids = {t[0] for t in EVENTS}

errors, warnings = [], []

# ----------------------------------------------------------------------------
# Assemble people + map source slugs -> S-#### ids
# ----------------------------------------------------------------------------
PEOPLE = [p for mod in (PEOPLE_1, PEOPLE_2, PEOPLE_3, PEOPLE_4, PEOPLE_5,
                        PEOPLE_6, PEOPLE_7, PEOPLE_8) for p in mod]
people_ids = {p["id"] for p in PEOPLE}
person_lookup = {p["id"]: p for p in PEOPLE}

slug_to_sid = {slug: f"S-{i:04d}" for i, slug in enumerate(sorted(SOURCES), 1)}
sid_to_slug = {v: k for k, v in slug_to_sid.items()}

# ----------------------------------------------------------------------------
# Validation helpers
# ----------------------------------------------------------------------------
def check(cond, msg, fatal=True):
    (errors if fatal else warnings).append(msg)

def check_member(value, allowed, ctx):
    if value not in allowed:
        errors.append(f"{ctx}: value {value!r} not in {sorted(allowed)}")

def check_list_members(value, allowed, ctx, sep=";"):
    for v in (value or "").split(sep):
        v = v.strip()
        if v and v != "NULL" and v not in allowed:
            errors.append(f"{ctx}: value {v!r} not in {sorted(allowed)}")

# --- people ------------------------------------------------------------------
seen = set()
for p in PEOPLE:
    pid = p["id"]
    if pid in seen:
        errors.append(f"people: duplicate id {pid}")
    seen.add(pid)
    check_member(p.get("rel"), REL_TYPES, f"{pid}.relationship_type")
    check_member(p.get("dir"), DIRECTIONS, f"{pid}.direction_of_influence")
    check_member(p.get("conf"), CONFIDENCE, f"{pid}.confidence")
    check_member(p.get("status"), STATUSES, f"{pid}.status")
    check_member(p.get("period"), PERIODS, f"{pid}.period")
    check_member(p.get("travel"), TRAVELED, f"{pid}.physically_traveled")
    check_list_members(p.get("exch"), EXCH_TYPES, f"{pid}.exchange_types")
    for s in p.get("srcs") or []:
        if s not in SOURCES:
            errors.append(f"{pid}.srcs: unknown source key {s!r}")

# --- sources ----------------------------------------------------------------
for slug, (citation, stype, url, adb, rel) in SOURCES.items():
    check_member(stype, SOURCE_TYPES, f"source {slug}.source_type")
    check_member(rel, RELIABILITY, f"source {slug}.reliability")
    if not url:
        errors.append(f"source {slug}: missing URL")

# --- places ------------------------------------------------------------------
seen = set()
for t in PLACES:
    if t[0] in seen:
        errors.append(f"places: duplicate id {t[0]}")
    seen.add(t[0])
    check_member(t[7], PLACE_TYPES, f"{t[0]}.place_type")
place_ids = seen

# --- travels -----------------------------------------------------------------
seen = set()
for t in TRAVELS:
    tid, pid, origin, dest, inter, s, e, prec, purpose, route, evid, conf, notes = t
    if tid in seen:
        errors.append(f"travels: duplicate id {tid}")
    seen.add(tid)
    if pid not in people_ids:
        errors.append(f"{tid}: person_id {pid} unknown")
    for pl in [origin, dest] + [x.strip() for x in (inter or "").split(";") if x.strip()]:
        if pl not in place_ids:
            errors.append(f"{tid}: place_id {pl} unknown")
    check_member(purpose, PURPOSES, f"{tid}.purpose")
    check_member(conf, CONFIDENCE, f"{tid}.confidence")

# --- texts -------------------------------------------------------------------
seen = set()
for t in TEXTS:
    tid = t[0]
    if tid in seen:
        errors.append(f"texts: duplicate id {tid}")
    seen.add(tid)
    author = t[3]
    if author is not None and author not in people_ids and author != "None":
        errors.append(f"{tid}: author_person_id {author} unknown")
    check_member(t[6], TEXT_TYPES, f"{tid}.text_type")
    check_member(t[10], CONFIDENCE, f"{tid}.confidence")

# --- institutions ------------------------------------------------------------
seen = set()
for t in INSTITUTIONS:
    iid = t[0]
    if iid in seen:
        errors.append(f"institutions: duplicate id {iid}")
    seen.add(iid)
    if t[3] is not None and t[3] not in place_ids:
        errors.append(f"{iid}: location_place_id {t[3]} unknown")
    check_member(t[5], INST_TYPES, f"{iid}.institution_type")

# --- person-person -----------------------------------------------------------
seen = set()
for t in RELS:
    rid = t[0]
    if rid in seen:
        errors.append(f"person_person: duplicate id {rid}")
    seen.add(rid)
    if t[1] not in people_ids:
        errors.append(f"{rid}: person_a_id {t[1]} unknown")
    if t[2] not in people_ids:
        errors.append(f"{rid}: person_b_id {t[2]} unknown")
    check_member(t[3], REL_KINDS, f"{rid}.relationship_kind")
    check_member(t[4], REL_TYPES, f"{rid}.relationship_type")
    check_member(t[6], CONFIDENCE, f"{rid}.confidence")

# --- person-place ------------------------------------------------------------
seen = set()
for t in PPL:
    lid = t[0]
    if lid in seen:
        errors.append(f"person_place: duplicate id {lid}")
    seen.add(lid)
    if t[1] not in people_ids:
        errors.append(f"{lid}: person_id {t[1]} unknown")
    if t[2] not in place_ids:
        errors.append(f"{lid}: place_id {t[2]} unknown")
    check_member(t[3], PPL_LINK_TYPES, f"{lid}.link_type")
    check_member(t[5], CONFIDENCE, f"{lid}.confidence")

# --- person-text -------------------------------------------------------------
text_ids = {t[0] for t in TEXTS}
seen = set()
for t in PTX:
    lid = t[0]
    if lid in seen:
        errors.append(f"person_text: duplicate id {lid}")
    seen.add(lid)
    if t[1] not in people_ids:
        errors.append(f"{lid}: person_id {t[1]} unknown")
    if t[2] not in text_ids:
        errors.append(f"{lid}: text_id {t[2]} unknown")
    check_member(t[3], PTX_LINK_TYPES, f"{lid}.link_type")
    check_member(t[4], CONFIDENCE, f"{lid}.confidence")

# --- events ------------------------------------------------------------------
seen = set()
institution_ids = {t[0] for t in INSTITUTIONS}
for t in EVENTS:
    eid = t[0]
    if eid in seen:
        errors.append(f"events: duplicate id {eid}")
    seen.add(eid)
    check_member(t[2], EVENT_TYPES, f"{eid}.event_type")
    if t[5] not in place_ids:
        errors.append(f"{eid}: location_place_id {t[5]} unknown")
    for iid in (t[6] or "").split(";"):
        iid = iid.strip()
        if iid and iid not in institution_ids:
            errors.append(f"{eid}: organizer_institution_id {iid} unknown")
    check_member(t[10], CONFIDENCE, f"{eid}.confidence")
    check_member(t[11], STATUSES, f"{eid}.status")
    for s in t[12] or []:
        if s not in SOURCES:
            errors.append(f"{eid}.srcs: unknown source key {s!r}")

# --- person-event ------------------------------------------------------------
seen = set()
event_participant_ids = {t[0] for t in EVENT_PARTICIPANTS}
for t in PERSON_EVENT:
    pid, eid, role = t[0], t[1], t[2]
    lid = f"{pid}@{eid}"
    if lid in seen:
        errors.append(f"person_event: duplicate {lid}")
    seen.add(lid)
    if pid not in people_ids and pid not in event_participant_ids:
        errors.append(f"person_event: person_id {pid} unknown (not in PEOPLE or EVENT_PARTICIPANTS)")
    if eid not in event_ids:
        errors.append(f"person_event: event_id {eid} unknown")
    check_member(role, PE_ROLES, f"{lid}.role")
    check_member(t[4], CONFIDENCE, f"{lid}.confidence")

# --- event participants ------------------------------------------------------
seen = set()
for t in EVENT_PARTICIPANTS:
    if t[0] in seen:
        errors.append(f"event_participants: duplicate id {t[0]}")
    seen.add(t[0])

# --- cross-table warnings ----------------------------------------------------
# A travel record is "crossing" if it actually connects India and Korea
# (a third-country leg, e.g. Korea->Japan or India->Japan, is not a crossing).
place_by_id = {t[0]: t for t in PLACES}
india_places = {t[0] for t in PLACES if t[3] == "India"}
korea_places = {t[0] for t in PLACES if t[3] == "Korea"}

def is_crossing(t):
    o, d = t[2], t[3]
    if o in india_places and d in korea_places:
        return True
    if o in korea_places and d in india_places:
        return True
    return False

travel_person_ids = {t[1] for t in TRAVELS}
for p in PEOPLE:
    if p.get("travel") == "YES" and p["id"] not in travel_person_ids:
        warnings.append(f"{p['id']} ({p['full']}): travel=YES but no T-#### record")
    if p.get("travel") == "NO":
        for t in TRAVELS:
            if t[1] == p["id"] and is_crossing(t):
                warnings.append(f"{p['id']} ({p['full']}): travel=NO but has a India<->Korea T-#### record")
    if not p.get("srcs"):
        warnings.append(f"{p['id']} ({p['full']}): no sources listed")

# ----------------------------------------------------------------------------
# CSV writers
# ----------------------------------------------------------------------------
def write_csv(name, header, rows):
    path = os.path.join(DATA_DIR, name)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return path

def person_row(p):
    return [p["id"], p["full"], p.get("variants"), p.get("hangul"), p.get("hanja"),
            p.get("indian"), p.get("birth"), p.get("birthp"), p.get("death"), p.get("deathp"),
            p.get("nat"), p.get("period"), p.get("role"), p.get("religion"), p.get("inst"),
            p.get("india"), p.get("korea"), p.get("rel"), p.get("travel"), p.get("tsum"),
            p.get("dir"), p.get("exch"), p.get("evid"), p.get("sig"), p.get("conf"),
            p.get("notes"), p.get("date") or ACCESSED, p.get("status"),
            ";".join(slug_to_sid[s] for s in (p.get("srcs") or []) if s in slug_to_sid)]

people_header = ["person_id","full_name","name_variants","korean_name_hangul","korean_name_hanja",
                 "indian_local_name_variants","birth_year","birth_date_precision","death_year",
                 "death_date_precision","nationality_region","period","profession_role",
                 "religious_affiliation","institution_org","india_connection","korea_connection",
                 "relationship_type","physically_traveled","travel_summary","direction_of_influence",
                 "exchange_types","evidence_of_influence","historical_significance","confidence",
                 "notes","data_entry_date","status","source_ids"]

paths = []
paths.append(write_csv("people.csv", people_header, [person_row(p) for p in PEOPLE]))
paths.append(write_csv("places.csv",
    ["place_id","place_name","name_variants","modern_country","historical_region","lat","lon","place_type","notes"],
    PLACES))
paths.append(write_csv("travels.csv",
    ["travel_id","person_id","origin_place_id","destination_place_id","intermediate_place_ids",
     "travel_start_year","travel_end_year","travel_dates_precision","purpose","route_description",
     "evidence","confidence","notes"],
    TRAVELS))
paths.append(write_csv("texts.csv",
    ["text_id","title","title_variants","author_person_id","language","date","text_type",
     "india_relevance","korea_relevance","translation_info","confidence","notes"],
    TEXTS))
paths.append(write_csv("institutions.csv",
    ["institution_id","name","name_variants","location_place_id","founded_year","institution_type",
     "india_relevance","korea_relevance","notes"],
    INSTITUTIONS))
paths.append(write_csv("person_person.csv",
    ["relationship_id","person_a_id","person_b_id","relationship_kind","relationship_type",
     "evidence","confidence","notes"],
    RELS))
paths.append(write_csv("person_place.csv",
    ["link_id","person_id","place_id","link_type","year","confidence","notes"],
    PPL))
paths.append(write_csv("person_text.csv",
    ["link_id","person_id","text_id","link_type","confidence","notes"],
    PTX))
events_header = ["event_id","title","event_type","start_date","end_date","location_place_id",
                 "organizer_institution_ids","description","significance","evidence","confidence",
                 "status","source_ids"]
events_rows = [[t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], t[11],
                ";".join(slug_to_sid[s] for s in (t[12] or []) if s in slug_to_sid)] for t in EVENTS]
paths.append(write_csv("events.csv", events_header, events_rows))
pe_header = ["person_id","event_id","role","evidence","confidence","notes"]
paths.append(write_csv("person_event.csv", pe_header, PERSON_EVENT))
ep_header = ["participant_id","name","hangul","role_hint","notes"]
paths.append(write_csv("event_participants.csv", ep_header, EVENT_PARTICIPANTS))
sources_rows = [[sid, sid_to_slug[sid], SOURCES[slug][0], SOURCES[slug][1], SOURCES[slug][2],
                 SOURCES[slug][3], ACCESSED, SOURCES[slug][4], ""]
                for sid, slug in sorted((v, k) for k, v in slug_to_sid.items())]
paths.append(write_csv("sources.csv",
    ["source_id","source_key","citation","source_type","url","archive_database","accessed_date","reliability","notes"],
    sources_rows))

# ----------------------------------------------------------------------------
# XLSX (optional)
# ----------------------------------------------------------------------------
xlsx_path = None
try:
    from openpyxl import Workbook
    wb = Workbook()
    wb.remove(wb.active)
    sheet_map = [
        ("people", people_header, [person_row(p) for p in PEOPLE]),
        ("places", ["place_id","place_name","name_variants","modern_country","historical_region","lat","lon","place_type","notes"], PLACES),
        ("travels", ["travel_id","person_id","origin_place_id","destination_place_id","intermediate_place_ids","travel_start_year","travel_end_year","travel_dates_precision","purpose","route_description","evidence","confidence","notes"], TRAVELS),
        ("texts", ["text_id","title","title_variants","author_person_id","language","date","text_type","india_relevance","korea_relevance","translation_info","confidence","notes"], TEXTS),
        ("institutions", ["institution_id","name","name_variants","location_place_id","founded_year","institution_type","india_relevance","korea_relevance","notes"], INSTITUTIONS),
        ("person_person", ["relationship_id","person_a_id","person_b_id","relationship_kind","relationship_type","evidence","confidence","notes"], RELS),
        ("person_place", ["link_id","person_id","place_id","link_type","year","confidence","notes"], PPL),
        ("person_text", ["link_id","person_id","text_id","link_type","confidence","notes"], PTX),
        ("events", events_header, events_rows),
        ("person_event", pe_header, PERSON_EVENT),
        ("event_participants", ep_header, EVENT_PARTICIPANTS),
        ("sources", ["source_id","source_key","citation","source_type","url","archive_database","accessed_date","reliability","notes"], sources_rows),
    ]
    for sheet, header, rows in sheet_map:
        ws = wb.create_sheet(sheet)
        ws.append(header)
        for r in rows:
            ws.append(["" if v is None else v for v in r])
    xlsx_path = os.path.join(DATA_DIR, "india_korea_mediators_master.xlsx")
    wb.save(xlsx_path)
except ImportError:
    print("NOTE: openpyxl not installed - skipping XLSX (CSV output only).")

# ----------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------
print("=" * 72)
print("INDIA-KOREA MEDIATORS MASTER DATASET - BUILD REPORT")
print("=" * 72)
print(f"people:        {len(PEOPLE)}  (P-{PEOPLE[0]['id']}..P-{PEOPLE[-1]['id']})")
print(f"places:        {len(PLACES)}")
print(f"travels:       {len(TRAVELS)}")
print(f"texts:         {len(TEXTS)}")
print(f"institutions:  {len(INSTITUTIONS)}")
print(f"person_person: {len(RELS)}")
print(f"person_place:  {len(PPL)}")
print(f"person_text:   {len(PTX)}")
print(f"events:        {len(EVENTS)}")
print(f"person_event:  {len(PERSON_EVENT)}")
print(f"event_participants: {len(EVENT_PARTICIPANTS)}")
print(f"sources:       {len(SOURCES)}")
print("-" * 72)
from collections import Counter
for label, fn in [
    ("period", lambda p: p["period"]), ("relationship_type", lambda p: p["rel"]),
    ("direction", lambda p: p["dir"]), ("confidence", lambda p: p["conf"]),
    ("status", lambda p: p["status"]), ("physically_traveled", lambda p: p["travel"]),
]:
    c = Counter(fn(p) for p in PEOPLE)
    print(f"{label:20s}: " + ", ".join(f"{k}={v}" for k, v in sorted(c.items())))
print("-" * 72)
print(f"ERRORS:   {len(errors)}")
for e in errors:
    print(f"  [E] {e}")
print(f"WARNINGS: {len(warnings)}")
for w in warnings[:20]:
    print(f"  [W] {w}")
if len(warnings) > 20:
    print(f"  ... and {len(warnings)-20} more")
print("-" * 72)
for p in paths:
    print(f"wrote {p}")
if xlsx_path:
    print(f"wrote {xlsx_path}")
print("BUILD " + ("FAILED" if errors else "OK"))
sys.exit(1 if errors else 0)
