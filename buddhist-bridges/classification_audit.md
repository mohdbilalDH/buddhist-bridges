# Buddhist Bridges — Classification Audit of the V2 Dataset (v0.2)

**Date:** 2026-08-17 · **Inputs:** `data_people_1..8.py`, `data_links_1.py`, `data_links_2.py`, `buddhist-bridges/classification_v3.py`
**Machine-readable output:** `buddhist-bridges/classification_v3.csv` (regenerate: `python3 buddhist-bridges/build_classification.py`)
**Supersedes:** v0.1 (2026-08-17) — binary scope replaced by the graded relevance scale per the user's methodological pass.

---

## 1. Method

Every one of the 275 V2 records was classified individually against the Buddhist Bridges scope:

- **`buddhist_relevance`** (graded, the V3 decision mechanism):
  - **PRIMARY** — Buddhist identity: monks/nuns/ordained practitioners, Buddhist institutions, sacred sites, core Buddhist texts.
  - **SECONDARY** — significant Buddhist activity, primary identity elsewhere (scholars of Buddhism, Buddhist-themed writers, partly-Buddhist institutions/texts).
  - **MEDIATOR** — not Buddhist themselves, but a documented channel in the India–Korea Buddhist exchange (Tagore, Gandhi, Vinoba, hosts).
  - **CONTEXTUAL** — relevant background/context, no direct Buddhist channel (legends, literary circles, partly-relevant surveys).
  - **NONE** — no Buddhist relevance (V2-only records).
- **`scope`** (carry decision, derived from relevance and validated by the generator): PRIMARY→KEEP, SECONDARY→ADAPT, MEDIATOR→ADAPT, CONTEXTUAL→CONTEXT, NONE→EXCLUDE; REVIEW is an explicit override (P-0068, P-0070).
- Each record also receives a **period band** (B1–B6), one or more **connection types** from the six-level ladder (PHYSICAL_MOVEMENT → PERSON_ENCOUNTER → INSTITUTIONAL → TEXTUAL_TRANSMISSION → INDIRECT_INFLUENCE → LEGENDARY, multi-valued), and a **movement status** (planned/visited/worked/studied/legendary/-). Relationship/link tables inherit their people's relevance; a link is excluded when its *content* is non-Buddhist even if the person is in scope.

## 2. Headline numbers

| Table | Total | KEEP | ADAPT | CONTEXT | EXCLUDE | REVIEW |
|-------|------:|-----:|------:|--------:|--------:|-------:|
| PEOPLE | 70 | 29 | 7 | 10 | 22 | 2 |
| PLACES | 31 | 15 | 9 | 3 | 4 | 0 |
| TRAVELS | 39 | 21 | 3 | 1 | 14 | 0 |
| TEXTS | 30 | 11 | 2 | 7 | 10 | 0 |
| INSTITUTIONS | 21 | 9 | 1 | 2 | 9 | 0 |
| RELS | 18 | 3 | 3 | 8 | 4 | 0 |
| PPL | 34 | 17 | 0 | 6 | 11 | 0 |
| PTX | 32 | 12 | 2 | 9 | 9 | 0 |
| **Total** | **275** | **117** | **27** | **46** | **83** | **2** |

**Relevance totals:** PRIMARY=117, SECONDARY=11, MEDIATOR=18, CONTEXTUAL=46, NONE=83.
**Movement totals (non-"-"):** visited=42, studied=29, worked=33, legendary=3, planned=1.
**People carried into V3: 36** (29 KEEP + 7 ADAPT), plus 10 CONTEXT reference rows and 2 REVIEW. Dataset-wide V3 carry rows (KEEP+ADAPT): 144; CONTEXT: 46.

vs v0.1: people in scope grew 34 → 36 (P-0030 Tagore and P-0038 Gandhi joined as MEDIATOR; P-0034 Han Yong-un upgraded ADAPT→KEEP), and 10 people moved from EXCLUDE to CONTEXT.

## 3. People — in scope (36)

### 3.1 KEEP (29) — PRIMARY Buddhist identity

| ID | Person | Band | Connection(s) | Movement | Core content |
|----|--------|------|---------------|----------|--------------|
| P-0001 | Hyecho | B1 | PHYSICAL_MOVEMENT; TEXTUAL_TRANSMISSION | visited | Pilgrimage to Five Indias; *Wang ocheonchukguk jeon* |
| P-0002 | Woncheuk | B1 | TEXTUAL_TRANSMISSION | - | Yogacara in Chang'an; Indian doctrine via Xuanzang corpus |
| P-0003 | Wŏnhyo | B1 | TEXTUAL_TRANSMISSION | - | Commentaries on Indian-origin texts (Awakening of Faith) |
| P-0004 | Kyŏnghŭng | B1 | TEXTUAL_TRANSMISSION | - | Silla exegete of Indian sutra heritage |
| P-0005 | T'aehyŏn | B1 | TEXTUAL_TRANSMISSION | - | Yogacara commentator (Cheng Weishi Lun lineage) |
| P-0006 | Marananta | B1 | PHYSICAL_MOVEMENT; INSTITUTIONAL | worked | 384 CE arrival; founder of Baekje Buddhism |
| P-0009 | Iryŏn | B2 | TEXTUAL_TRANSMISSION | - | *Samguk Yusa* — primary record of early traditions |
| P-0010 | Hyeil | B1 | TEXTUAL_TRANSMISSION | - | Amoghavajra-lineage esoteric transmission |
| P-0011 | Gyeomik | B1 | PHYSICAL_MOVEMENT; TEXTUAL_TRANSMISSION | studied | Sea pilgrimage 526–531; Vinaya; Sanskrit |
| P-0012 | Baedalta | B1 | PHYSICAL_MOVEMENT; TEXTUAL_TRANSMISSION | worked | Indian master resident in Baekje (531) |
| P-0013 | Ariyabalma | B1 | PHYSICAL_MOVEMENT | studied | Silla monk at Nalanda (Yijing) |
| P-0014 | Hyeeop | B1 | PHYSICAL_MOVEMENT | visited | Bodh Gaya/Nalanda; manuscripts seen by Yijing |
| P-0015 | Hyŏnt'ae | B1 | PHYSICAL_MOVEMENT | visited | Pilgrim to India (Yijing) |
| P-0016 | Hyŏngak | B1 | PHYSICAL_MOVEMENT | visited | Died at Bodh Gaya (Yijing) |
| P-0017 | Gubon | B1 | PHYSICAL_MOVEMENT | visited | Pilgrim to India (Yijing) |
| P-0018 | Hyeryun | B1 | PHYSICAL_MOVEMENT | visited | In Yijing's India network |
| P-0020 | Ojin | B1 | PHYSICAL_MOVEMENT | visited | Reached Central India; died in Tibet |
| P-0021 | Wonpyo | B1 | PHYSICAL_MOVEMENT | visited | India via Tang (742–765) |
| P-0022 | Hyŏnyu | B1 | PHYSICAL_MOVEMENT | studied | Ordained in Sri Lanka (South Asian Buddhist world) |
| P-0023 | Dhyānabhadra | B2 | PHYSICAL_MOVEMENT; INSTITUTIONAL; PERSON_ENCOUNTER | worked | Indian master; Nalanda → Goryeo; Hoeamsa (1328); Naong's teacher |
| P-0024 | Naong Hyegeun | B2 | PERSON_ENCOUNTER | - | Transmission from Jikong (in-person, two meetings) |
| P-0034 | Han Yong-un | B4 | INDIRECT_INFLUENCE; TEXTUAL_TRANSMISSION | - | Buddhist monk-poet (PRIMARY identity); Tagore reception; *Nim-ŭi Ch'immuk* (upgraded from ADAPT in v0.2) |
| P-0052 | Pŏpchŏng | B5 | PHYSICAL_MOVEMENT; PERSON_ENCOUNTER | visited | 1971 India pilgrimage; met Vinoba Bhave; *Muso-yu* |
| P-0053 | Lokesh Chandra | B6 | PHYSICAL_MOVEMENT; TEXTUAL_TRANSMISSION | visited | Career Buddhist-studies Indologist; India–Korea interflow scholarship; Seoul 2016 |
| P-0055 | U Myeong-ju | B6 | PHYSICAL_MOVEMENT; INSTITUTIONAL | studied | Delhi University MA/PhD Buddhist Studies; DU lecturer |
| P-0062 | Buddhavara | B6 | PHYSICAL_MOVEMENT; INSTITUTIONAL | worked | Bunhwangsa India abbot; BGICBS; DU MOU 2026 |
| P-0063 | Hyoseok | B6 | PHYSICAL_MOVEMENT; INSTITUTIONAL | studied | Pune MA → Delhi PhD (bhikkhuni) |
| P-0064 | Wookwan | B6 | PHYSICAL_MOVEMENT; TEXTUAL_TRANSMISSION | studied | Delhi University; temple-food master |
| P-0065 | Gakseong | B6 | PHYSICAL_MOVEMENT; INSTITUTIONAL | studied | Delhi University 1992–98; 4,500 km pilgrimage |

### 3.2 ADAPT (7) — SECONDARY / MEDIATOR, needs reframing

| ID | Person | Band | Relevance | Connection(s) | Why ADAPT |
|----|--------|------|-----------|---------------|-----------|
| P-0028 | Yi Nŭng-hwa | B4 | SECONDARY | TEXTUAL_TRANSMISSION | Scholar (not practitioner) of Buddhism; *Chosŏn Pulgyo T'ongsa* is core Buddhist historiography |
| P-0029 | Ch'oe Nam-sŏn | B4 | SECONDARY | TEXTUAL_TRANSMISSION; PERSON_ENCOUNTER | Wrote *Chosŏn Pulgyo* (1930) on Buddhism's direct Indian origin; nationalist framing — reframe as historiography |
| P-0030 | Tagore | B4 | MEDIATOR | INDIRECT_INFLUENCE; PERSON_ENCOUNTER | Not Buddhist, but documented channel: *Lamp of the East* (1929) invoked Korea's Buddhist heritage; influenced Han Yong-un; Seoul visit planned 1929 (new in scope v0.2) |
| P-0038 | Gandhi | B4 | MEDIATOR | INDIRECT_INFLUENCE | Not Buddhist, but his words open Pŏpchŏng's *Muso-yu* — textual influence on a Buddhist monk (new in scope v0.2) |
| P-0051 | Ko Un | B6 | SECONDARY | PHYSICAL_MOVEMENT; TEXTUAL_TRANSMISSION | Poet, ordained 1952–62; India travels + *Little Pilgrim* (Buddha novel) — literary-academic channel |
| P-0054 | Jung Seung-suk | B6 | SECONDARY | TEXTUAL_TRANSMISSION | Korean scholar of Indian/Buddhist philosophy; domestic tradition (Dongguk degrees, not India-trained) |
| P-0071 | Vinoba Bhave | B5 | MEDIATOR | PERSON_ENCOUNTER | Gandhian, not Buddhist — kept as the documented Indian counterpart of Pŏpchŏng's 1971 encounter |

### 3.3 CONTEXT (10) — reference-only rows

P-0007 Heo Hwang-ok, P-0008 Suro (legend); P-0031 Chin Hak-mun, P-0032 Kim Ŏk, P-0033 Jeong Ji-yong, P-0035 Yi Kwang-su, P-0036 Chu Yo-han (Tagore literary circle); P-0037 Ham Sŏk-hŏn (Quaker Gandhi bridge); P-0059 Vyjayanti Raghavan, P-0061 (co-editor/subject of partly-Buddhist cultural-religious works). Carried in V3 as labelled context only.

### 3.4 REVIEW (2) — pending research

| ID | Person | Issue |
|----|--------|-------|
| P-0068 | Sŏ Chŏng-ju | SECONDARY (Buddhist poet, Dongguk) but **no India link found** — research targets: Asian poetry congresses, Buddhist-press coverage |
| P-0070 | Kim Chi-ha | MEDIATOR (tentative); popular Gandhi/ahimsa association **unverifiable in available sources** — needs a primary source or stays out |

## 4. People — EXCLUDE (22), grouped

**Joseon/Silhak geography (3):** P-0025 Yi Su-gwang, P-0026 Yi Kyu-gyŏng, P-0027 Ch'oe Han-gi — India entered Joseon via Chinese-world geography, not Buddhism.

**Politics/military/economy (12):** P-0039 Nehru, P-0040 Krishna Menon, P-0041 Panikkar, P-0042 K.P.S. Menon, P-0043 Thimayya, P-0044 Thorat, P-0045 Chakravarty, P-0046 Rangaraj, P-0047 Aga, P-0048 Park Chan-hyun, P-0049 Kim Woo-choong, P-0050 Lee Kun-hee — diplomatic/military/economic channels only.

**Non-Buddhist academia/translation (6):** P-0056 Lee Jeong-ho, P-0057 Pankaj Mohan, P-0058 Neerja Samajdar, P-0060 Kaushal Kumar, P-0066 Divik Ramesh, P-0067 Dileep Jhaveri — Korean/Hindi studies, literary translation.

**No documented link (1):** P-0069 Hwang Tong-gyu (UNRESOLVED in V2; no India link).

## 5. Borderline decisions — v0.2 grading notes

1. **Tagore cluster.** v0.2 split by content: Tagore himself (P-0030), *Lamp of the East* (TX-0010, L-0110), and the Han Yong-un influence edge (R-0009) are **MEDIATOR/ADAPT** — the *Lamp* explicitly addresses Korea's Buddhist heritage and the reception shaped Buddhist poetry. The literary translations and meetings (P-0031..P-0033, P-0035, P-0036; TX-0008/0009/0011/0013–0015; R-0004..R-0008, R-0010) are **CONTEXT**. Gitanjali/Gardener texts carry no Buddhist content.
2. **Gandhi/Vinoba.** Gandhi (P-0038) and Vinoba (P-0071) are **MEDIATOR/ADAPT**: R-0012 (Gandhi's words opening *Muso-yu*) and R-0013 (Pŏpchŏng–Vinoba 1971 meeting) are the documented Buddhist-exchange edges. Ham Sŏk-hŏn (Quaker) is CONTEXT.
3. **Heo Hwang-ok / Suro.** CONTEXT (reference-only); their source texts (*Samguk Yusa* TX-0003, *Samguk Sagi* TX-0028) are KEEP as Buddhist-authored primary records; L-0128/L-0129 (legend SUBJECT links) are CONTEXT.
4. **Sri Lanka (P-0022 Hyŏnyu, PL-0022, T-0012).** KEEP under "South Asian Buddhist world"; flagged in the CSV rationale. Excludable if the user wants strictly mainland-India scope.
5. **Seoul (PL-0024) / New Delhi (PL-0027).** KEEP — both are hubs of the modern Buddhist exchange (Jogye HQ, Dongguk, Bongwonsa / Delhi University, IBC, GBS 2026).
6. **Ch'oe Nam-sŏn split.** Person SECONDARY/ADAPT; TX-0016 (*Chosŏn Pulgyo* 1930) KEEP; T-0016 (1916 Tokyo Tagore meeting) ADAPT only as part of his Buddhist-history channel.
7. **TX-0030** is a duplicate of TX-0016 — EXCLUDE; drop in V3.
8. **Mediator places (8).** Chang'an, Guangzhou, Kucha, Serindia, Nishapur, Tibet, Yuan Dadu, Eastern Jin are MEDIATOR/ADAPT — transit/route nodes of the Buddhist transmission rather than Buddhist sites themselves.

## 6. Entity tables — summary

- **PLACES KEEP/ADAPT (24):** B1 sacred-site/monastery/kingdom records (Silla, Baekje, Goguryeo, Goryeo, Gandhara, Nalanda, Bodh Gaya, Kashmir, Sangana, Sri Lanka, Gyeongju, generic India), Delhi, Pune (ADAPT), Seoul, New Delhi, plus 8 mediator route nodes (ADAPT). CONTEXT: Gaya/Ayodhya (legend), Ayuta, Tokyo/Yokohama. EXCLUDE: Joseon, Busan, Panmunjom, Meerut.
- **TRAVELS KEEP (21) + ADAPT (3):** all B1 monastic journeys + Dhyānabhadra (B2) + Pŏpchŏng 1971, Lokesh Chandra 2016, U Myeong-ju, Buddhavara, Hyoseok, Wookwan, Gakseong, Hyeryun (KEEP); Ko Un (T-0025), Ch'oe Nam-sŏn (T-0016), Tagore's Japan visits (T-0014, MEDIATOR) (ADAPT). CONTEXT: Chin Hak-mun (T-0015). EXCLUDE: Korean-War diplomats/military, Kim Woo-choong, Lee Jeong-ho, JNU/SNU scholars, Jhaveri, Kaushal Kumar.
- **TEXTS KEEP/ADAPT (13):** travelogues/commentaries/histories/essays with Buddhist content (TX-0001..0003, 0007, 0012, 0016, 0018..0020, 0028, 0029; ADAPT: TX-0021 survey, TX-0010 Lamp of the East). CONTEXT: Tagore poems/translations, Gandhi biography. EXCLUDE: geography encyclopedias, dictionary, ICF history, TX-0030 dup.
- **INSTITUTIONS KEEP/ADAPT (10):** Nalanda, Hoeamsa, Dongguk, Delhi University, BGICBS, Bunhwangsa India, Mahayeon, Songgwangsa, Bongnyeongsa (KEEP); Pune (ADAPT). CONTEXT: Ayuta state, Visva-Bharati. EXCLUDE: NNRC/ICF/60PFA, JNU CKS, AKS, HUFS, Daewoo, Samsung, Embassy.
- **RELS KEEP (3) + ADAPT (3):** R-0002 (Gyeomik–Baedalta), R-0003 (Dhyānabhadra–Naong), R-0018 (Iryŏn documents Marananta) KEEP; R-0009 (Tagore→Han Yong-un), R-0012 (Gandhi→*Muso-yu*), R-0013 (Pŏpchŏng–Vinoba) ADAPT. CONTEXT: legend + literary circle (8). EXCLUDE: diplomacy/colleagues (4).
- **PPL KEEP (17):** B1 monastic links + Pŏpchŏng, Lokesh Chandra, U Myeong-ju, Buddhavara, Hyoseok, Wookwan, Gakseong links. CONTEXT: legend + Tagore links (6). EXCLUDE: Joseon/military/diplomatic/economic links (11).
- **PTX KEEP/ADAPT (14):** Buddhist-authorship links (L-0101..0103, 0107, 0112, 0116, 0118..0120, 0127, 0130, 0131; ADAPT: L-0110 Lamp of the East, L-0121 survey co-editor). CONTEXT: Tagore/literary links (9). EXCLUDE: 9.

## 7. Regeneration & maintenance

- Classification decisions live in `buddhist-bridges/classification_v3.py` (source of truth); the generator validates relevance/scope/movement/connection vocabularies and the relevance→scope mapping (errors on any mismatch; BUILD FAILED until fixed).
- CSV regenerated by `python3 buddhist-bridges/build_classification.py`.
- When V2 records are added/changed, the classifier must cover them before the CSV can rebuild.
