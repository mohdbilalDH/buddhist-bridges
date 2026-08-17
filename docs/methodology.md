# Methodology — India–Korea Mediators Master Dataset

Version 0.1 · 2026-08-16 · Project: *Mediators Across Civilizations: Mapping Individual India–Korea Encounters*

## 1. Scope and definition

The dataset records **individuals who mediated between India and Korea** — culturally, religiously, intellectually, literarily, politically, diplomatically, economically, or militarily — from the earliest attested encounters (4th century CE) to 2026.

Inclusion is governed by the **golden rule** (schema/data_dictionary.md): *no relationship is recorded as influential without documentary evidence. Association with both countries ≠ influence.*

### Relationship typology (core rule)
- **DIRECT** = physical encounter/travel between the person and the other country (or an in-person meeting between an Indian and a Korean, including in a third country).
- **INDIRECT** = influence/connection without physical travel (e.g., Tagore writing about Korea without visiting).
- **MEDIATED** = influence through another person, language, text, or intermediary.
- **UNCERTAIN** = evidence insufficient to classify (e.g., legendary figures like Heo Hwang-ok).

## 2. Research workflow

1. **Era-based research agents** (4 parallel agents): ancient/medieval (pre-1400), Joseon/early-modern, 20th-century political/diplomatic, contemporary (1945–2026). Each agent was instructed to find individuals with **documented** India–Korea connections, with real URLs, and to explicitly report negative results.
2. **Anchor verification**: every candidate was checked against at least one authoritative source (Encyclopedia of Korean Culture, National Institute of Korean History DB, KCI/KISS scholarship, Nehru Memorial Archive, UN Digital Library, JNU/AKS faculty pages, Korean Buddhist press). Wikipedia/NamuWiki used only as tertiary pointers, never as sole evidence.
3. **Data entry**: structured records written to `data_people_1..8.py`, `data_sources.py`, `data_links_1.py`, `data_links_2.py` with stable IDs and controlled vocabularies.
4. **Validation & build**: `build_dataset.py` validates controlled vocabularies, ID uniqueness, FK integrity, and source-key references, then emits 9 CSVs + one XLSX into `data/`.

## 3. Source hierarchy and reliability

| Reliability | Meaning | Examples |
|---|---|---|
| AUTHORITATIVE | National academy, university press, peer-reviewed, primary archival | EncyKorea (AKS), db.history.go.kr, Nehru Archive, UN Digital Library |
| ACADEMIC | Scholarly articles/books (KCI, KISS, JABS, eScholarship) | KCI papers, UCLA dissertations |
| INSTITUTIONAL | Museum, embassy, government, university pages | Embassy of India Seoul, JNU, AKS, Korean Medals |
| POPULAR | Press, blogs | JoongAng Ilbo, Korea Herald, Bulkwang, BTN |
| UNVERIFIED | Not yet checked | (none used as sole evidence) |

Every person record's `srcs` field lists source keys resolved in `data/sources.csv` (125 sources, each with citation, type, URL, archive/database, accessed date, reliability).

## 4. Uncertainty handling

- **Confidence** (HIGH/MEDIUM/LOW/SPECULATIVE) is recorded per person, per travel, per relationship, and per text.
- **Status** (VERIFIED/PARTIAL/UNRESOLVED/LEGENDARY) flags record completeness.
- **Date precision** (YEAR/MONTH/DAY/CENTURY/APPROX/UNKNOWN) prevents invented precision.
- **Negative results are recorded**: candidates searched and rejected (e.g., Goryeo Hyeil's India journey, Sŏ Chŏng-ju, Hwang Tong-gyu, Kim Chi-ha) are documented in `docs/unresolved_cases.md` rather than silently dropped.
- **Legendary figures** (Heo Hwang-ok, King Suro) are included with status=LEGENDARY, confidence=SPECULATIVE, and the scholarly debate summarized in notes.

## 5. Known limitations (pilot)

- Pilot target was 30–50 records; the dataset contains **71 people** — the schema evaluation (docs/schema_evaluation.md) assesses whether this exceeds the pilot's validation capacity.
- Korean-language sources were prioritized but not exhaustively searched; some figures (e.g., Yi Kyu-gyŏng's India content) remain PARTIAL.
- Some contemporary figures' travel dates are UNKNOWN (fellowship records without dates).
- The 15-line "Lamp of the East" poem is documented as a composite/fabrication (see P-0030 notes); only the 6-line 1929 message is treated as authentic.
- Websearch API rate limits (429) during research were worked around with the built-in browser for Naver News and Korean sources.

## 6. Reproducibility

- All data lives in plain-text Python modules; `python3 build_dataset.py` regenerates all CSVs/XLSX deterministically.
- All source URLs are recorded in `data/sources.csv` with access date 2026-08-16.
- No API keys or credentials are required to rebuild.