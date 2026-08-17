# Buddhist Bridges

**Sixteen centuries of Buddhist exchange between India and Korea — 43 documented mediators,
five generations, one five-hundred-year silence.**

A digital humanities project: a curated, source-graded dataset of documented mediators of
India–Korea Buddhist exchange (300–2026 CE), and a static web presentation of its argument.

## Central finding

There was never one continuous "Buddhist bridge." The connection was built five times, by five
different kinds of mediator, in alternating directions — Silla pilgrims walking west (B1),
an Indian master and his Goryeo disciples (B2), colonial intellectuals connected by texts rather
than travel (B4), a thin postwar thread (B5), and a modern institutional web (B6) — separated by
the Joseon period's five-hundred-year documented silence (B3: 11 candidates examined, 0 carried).

## Layout

| Path | What it is |
|---|---|
| `v3.0_frozen/` | **The citable release.** 13 CSVs + SHA-256 manifest (`VERSION.md`). Never edited. |
| `../data_*.py`, `../build_dataset.py` | Editable source of truth (parent dir); deterministic build. |
| `analysis/` | Derived tables, prosopography, timeline/network builders + validators, findings reports. |
| `analysis/export_web.py` | Builds `outputs/web/` — verifies the frozen manifest first, fails on any mismatch. |
| `outputs/web/` | The JSON contract the site consumes. Regenerable. |
| `site/` | Astro static site (`npm run dev` / `npm run build`; data synced from `outputs/web/`). |

## Reproduce

```bash
python3 ../build_dataset.py            # rebuild CSVs from source modules (0 errors expected)
python3 audit_v3.py                    # AUDIT PASSED expected
python3 analysis/export_web.py         # verify frozen manifest + export web JSON
cd site && npm install && npm run build
```

## Method in one paragraph

Golden rule: no relationship is recorded as influential without documentary evidence —
association with both countries ≠ influence. Every record carries confidence
(HIGH/MEDIUM/LOW/SPECULATIVE), status (VERIFIED/PARTIAL/UNRESOLVED/LEGENDARY), and date
precision; single-source records are flagged; rejected candidates are preserved as documented
negatives; undated records are never assigned dates. See the site's Data & Method page and
`../docs/methodology.md`.

## License & citation

Data CC-BY-4.0 · code MIT · see `CITATION.cff`. Zenodo DOI: pending deposit.
