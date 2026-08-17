# Prosopography Findings Report — Phase 2, Step 2 (v1)

**Project:** Buddhist Bridges — India–Korea Buddhist Connections
**Date:** 2026-08-17
**Scope:** 43 carried people (KEEP/ADAPT) from frozen V3.0, analyzed through 8 analytical tables
**Scripts:** `analysis/build_prosopography.py` → `analysis/data/*.csv`; validated by `analysis/validate_prosopography.py` (483/483 checks pass; frozen V3.0 SHA-256 manifest unchanged, 13/13 files)

**Read this with:** `register.csv` (per-person), `role_x_period.csv`, `tradition_x_period.csv`, `movement_mediation_typology.csv`, `life_course_sequences.csv`, `relevance_comparison.csv`, `missingness_summary.csv`, `typologies.csv` — all in `analysis/data/`.

---

## 1. The five-band structure in one view

| Band | n | Population | Movement | Direction | Confidence |
|---|---|---|---|---|---|
| B1 (≤900) | 18 | 100% monastics (11 pilgrims, 6 scholars, 2 generals, 1 translator) | visited 8 / studied 3 / worked 2 / none 5 | balanced 8:8 (+1 bidir, 1 uncertain) | MEDIUM 15/18 |
| B2 (900–1392) | 6 | 100% Seon masters (5 patriarchs, Iryŏn scholar) | worked 1 (Dhyānabhadra), none 5 | 6/6 INDIA_TO_KOREA | MEDIUM 4/6 |
| B3 (1392–1900) | 0 | — (11 classified rows, all EXCLUDE) | — | — | — |
| B4 (1900–1945) | 6 | 4 non-Buddhists + Han Yong-un + Yi Yŏng-jae | none 4 / planned 2 | 5:1 I→K | HIGH 5/6 |
| B5 (1945–1990) | 5 | 1 monk-poet, 2 poets, 1 activist, 1 archaeologist | visited 2 / none 3 | 4:1 I→K | HIGH 2/5 |
| B6 (1990–2026) | 8 | 3 academics, 4 monastic leaders/bhikkhunis, 1 poet | studied 4 / visited 2 / worked 1 / none 1 | 4:1 I→K, 3 BIDIRECTIONAL | HIGH 7/8 |

**Strongest pattern:** the exchange is **period-structured, not person-structured**. Each band is a near-homogeneous cohort (monastic pilgrims → Seon patriarchs → colonial intellectuals/non-Buddhists → postwar figures → academics + institutional monastics). The population reads as five distinct generation-cohorts rather than one continuous network — a result that will shape the timeline (five separate clusters) and the network (sparse person-person core).

## 2. Patterns by theme

**Direction asymmetry.** KOREA_TO_INDIA is essentially a B1 phenomenon (8 of 11 carried KOREA_TO_INDIA cases: Ariyabalma, Hyeeop, Hyŏnt'ae, Hyŏngak, Gubon, Hyeryun, Ojin, Wonpyo; Hyecho is BIDIRECTIONAL; the 11th is split across B4–B6). From B2 onward the flow is INDIA_TO_KOREA (19 of 25 carried non-B1 cases); B6 is the first band with real bidirectional movement (Ko Un, U Myeong-ju, Wookwan). **The mediators of the later eras are Indians bringing Buddhism/ideas to Korea; the carriers of the early era are Koreans going to India.**

**The "resident worker" type spans 1,600 years with one per era:** Marananta (384), Baedalta (531), Dhyānabhadra (1289), Buddhavara (2026) — absent only in B4/B5. These four are the only carried cases of long-term religious residence.

**Two planned pilgrims, neither realized:** Tagore (planned 1937 visit) and Yi Yŏng-jae (planned 1935–37 India trip) — the colonial era's "almost" meetings. Both are HIGH confidence. Good timeline markers as unrealized events.

**Roles: translation is nearly absent from the carried population.** Only Gyeomik (B1) carries TRANSLATOR. All documented modern translation of Tagore is carried by EXCLUDE-scope figures (Kim Ŏk, Chu Yo-han, Jeong Ji-yong, etc.) via link rows L-0113…L-0125. The carried register therefore under-represents the translation layer; the textual layer must be analyzed through `texts.csv`/`person_text.csv`, not through the register roles.

**Multi-role is concentrated in B4–B6** (14 of 18 multi-role people are post-1900; Han Yong-un is the only triple-role carried person: LITERARY_FIGURE + ACTIVIST + MONK_GENERAL). Pre-modern roles are single (monk-type only).

**Tradition:** B1 is doctrinally diverse (Esoteric, Yogācāra, Vinaya, Hwaŏm, Pure Land, general), B2 is uniformly Seon (6/6), B4 splits 4 non-Buddhist / 2 Seon, B5–B6 are Seon + lay-Buddhist + academic. THERAVADA_ORIENTED appears only in B6 (Buddhavara). UNKNOWN tradition: exactly 1 (P-0054 Jung Seung-suk).

**Women enter only in B6:** Hyoseok and Wookwan are the only women in the carried population (BHIKKHUNI role first appears in B6; no bhikkhuni, no laywoman, no nun before 1990). This is either a real historical pattern or a source/collection bias — flagged as a limitation (see §5); the register documents it, it does not resolve it.

**Confidence mirror:** B1 is 15/18 MEDIUM (hagiographic sources), B6 is 7/8 HIGH (contemporary documentation). Confidence tracks *source proximity to the event*, not historical importance — consistent with the "source count ≠ importance" rule. Any B1-vs-B6 quantitative contrast must be read with `source_mix_by_band.csv`.

## 3. Typology distribution (n=43)

PILGRIM_VISITOR 12 · TEXTUAL_MEDIATOR 10 · STUDENT 7 · RESIDENT_WORKER 4 · ENCOUNTER_FIGURE 4 · INDIRECT_INFLUENCER 4 · PLANNED_PILGRIM 2.

- **TEXTUAL_MEDIATOR (10)** = people with no documented physical movement whose connection is textual (Woncheuk, Wŏnhyo, Kyŏnghŭng, T'aehyŏn, Iryŏn, Hyeil, Yi Nŭng-hwa, Ch'oe Nam-sŏn, Han Yong-un, Jung Seung-suk). This is the single largest non-travelling mediation channel — textual transmission outnumbers institutional or encounter channels.
- **ENCOUNTER_FIGURE (4)**: Naong, Sŏ Chŏng-ju, Vinoba, Yashaschandra.
- **INDIRECT_INFLUENCER (4)**: Gandhi, Muhak, Baegun, Ch'ukwŏn — lineage-mediated influence without movement (the B2 trio is entirely this type).
- No INSTITUTIONAL_ANCHOR cases: every carried person with an INSTITUTIONAL connection also carries TEXTUAL_TRANSMISSION or movement, so the institutional channel never stands alone at person level.

## 4. Important absences

1. **B3 (Joseon, 1392–1900): zero carried records.** 11 classified rows exist and all are EXCLUDE (people P-0025/26/27, place PL-0006, texts TX-0004/05/06, links L-0014/L-0104/05/06). Per the frozen rules this reads as "no records meeting current inclusion criteria" — **not** "no Buddhist India–Korea activity." The ~500-year gap is the single most consequential structural finding for both timeline and network phases.
2. **No modern translators carried** (see §2).
3. **No women before B6** (see §2).
4. **Only 2 of 43 people have person-event links** (P-0024 Naong as ORGANIZER 1370, P-0062 Buddhavara as REPRESENTATIVE 2026) — the person-event layer is nearly empty.
5. **10 of 43 have no dated activity at all** — 9 are B1 monks known only via floruits/hagiographies (Kyŏnghŭng, Hyeil, Ariyabalma, Hyeeop, Hyŏnt'ae, Hyŏngak, Gubon, Hyeryun, Hyŏnyu) plus P-0054 Jung Seung-suk. Life-course sequences are therefore structurally empty for the two extremes: early monks and one sparse B6 academic.
6. **Institution mapping covers 13/43** (10 MAPPED + 3 PARTIAL in `institution_mapping.csv`); 30/43 are UNMAPPED or NO_INSTITUTION — concentrated in B1 (pre-institutional era) and B4 (non-Buddhist figures).

## 5. Methodological limitations (explicit)

- **Descriptive only, n=43.** No inferential statistics; band differences are descriptive contrasts.
- **Source-density asymmetry.** B1 records rest on a handful of sources (Yijing, hagiographies) vs. dense modern documentation for B6. Cross-band count comparisons (e.g., "more pilgrims in B1 than academics in B6") are not valid without `source_mix_by_band.csv` qualification. This is the report's single most important interpretive caveat.
- **20 of 43 floruits are approximate** (`person_floruits.csv`); the register's `floruit_start/end` are not year-level evidence and are excluded from life-course sequences (explicit dates only — 10 sequences are empty by design).
- **Classification vocabulary in the frozen CSV** (full band strings, e.g. `B1 Ancient/early-medieval (<900)`) differs from the Phase-1 proposal docs; frozen CSV is authoritative.
- **Undocumented date derivations** (travels T-0030 Pankaj Mohan, T-0034 Hyoseok, T-0041 Kaushal Kumar = UNDOCUMENTED; L-0113 1921-vs-1923 discrepancy) concern EXCLUDE-scope records and do not enter the carried register, but they constrain any later expansion.
- **P-0054 floruit 1980–1991 crosses the B6 boundary** (overlap semantics: floruit = activity window; band = India-exchange period). Expected, not an error.
- **Single-source carried people (8):** P-0021 Wonpyo, P-0022 Hyŏnyu, P-0024 Naong, P-0055 U Myeong-ju, P-0062 Buddhavara, P-0063 Hyoseok, P-0071 Vinoba, P-0076 Yashaschandra. Their profiles rest on one source each.
- **Women's absence pre-B6** may be source/collection bias; the prosopography cannot distinguish absence-from-record from absence-in-history.

## 6. Findings robust enough to carry into the timeline and network phases

1. **Timeline will show five discrete activity clusters, not a continuous stream** (3rd–8th c., 13th–14th c., 1910s–30s, 1960s–70s, 1990s–2020s) with a ~500-year B3 void. Use `travel_start_year`, text dates, and event start dates — **not** floruits — as timeline anchors. The two PLANNED cases (Tagore 1937, Yi Yŏng-jae 1935) are usable as "planned/unrealized" markers.
2. **Network expectation: sparse person-person core.** 26/43 carried people have zero relationships to other carried people; the person-person layer is a small component (Jikong cluster: P-0023 with 4 in-population links; Tagore hub: P-0030 with 2 in-population links and 5 links to EXCLUDE-scope figures) plus the translator links outward. The **person-text layer** (12 people) and **institution layer** are the connective backbones — the network phase should build the two-mode graph (people ↔ texts ↔ institutions) rather than expect a rich one-mode person graph.
3. **Directional asymmetry is a genuine structural feature:** KOREA_TO_INDIA ≡ B1, INDIA_TO_KOREA ≡ B2–B6. Any narrative of the relationship must be bidirectional before 900 and one-directional after — until B6's partial re-bilateralization (3 BIDIRECTIONAL).
4. **B6 is the only band where monastic leaders, academics, and women coexist** — the "institutional turn" (Dhyānabhadra-style residence returns as Buddhavara's residence 2026; bhikkhuni study exchange begins with Hyoseok/Wookwan).
5. **Mediation typology priority holds across eras:** physical movement first, then textual, then institutional/encounter/indirect — but the *relative weight* shifts: B1 is 13/18 movement-based (pilgrims/students/workers), B2–B5 are majority non-movement or unrealized (textual/institutional/indirect/planned: 5/6, 4/6, 3/5), B6 is movement-based again (7/8). The mediating mechanisms invert between the early and late eras.

---

**Status:** Step 2 (prosopography) complete and validated. Awaiting review before Step 3 (timeline MVP).
