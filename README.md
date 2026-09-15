# India–Korea Mediators / Buddhist Bridges

A Digital Humanities research project on documented mediators between India and Korea,
4th century CE to 2026. The repository holds two layers:

1. **India–Korea Mediators (V2)** — the master dataset: 76 people who mediated between the two
   countries in any domain (religious, literary, political, diplomatic, academic), entered as
   plain-text Python modules and compiled deterministically into CSVs.
2. **Buddhist Bridges (V3)** — the Buddhist-relevance classification of every V2 record, a
   frozen and checksummed release, a prosopographical analysis, and a compact web presentation
   of the central finding: *five short-lived bridges, one five-hundred-year silence.*

The public output is a single project page (plus an explore view) designed to sit inside a
personal academic website. See `buddhist-bridges/README.md` for the research summary and
`buddhist-bridges/site/DESIGN.md` for the design system.

## Repository map

| Path | Contents |
|---|---|
| `data_people_*.py`, `data_sources.py`, `data_links_*.py`, `data_events.py` | Source of truth. Structured records with stable IDs, controlled vocabularies, and source keys. Only these files are hand-edited. |
| `build_dataset.py` | Compiles the modules into `data/` (13 CSVs + XLSX). Validates vocabularies, ID uniqueness, and referential integrity. |
| `data/` | Compiled V2 CSVs. Regenerable; committed for convenience. |
| `docs/` | Methodology, data dictionary pointers, unresolved cases, schema evaluation. |
| `schema/` | Data dictionary and controlled vocabularies. |
| `buddhist-bridges/` | The V3 project. |
| `buddhist-bridges/v3.0_frozen/` | **The citable release.** 13 CSVs + SHA-256 manifest (`VERSION.md`). Never edited. |
| `buddhist-bridges/analysis/` | Derived tables, prosopography, timeline and network builders, validators, findings reports. |
| `buddhist-bridges/analysis/export_web.py` | Verifies the frozen manifest, then writes the JSON tier the site consumes. |
| `buddhist-bridges/outputs/web/` | The JSON contract between analysis and site. Committed. |
| `buddhist-bridges/site/` | Astro static site: the project page and the explore view. |
| `buddhist-bridges/site/legacy_pages/` | Earlier standalone-site pages, kept out of the build for reference. |

## Reproduce everything

```bash
# 1. Rebuild the V2 CSVs from source modules (Python 3.9+, standard library only)
python3 build_dataset.py

# 2. Verify the frozen V3.0 release and audit
cd buddhist-bridges
python3 audit_v3.py

# 3. Regenerate the web JSON tier (aborts if the frozen manifest does not verify)
python3 analysis/export_web.py

# 4. Build the site (Node 20+)
cd site
npm install
npm run build        # or `npm run dev` at http://localhost:4321
```

Continuous integration runs steps 3–4 on every push (`.github/workflows/ci.yml`) and deploys
the site to GitHub Pages from `main`.

## Method in brief

No relationship is recorded as influential without documentary evidence; association with both
countries is not influence. Every record carries a confidence grade, a completeness status, and
a date-precision field. Rejected candidates are preserved as documented negatives. Legendary
material is labelled and excluded from analysis by default. Full statement:
`docs/methodology.md` and the site's Data and method section.

## Licensing

| What | Licence |
|---|---|
| The dataset — every CSV in `data/` and `buddhist-bridges/v3.0_frozen/`, and the JSON in `buddhist-bridges/outputs/web/` | **CC BY 4.0** (`LICENSE-DATA`) |
| The code — `build_dataset.py`, the `data_*.py` source modules, and everything under `buddhist-bridges/analysis/` and `buddhist-bridges/site/` | **MIT** (`LICENSE`) |
| Third-party source texts quoted inside `evidence` and `citation` fields | Remain with their rights holders. They are quoted at reference length for verification and are not relicensed. |

## How to cite

```
Bilal, Mohd. Five Bridges, One Silence: Documented Mediators of India–Korea
Buddhist Exchange, 300–2026. Dataset v3.0.0, frozen 17 August 2026.
https://github.com/mohdbilalDH/buddhist-bridges
```

Cite the component you used rather than the repository as a whole: a single record (`P-0001`), a
figure's dataset, or the release. Every record is versioned, and a citation naming its version and
its consulted date stays checkable after the next release. `CITATION.cff` carries the
machine-readable form. A Zenodo DOI will be minted from the first tagged release and added here.

## What this dataset does and does not support

- **The rule of collection.** No relationship is recorded as influential without documentary
  evidence; association with both countries is not influence.
- **Every record carries a confidence grade, a completeness status and a date-precision field.**
  Records without a safe date are listed in the register and never placed on a time axis.
- **Documented negatives stay in.** Candidates examined and excluded are retained so the boundary
  of a claim can be inspected. The five-century Chosŏn zero is a finding under stated inclusion
  criteria, not a claim that no contact ever occurred.
- **Limits.** All analysis is descriptive (n = 43). The modern era is documented mainly through
  the press, a different evidentiary regime from the premodern chapters. Korean-language sources
  dominate, and no Indian-source corroboration round has been carried out. No woman appears in the
  record before 1990; the register records that absence and cannot by itself explain it. Only 8 of
  41 travels have a recoverable route, which is why the project publishes no map.
