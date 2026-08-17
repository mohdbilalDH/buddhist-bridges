# Next Steps — India–Korea Mediators Master Dataset

Version 0.1 · 2026-08-16

## 1. Immediate (dataset hardening)

1. **Review the pilot with the user**: 71 people were collected against a 30–50 pilot target. Decide whether to (a) keep all 71, (b) trim to a curated subset, or (c) expand. See `docs/schema_evaluation.md`.
2. **Verify remaining PARTIAL records** (10 records): Thorat's full name, Chakravarty's identity, Rangaraj's dates, Lee Kun-hee's personal travel, Yi Kyu-gyŏng's India content.
3. **Add missing travel dates** for contemporary figures where fellowship records exist (Kaushal Kumar T-0041, Pankaj Mohan T-0030, etc.).
4. **Spot-check Korean-language sources** via the built-in browser (Naver News, EncyKorea) for the 10 PARTIAL records.

## 2. Expansion rounds (after schema evaluation)

5. **Round 2 — Buddhist exchange**: Korean monks in India post-2000 (beyond the 5 in the pilot), Indian monks in Korea, temple-food and meditation-center figures.
6. **Round 2 — Business & economic**: Samsung/Hyundai/LG India heads, Indian IT executives in Korea, KOTRA/Invest India figures.
7. **Round 2 — Arts & media**: K-pop/K-drama figures with documented India activity, Indian filmmakers on Korea, literary translators both directions.
8. **Round 2 — Academia**: Indian Koreanists beyond JNU (Delhi University, EFLU, IITs), Korean Indologists beyond the 5 in the pilot.
9. **Round 3 — Historical deep-dive**: Goryeo–Yuan Buddhist networks beyond Dhyānabhadra/Naong; Joseon envoys' India knowledge via China; colonial-era Indian visitors to Korea (e.g., Tagore circle, Indian soldiers in WWI/WWII contexts).

## 3. Analysis & visualization (the project's stated end goal)

10. **Network analysis**: build the person–person graph (18 relationships in pilot) with Gephi/NetworkX; compute centrality of mediators (Tagore, Dhyānabhadra, Nehru expected hubs).
11. **GIS mapping**: 31 places with lat/lon → map travel routes (Hyecho's pilgrimage, Gyeomik's voyage, Korean War deployments).
12. **Timeline**: interactive timeline of encounters 384 CE → 2026.
13. **Web DH project**: schema is designed for a future web publication (stable IDs, controlled vocabularies, provenance).

## 4. Maintenance

14. **Rebuild**: `python3 build_dataset.py` regenerates all CSVs/XLSX from the Python modules — run after any data edit.
15. **Versioning**: bump schema version in `schema/data_dictionary.md` and `schema/controlled_vocabularies.md` on any structural change (v0.1 → v0.2 after evaluation).
16. **Git**: initialize a repo in `india-korea-mediators/` when the user is ready (currently not a git repo).

## 5. Open questions for the user

- Should the dataset stay at 71 people, or be trimmed to a curated 30–50 pilot?
- Is the XLSX format sufficient, or do you want a separate Excel workbook with formatting (filters, color-coded confidence)?
- Do you want the analysis phase (network/GIS/timeline) to start now, or after Round 2 expansion?