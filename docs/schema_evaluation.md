# Schema Evaluation — India–Korea Mediators Master Dataset (Pilot)

Version 0.1 · 2026-08-16 · Evaluates schema/data_dictionary.md v0.1 against the 71-record pilot.

## 1. Pilot vs. target

| Metric | Target (plan) | Actual (pilot) | Verdict |
|---|---|---|---|
| People records | 30–50 | 71 | **Exceeds pilot target** — schema held up, but review needed |
| Sources | per-person URLs | 125 sources, all with URLs | OK |
| Periods covered | all | ANCIENT 21 · MEDIEVAL 3 · EARLY_MODERN 3 · MODERN 11 · CONTEMPORARY 33 | OK (MEDIEVAL thin) |
| Relationship types | all 4 | DIRECT 42 · INDIRECT 13 · MEDIATED 10 · UNCERTAIN 6 | OK |
| Confidence | explicit | HIGH 33 · MEDIUM 32 · LOW 4 · SPECULATIVE 2 | OK |
| Status | explicit | VERIFIED 56 · PARTIAL 10 · UNRESOLVED 3 · LEGENDARY 2 | OK |
| Travel | explicit | YES 37 · NO 25 · UNCERTAIN 9 | OK |

## 2. What worked

- **Stable IDs + FK integrity**: build script caught 31 errors on first run (vocab violations, a None destination, missing travel records) — all fixed; now 0 errors / 0 warnings.
- **Controlled vocabularies**: caught real data-entry mistakes (e.g., `HUMANITARIAN`, `JOURNALISM` were added to exchange_types as legitimate new values — v0.1.1).
- **Uncertainty discipline**: legendary figures and negative results are explicitly flagged; no fabricated connections.
- **Modular data files**: splitting people into 8 modules avoided the single-file write failure; build is deterministic.

## 3. Issues found (schema v0.1)

1. **exchange_types gap**: `HUMANITARIAN` (peacekeeping/medical missions) and `JOURNALISM` (media figures) were needed → added to vocabulary (v0.1.1). Expect more additions (e.g., `SPORTS`, `TECHNOLOGY`) in Round 2.
2. **MEDIEVAL period thin** (3 records): Goryeo-era India connections are under-researched; Round 3 should target Goryeo–Yuan Buddhist networks.
3. **person_place link_type**: `LEGENDARY_ORIGIN` works, but `OTHER` is used for a few links — consider `BIRTHPLACE` vs `BIRTH` distinction later.
4. **travels.destination NULL**: schema requires a destination; generic place PL-0031 "India (unspecified)" was added for Yijing-recorded monks whose exact site is unknown. Acceptable, but note in methodology.
5. **sources.csv**: source keys are slugs (e.g., `encykorea_wangoj`); the schema's `S-####` ID convention was not used for sources — the build maps slugs → S-#### deterministically. Decide whether to keep slugs (readable) or switch to S-#### (schema-pure) in v0.2.
6. **XLSX**: built with openpyxl (9 sheets, no formatting). If the user wants a formatted workbook (filters, color-coded confidence), that's a separate deliverable.

## 4. Recommendations for v0.2

1. Keep the 9-table structure — it held up under 71 records.
2. Decide source ID convention (slugs vs S-####).
3. Add `SPORTS`/`TECHNOLOGY` to exchange_types only when Round 2 data requires them (avoid speculative vocab).
4. Consider a `person_institution` link table (currently institutions are free-text in people.institution_org) if institutional analysis becomes a goal.
5. Add a `notes` field to sources.csv rows (currently empty) for provenance caveats.
6. Re-run this evaluation after Round 2 (target: 150+ records) before any web publication.