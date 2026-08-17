#!/usr/bin/env python3
"""Export the web JSON tier (outputs/web/) from frozen V3.0 + validated derived tables.

Contract (dh-site-publish): the site reads ONLY outputs/web/. This script
- verifies the SHA-256 manifest in v3.0_frozen/VERSION.md before exporting,
- reads frozen CSVs and analysis/data/ derived tables read-only,
- writes small per-view JSON files, each with a _meta provenance block.

Run:  python3 analysis/export_web.py   (from buddhist-bridges/)
"""

import csv
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

BB = Path(__file__).resolve().parent.parent          # buddhist-bridges/
FROZEN = BB / "v3.0_frozen"
DERIVED = BB / "analysis" / "data"
OUT = BB / "outputs" / "web"

BANDS = [
    {"id": "B1", "label": "Silla pilgrims go west", "start": 300, "end": 900},
    {"id": "B2", "label": "The master from Magadha", "start": 900, "end": 1392},
    {"id": "B3", "label": "The long silence (Joseon)", "start": 1392, "end": 1900},
    {"id": "B4", "label": "Paper bridges", "start": 1900, "end": 1945},
    {"id": "B5", "label": "Thin threads", "start": 1945, "end": 1990},
    {"id": "B6", "label": "The institutional turn", "start": 1990, "end": 2027},
]


def verify_manifest() -> str:
    """Recompute SHA-256 of every frozen CSV against VERSION.md; abort on mismatch."""
    text = (FROZEN / "VERSION.md").read_text(encoding="utf-8")
    expected = dict(
        (name, digest)
        for digest, name in re.findall(r"^([0-9a-f]{64})\s+(\S+\.csv)$", text, re.M)
    )
    if len(expected) != 13:
        sys.exit(f"manifest parse error: found {len(expected)} hashes, expected 13")
    for name, want in expected.items():
        got = hashlib.sha256((FROZEN / name).read_bytes()).hexdigest()
        if got != want:
            sys.exit(f"FROZEN FILE MODIFIED: {name}\n  manifest {want}\n  on disk  {got}")
    return hashlib.sha256("".join(sorted(expected.values())).encode()).hexdigest()[:16]


def rows(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def meta(manifest_id: str, note: str) -> dict:
    return {
        "dataset": "Buddhist Bridges V3.0 (frozen 2026-08-17)",
        "manifest_check": manifest_id,
        "generated": date.today().isoformat(),
        "note": note,
    }


def write(name: str, payload: dict) -> None:
    path = OUT / name
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  {name:>18}  {path.stat().st_size/1024:6.1f} KB")


def main() -> None:
    manifest_id = verify_manifest()
    print(f"manifest verified ({manifest_id}); exporting to {OUT}")
    OUT.mkdir(parents=True, exist_ok=True)

    people = rows(FROZEN / "people.csv")
    travels = rows(FROZEN / "travels.csv")
    places = {p["place_id"]: p for p in rows(FROZEN / "places.csv")}
    events = rows(FROZEN / "events.csv")
    sources = rows(FROZEN / "sources.csv")
    classification = rows(FROZEN / "classification_v3.csv")
    person_event = rows(FROZEN / "person_event.csv")

    register = {r["person_id"]: r for r in rows(DERIVED / "register.csv")}
    for r in register.values():          # frozen register stores full band strings
        r["band"] = (r["band"] or "")[:2]
    typology = {r["person_id"]: r for r in rows(DERIVED / "movement_mediation_typology.csv")}
    floruits = {r["person_id"]: r for r in rows(DERIVED / "person_floruits.csv")}
    source_mix = rows(DERIVED / "source_mix_by_band.csv")

    src_by_id = {s["source_id"]: s for s in sources}

    def resolve_sources(ids_field: str) -> list[dict]:
        out = []
        for sid in re.split(r"[;,|]\s*", ids_field or ""):
            sid = sid.strip()
            if sid and sid in src_by_id:
                s = src_by_id[sid]
                out.append({
                    "id": sid, "citation": s["citation"], "url": s["url"],
                    "type": s["source_type"], "reliability": s["reliability"],
                })
        return out

    # ---- sources.json -------------------------------------------------------
    write("sources.json", {
        "_meta": meta(manifest_id, "Full graded source registry (187 sources)."),
        "sources": [{
            "id": s["source_id"], "key": s["source_key"], "citation": s["citation"],
            "type": s["source_type"], "url": s["url"], "archive": s["archive_database"],
            "accessed": s["accessed_date"], "reliability": s["reliability"],
        } for s in sources],
    })

    # ---- people.json (carried register, 43) ---------------------------------
    carried = []
    for p in people:
        reg = register.get(p["person_id"])
        if not reg:                        # register.csv holds only carried people
            continue
        fl = floruits.get(p["person_id"], {})
        ty = typology.get(p["person_id"], {})
        carried.append({
            "id": p["person_id"],
            "name": p["full_name"],
            "hangul": p["korean_name_hangul"],
            "hanja": p["korean_name_hanja"],
            "variants": p["name_variants"],
            "band": reg["band"],
            "nationality": p["nationality_region"],
            "role": p["profession_role"],
            "roles": [r for r in (reg["role_1"], reg["role_2"], reg["role_3"]) if r],
            "tradition": [t for t in (reg["tradition_1"], reg["tradition_2"], reg["tradition_3"]) if t],
            "typology": ty.get("typology", ""),
            "movement": reg["movement_status"],
            "direction": p["direction_of_influence"],
            "birth": p["birth_year"], "death": p["death_year"],
            "birth_precision": p["birth_date_precision"],
            "floruit": [fl.get("floruit_start", ""), fl.get("floruit_end", "")],
            "floruit_precision": fl.get("precision", ""),
            "india_connection": p["india_connection"],
            "korea_connection": p["korea_connection"],
            "evidence": p["evidence_of_influence"],
            "significance": p["historical_significance"],
            "confidence": p["confidence"],
            "status": p["status"],
            "single_source": reg["single_source"].strip().upper() == "YES",
            "source_count": reg["source_count"],
            "sources": resolve_sources(p["source_ids"]),
        })
    order = {b["id"]: i for i, b in enumerate(BANDS)}
    carried.sort(key=lambda r: (order.get(r["band"], 9), r["id"]))
    write("people.json", {
        "_meta": meta(manifest_id, "43 carried people: frozen record + prosopography register + floruits + typology."),
        "people": carried,
    })

    # ---- story.json ---------------------------------------------------------
    band_of = {r["person_id"]: r["band"] for r in register.values()}

    direction_by_band: dict[str, dict] = {}
    for pid, reg in register.items():
        d = direction_by_band.setdefault(reg["band"], {})
        d[reg["direction_of_influence"]] = d.get(reg["direction_of_influence"], 0) + 1

    mechanism_by_band: dict[str, dict] = {}
    for row in classification:
        if row["scope"] in ("KEEP", "ADAPT") and row["period_band"][:2] in ("B1", "B2", "B3", "B4", "B5", "B6"):
            band = row["period_band"][:2]
            for ct in re.split(r"[;,+|]\s*", row["connection_type"] or ""):
                ct = ct.strip()
                if ct and ct != "-":
                    m = mechanism_by_band.setdefault(band, {})
                    m[ct] = m.get(ct, 0) + 1

    resident_ids = ["P-0006", "P-0012", "P-0023", "P-0062"]
    residents = [p for p in carried if p["id"] in resident_ids]
    planned = [p for p in carried if p["typology"] == "PLANNED_PILGRIM"]

    journeys = []
    for t in travels:
        if band_of.get(t["person_id"]) is None:
            continue
        o, d = places.get(t["origin_place_id"]), places.get(t["destination_place_id"])
        inter = [places[i.strip()] for i in re.split(r"[;,|]\s*", t["intermediate_place_ids"] or "")
                 if i.strip() in places]
        journeys.append({
            "id": t["travel_id"], "person": t["person_id"],
            "person_name": next((p["name"] for p in carried if p["id"] == t["person_id"]), ""),
            "band": band_of.get(t["person_id"], ""),
            "start": t["travel_start_year"], "end": t["travel_end_year"],
            "precision": t["travel_dates_precision"], "purpose": t["purpose"],
            "routed": bool(inter),
            "route_description": t["route_description"],
            "confidence": t["confidence"],
            "points": [{"name": pl["place_name"], "lat": pl["lat"], "lon": pl["lon"]}
                       for pl in ([o] + inter + [d]) if pl and pl["lat"]],
        })

    ev_out = [{
        "id": e["event_id"], "title": e["title"], "type": e["event_type"],
        "start": e["start_date"], "end": e["end_date"],
        "description": e["description"], "significance": e["significance"],
        "confidence": e["confidence"], "status": e["status"],
        "sources": resolve_sources(e["source_ids"]),
        "participants": [pe["person_id"] for pe in person_event if pe["event_id"] == e["event_id"]],
    } for e in events]

    write("story.json", {
        "_meta": meta(manifest_id, "Curated data for the five-chapter argument."),
        "bands": BANDS,
        "cohort_sizes": {b: sum(1 for r in register.values() if r["band"] == b)
                         for b in ("B1", "B2", "B3", "B4", "B5", "B6")},
        "direction_by_band": direction_by_band,
        "mechanism_by_band": mechanism_by_band,
        "residents": residents,
        "planned_pilgrims": planned,
        "journeys": journeys,
        "events": ev_out,
        "source_mix_by_band": [
            {"band": r["band"], "type": r["source_type"], "count": int(r["count"])}
            for r in source_mix],
        "b3_note": ("Joseon (1392–1900): 11 candidate rows classified, all excluded on evidence. "
                    "Zero carried records is a documented finding under stated inclusion criteria, "
                    "not an absence of Buddhism and not missing data."),
    })

    # ---- timeline.json (already validated upstream) -------------------------
    timeline = json.loads((DERIVED / "timeline_data.json").read_text(encoding="utf-8"))
    timeline["_meta"] = meta(manifest_id, "Pass-through of validated timeline_data.json (validate_timeline.py).")
    write("timeline.json", timeline)

    # ---- network.json (period slices only) ----------------------------------
    nodes = rows(BB / "analysis" / "network" / "network_nodes.csv")
    edges = rows(BB / "analysis" / "network" / "network_edges.csv")

    def slice_for(bands: set[str]) -> dict:
        eset = [e for e in edges if e["historical_band"] in bands and e["legendary"].upper() != "TRUE"]
        keep_ids = {e["source_node"] for e in eset} | {e["target_node"] for e in eset}
        nset = [n for n in nodes if n["node_id"] in keep_ids]
        return {
            "nodes": [{"id": n["node_id"], "label": n["label"], "type": n["node_type"],
                       "band": n["historical_band"], "confidence": n["confidence"],
                       "single_source": n["single_source"]} for n in nset],
            "edges": [{"id": e["edge_id"], "source": e["source_node"], "target": e["target_node"],
                       "kind": e["connection_type"], "subtype": e["subtype"],
                       "direction": e["direction"], "confidence": e["confidence"],
                       "evidence": e["evidence"]} for e in eset],
        }

    write("network.json", {
        "_meta": meta(manifest_id, "Two period slices; the all-at-once graph is deliberately not exported."),
        "slices": {
            "b2_circle": slice_for({"B2"}),
            "b6_web": slice_for({"B5", "B6"}),
        },
    })

    # ---- core.json ----------------------------------------------------------
    write("core.json", {
        "_meta": meta(manifest_id, "Site-wide counts and band definitions."),
        "bands": BANDS,
        "counts": {
            "people_carried": len(carried),
            "people_total": len(people),
            "events": len(events),
            "sources": len(sources),
            "travels": len(travels),
            "journeys_routed": sum(1 for j in journeys if j["routed"]),
            "texts": len(rows(FROZEN / "texts.csv")),
            "institutions": len(rows(FROZEN / "institutions.csv")),
        },
    })

    print("export complete")


if __name__ == "__main__":
    main()
