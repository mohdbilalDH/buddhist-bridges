# Buddhist Bridges Dataset — V3.0 FROZEN MANIFEST

**Freeze date:** 2026-08-17
**Status:** FROZEN — no further data collection or record changes until the next research/analysis phase begins.
**Audit:** `buddhist-bridges/audit_v3.py` — 0 errors / 0 warnings (AUDIT PASSED).
**Builds:** `build_dataset.py` 0/0 · `build_classification.py` 0/0.

## Contents (13 files, frozen copies)

| File | Rows (excl. header) | Source of truth |
|---|---|---|
| people.csv | 76 | data_people_1..8.py |
| places.csv | 39 | data_links_1.py |
| travels.csv | 41 | data_links_1.py |
| texts.csv | 30 | data_links_1.py |
| institutions.csv | 31 | data_links_2.py |
| person_person.csv | 22 | data_links_2.py |
| person_place.csv | 35 | data_links_2.py |
| person_text.csv | 32 | data_links_2.py |
| events.csv | 19 | data_events.py |
| person_event.csv | 13 | data_events.py |
| event_participants.csv | 10 | data_events.py |
| sources.csv | 187 | data_sources.py |
| classification_v3.csv | 325 | buddhist-bridges/classification_v3.py |

## Freeze rules

1. The frozen CSVs in this directory are the authoritative V3.0 snapshot. The `data_*.py` modules remain the editable source of truth for the NEXT version (V3.1+).
2. No new PEOPLE, PLACES, TRAVELS, TEXTS, INSTITUTIONS, RELS, PPL, PTX, EVENTS, PERSON_EVENT, EVENT_PARTICIPANTS, or SOURCES records may be added before the next research phase is approved.
3. Corrections of factual errors found in the frozen data are allowed but must be recorded in `buddhist-bridges/CHANGELOG_v3.md` and trigger a re-freeze (V3.0.1+).
4. Documented negatives (see `docs/unresolved_cases.md`, `buddhist-bridges/collect_next.md`) are preserved as-is; "no evidence found" must never be rewritten as "did not happen".

## Verification commands (run from project root)

```
python3 build_dataset.py                 # expect 0 errors / 0 warnings
python3 buddhist-bridges/build_classification.py   # expect 0 errors / 0 warnings
python3 buddhist-bridges/audit_v3.py     # expect AUDIT PASSED
```

## SHA-256 checksums (final verified build, 2026-08-17)

```
06c380bf401da0914671ec538d3142b7f1dc3ca80cf81fde063d4adb9c48ed0e  classification_v3.csv
077be3b523d95765f906d905ba00fc206de9907ef0b5b33c6146305576417d5d  event_participants.csv
b1db2c155fc4095768aad3b420bc14a7515b74a7d82dd9955c30125211f6f96e  events.csv
1fbf3fde07fe156eee56b76cf13365622ea8ea3183f90460f8b92104c89f8c57  institutions.csv
540bb35acf3b440479dfef19f585f1c070293b010ada7572fe7fa1219c43e1bb  people.csv
98c669438365605f6a2974cc9593c9b2fafb5a9d05ef74bc89e95816bb412981  person_event.csv
f2e2d2ec308cec6ffb81da6cacf3f9df2c467f1e897ef213dfb4980ab10141af  person_person.csv
5cbfc29be097c2696ee1b31db0b42b5995b303992d0659eb06b6221132e45574  person_place.csv
c1b36a8a7ebc6721e9135d35b516cf2b8d5980ad813de7a8fedb7cddf800de31  person_text.csv
2e5c27ea913e1c2b5ff59d70268bf11ad0346f2c729f599ea424673608f03c34  places.csv
df30bae62b635aa9d79939a581978bd7f34633b980ac583bc908e2c3bed04e35  sources.csv
c73ce9ddcb2257b18e5fa56f7bb8cb0ce8c0ed33ef779406968f3437ee21da46  texts.csv
fb1426a417af10ad4fdf6e49f3f97c6163cf5d79610c7cc85ee4915a3093a045  travels.csv
```

## Companion documents

- Final data dictionary: `schema/data_dictionary_v3.0.md`
- Final schema: `buddhist-bridges/schema_v3.md` (status FINAL v3.0)
- Controlled vocabularies: `schema/controlled_vocabularies_v3.0.md`
- Provenance audit: `buddhist-bridges/provenance_audit_v3.0.md`
- Data-quality report: `buddhist-bridges/data_quality_report_v3.0.md`
- Coverage analysis: `buddhist-bridges/coverage_analysis_v3.0.md`
- Unresolved candidates & gaps: `buddhist-bridges/unresolved_v3.0.md`