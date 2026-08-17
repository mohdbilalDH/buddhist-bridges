# -*- coding: utf-8 -*-
"""Generate buddhist-bridges/classification_v3.csv from the V2 data modules
and buddhist-bridges/classification_v3.py (v0.2).

Every record of the V2 dataset gets one row: table, record_id, label,
buddhist_relevance, scope, period_band, connection_type (multi, "; "-joined),
movement_status, exchange_types, rationale.

The generator validates the relevance -> scope mapping (SCOPE_DERIVED) and
the movement/connection vocabularies.

Usage:  python3 build_classification.py   (run from the project root)
"""
import csv, os, sys

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
from data_links_1 import PLACES, TRAVELS, TEXTS
from data_links_2 import INSTITUTIONS, RELS, PPL, PTX
from data_events import EVENTS, PERSON_EVENT, EVENT_PARTICIPANTS
import classification_v3 as C

PEOPLE = [p for mod in (PEOPLE_1, PEOPLE_2, PEOPLE_3, PEOPLE_4, PEOPLE_5,
                        PEOPLE_6, PEOPLE_7, PEOPLE_8) for p in mod]
person_lookup = {p["id"]: p for p in PEOPLE}
participant_lookup = {t[0]: t for t in EVENT_PARTICIPANTS}

errors, warnings = [], []


def band_for_year(y):
    if y is None:
        return None
    if y < 900: return "B1"
    if y < 1392: return "B2"
    if y < 1900: return "B3"
    if y < 1945: return "B4"
    if y < 1990: return "B5"
    return "B6"


def band_label(b):
    return C.BANDS.get(b, b) if b else "-"


def person_band(pid):
    entry = C.PERSON.get(pid)
    if not entry:
        warnings.append(f"PERSON missing for {pid}")
        return None
    return entry[2]


def check(record_id, relevance, scope, conns, movement):
    """Validate one classified record against the vocabularies."""
    if relevance not in C.RELEVANCE:
        errors.append(f"{record_id}: bad relevance {relevance!r}")
    if scope not in C.SCOPES:
        errors.append(f"{record_id}: bad scope {scope!r}")
    elif scope != "REVIEW" and C.SCOPE_DERIVED.get(relevance) != scope:
        errors.append(
            f"{record_id}: scope {scope} != derived {C.SCOPE_DERIVED.get(relevance)} "
            f"for relevance {relevance}")
    for c in conns:
        if c != "-" and c not in C.CONN:
            errors.append(f"{record_id}: bad connection {c!r}")
    if movement not in C.MOVEMENT:
        errors.append(f"{record_id}: bad movement {movement!r}")


def conns_str(conns):
    if not conns:
        return "-"
    names = [C.CONN.get(c, c) for c in conns if c != "-"]
    return "; ".join(names) if names else "-"


# --- people rows -------------------------------------------------------------
rows = []
for p in PEOPLE:
    e = C.PERSON.get(p["id"])
    if not e:
        errors.append(f"PERSON classification missing for {p['id']}")
        continue
    rel, scope, band, conns, mv, why = e
    check(p["id"], rel, scope, conns, mv)
    rows.append(["PEOPLE", p["id"], p["full"], rel, scope, band_label(band),
                 conns_str(conns), mv, p.get("exch") or "-", why])

# --- places rows -------------------------------------------------------------
for t in PLACES:
    e = C.PLACE.get(t[0])
    if not e:
        errors.append(f"PLACE classification missing for {t[0]}")
        continue
    rel, scope, band, conns, why = e
    check(t[0], rel, scope, conns, "-")
    rows.append(["PLACES", t[0], t[1], rel, scope, band_label(band),
                 conns_str(conns), "-", "-", why])

# --- travels rows ------------------------------------------------------------
for t in TRAVELS:
    tid, pid = t[0], t[1]
    e = C.TRAVEL.get(tid)
    if not e:
        errors.append(f"TRAVEL classification missing for {tid}")
        continue
    rel, scope, mv, why = e
    check(tid, rel, scope, ("PHYSICAL",), mv)
    band = band_for_year(t[6] or t[5]) or person_band(pid)
    label = f"{person_lookup[pid]['full']} ({t[6] or t[5] or 'dates unknown'})"
    rows.append(["TRAVELS", tid, label, rel, scope, band_label(band),
                 "PHYSICAL_MOVEMENT", mv, person_lookup[pid].get("exch") or "-", why])

# --- texts rows --------------------------------------------------------------
for t in TEXTS:
    e = C.TEXT.get(t[0])
    if not e:
        errors.append(f"TEXT classification missing for {t[0]}")
        continue
    rel, scope, band, conns, why = e
    check(t[0], rel, scope, conns, "-")
    rows.append(["TEXTS", t[0], t[1], rel, scope, band_label(band),
                 conns_str(conns), "-", "-", why])

# --- institutions rows -------------------------------------------------------
for t in INSTITUTIONS:
    e = C.INSTITUTION.get(t[0])
    if not e:
        errors.append(f"INSTITUTION classification missing for {t[0]}")
        continue
    rel, scope, band, conns, why = e
    check(t[0], rel, scope, conns, "-")
    rows.append(["INSTITUTIONS", t[0], t[1], rel, scope, band_label(band),
                 conns_str(conns), "-", "-", why])

# --- person-person rows ------------------------------------------------------
REL_CONN_BY_KIND = {"MET_IN_PERSON": "ENCOUNTER", "TEACHER_STUDENT": "ENCOUNTER",
                    "INFLUENCED": "INDIRECT", "TRANSLATOR_OF": "TEXTUAL",
                    "DOCUMENTED": "TEXTUAL", "COLLEAGUE": "ENCOUNTER",
                    "FAMILY": "LEGENDARY", "CONTEMPORARY": "ENCOUNTER",
                    "CORRESPONDENT": "ENCOUNTER", "SUBJECT_OF": "TEXTUAL"}
for t in RELS:
    e = C.REL.get(t[0])
    if not e:
        errors.append(f"REL classification missing for {t[0]}")
        continue
    rel, scope, conns, why = e
    if conns == ("-",):
        conns = (REL_CONN_BY_KIND.get(t[3], "INDIRECT"),)
    check(t[0], rel, scope, conns, "-")
    band = person_band(t[1]) or person_band(t[2])
    label = f"{person_lookup[t[1]]['full']} <-> {person_lookup[t[2]]['full']} ({t[3]})"
    rows.append(["RELS", t[0], label, rel, scope, band_label(band),
                 conns_str(conns), "-", "-", why])

# --- person-place rows -------------------------------------------------------
PPL_CONN_BY_LTYPE = {"BIRTH": "-", "RESIDENCE": "PHYSICAL", "VISITED": "PHYSICAL",
                     "STUDIED": "PHYSICAL", "WORKED": "INSTITUTIONAL",
                     "LEGENDARY_ORIGIN": "LEGENDARY", "DIED": "PHYSICAL", "OTHER": "-"}
PPL_MV_BY_LTYPE = {"BIRTH": "-", "RESIDENCE": "worked", "VISITED": "visited",
                   "STUDIED": "studied", "WORKED": "worked",
                   "LEGENDARY_ORIGIN": "legendary", "DIED": "visited", "OTHER": "-"}
place_lookup = {t[0]: t for t in PLACES}
for t in PPL:
    e = C.PPL.get(t[0])
    if not e:
        errors.append(f"PPL classification missing for {t[0]}")
        continue
    rel, scope, why = e
    conns = (PPL_CONN_BY_LTYPE.get(t[3], "-"),)
    mv = PPL_MV_BY_LTYPE.get(t[3], "-")
    check(t[0], rel, scope, conns, mv)
    band = person_band(t[1])
    label = f"{person_lookup[t[1]]['full']} -> {place_lookup[t[2]][1]} ({t[3]})"
    rows.append(["PPL", t[0], label, rel, scope, band_label(band),
                 conns_str(conns), mv, "-", why])

# --- person-text rows --------------------------------------------------------
text_lookup = {t[0]: t for t in TEXTS}
for t in PTX:
    e = C.PTX.get(t[0])
    if not e:
        errors.append(f"PTX classification missing for {t[0]}")
        continue
    rel, scope, why = e
    check(t[0], rel, scope, ("TEXTUAL",), "-")
    band = person_band(t[1])
    label = f"{person_lookup[t[1]]['full']} -> {text_lookup[t[2]][1]} ({t[3]})"
    rows.append(["PTX", t[0], label, rel, scope, band_label(band),
                 "TEXTUAL_TRANSMISSION", "-", "-", why])

# --- events rows -------------------------------------------------------------
for t in EVENTS:
    e = C.EVENT.get(t[0])
    if not e:
        errors.append(f"EVENT classification missing for {t[0]}")
        continue
    rel, scope, band, conns, why = e
    check(t[0], rel, scope, conns, "-")
    label = f"{t[1]} ({t[3]}..{t[4]})"
    rows.append(["EVENTS", t[0], label, rel, scope, band_label(band),
                 conns_str(conns), "-", "-", why])

# --- person-event rows -------------------------------------------------------
for t in PERSON_EVENT:
    pid, eid, role = t[0], t[1], t[2]
    e = C.PERSON_EVENT.get(f"{pid}@{eid}") or C.EVENT.get(eid)
    if not e:
        errors.append(f"PERSON_EVENT classification missing for {pid}@{eid}")
        continue
    if len(e) == 5:
        rel, scope, band, conns, why = e
    else:
        rel, scope, band, conns, mv, why = e
    check(f"{pid}@{eid}", rel, scope, conns, "-")
    if pid in person_lookup:
        pname = person_lookup[pid]["full"]
    elif pid in participant_lookup:
        pname = participant_lookup[pid][1]
    else:
        pname = pid
    label = f"{pname} -> {eid} ({role})"
    rows.append(["PERSON_EVENT", f"{pid}@{eid}", label, rel, scope, band_label(band),
                 conns_str(conns), "-", "-", why])

# --- write CSV ---------------------------------------------------------------
out = os.path.join(ROOT, "buddhist-bridges", "classification_v3.csv")
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["table", "record_id", "label", "buddhist_relevance", "scope",
                "period_band", "connection_type", "movement_status",
                "exchange_types", "rationale"])
    for r in rows:
        w.writerow(r)

# --- report ------------------------------------------------------------------
from collections import Counter
print("=" * 72)
print("BUDDHIST BRIDGES V3 - CLASSIFICATION CSV BUILD REPORT (v0.2)")
print("=" * 72)
per_table = Counter(r[0] for r in rows)
for tname in ["PEOPLE", "PLACES", "TRAVELS", "TEXTS", "INSTITUTIONS", "RELS", "PPL", "PTX", "EVENTS", "PERSON_EVENT"]:
    print(f"{tname:12s}: {per_table.get(tname, 0)}")
print("-" * 72)
rels = Counter(r[3] for r in rows)
print("buddhist_relevance totals: " + ", ".join(f"{k}={v}" for k, v in sorted(rels.items())))
scopes = Counter(r[4] for r in rows)
print("scope totals: " + ", ".join(f"{k}={v}" for k, v in sorted(scopes.items())))
mvs = Counter(r[7] for r in rows if r[7] != "-")
print("movement statuses (non-'-'): " + ", ".join(f"{k}={v}" for k, v in sorted(mvs.items())))
keep = [r for r in rows if r[4] == "KEEP"]
adapt = [r for r in rows if r[4] == "ADAPT"]
context = [r for r in rows if r[4] == "CONTEXT"]
review = [r for r in rows if r[4] == "REVIEW"]
print(f"V3 carry rows (KEEP+ADAPT): {len(keep) + len(adapt)}  (CONTEXT: {len(context)}, REVIEW: {len(review)})")
people_in_scope = [r for r in rows if r[0] == "PEOPLE" and r[4] in ("KEEP", "ADAPT")]
print(f"PEOPLE carried into V3: {len(people_in_scope)}")
for band in ["B1", "B2", "B3", "B4", "B5", "B6"]:
    n = len([r for r in rows if r[5].startswith(band)])
    print(f"band {band}: {n} rows")
print("-" * 72)
print(f"ERRORS: {len(errors)}")
for e in errors:
    print(f"  [E] {e}")
print(f"WARNINGS: {len(warnings)}")
for w in warnings[:20]:
    print(f"  [W] {w}")
print(f"wrote {out}")
print("BUILD " + ("FAILED" if errors else "OK"))
sys.exit(1 if errors else 0)
