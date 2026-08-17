# Buddhist Bridges — Collect Next: Prioritized Exact List (v0.2)

**Date:** 2026-08-17 · **Rule:** per the user's instruction, NO large record additions yet. This list is the exact, prioritized set of what to collect when the green light is given. Each item names the record type, proposed ID, content, and source(s).

Status legend: **READY** = confirmed by sources, addable immediately · **RESEARCH** = needs one more targeted search round · **WAIT** = do not add yet.

## 0. Progress log (2026-08-17, third execution round)

**V3.0 FREEZE round — COMPLETED (2026-08-17):**
- Dataset FROZEN at V3.0: `buddhist-bridges/v3.0_frozen/` (13 CSVs + VERSION.md manifest).
- Final audit `audit_v3.py`: **0 errors / 0 warnings — AUDIT PASSED** (dimensions A–H).
- Normalization (no new records): P-0008 movement `legendary`→`-`; P-0061 movement `-`→`studied`; 7 sacred sites MONASTERY→SITE (PL-0010, PL-0032..0037; `SITE` added to PLACE_TYPES); 6 PTX TRANSLATOR links gained evidence notes (L-0113/114/115/122/123/125); P-0037/P-0073 period MODERN→CONTEMPORARY.
- Final builds: build_dataset.py 0/0 (people=76, rels=22, events=19, person_event=13, sources=187); build_classification.py 0/0 (PRIMARY=171, KEEP=171, MEDIATOR=19, SECONDARY=17, REVIEW=0, carry=207, people carried=43).
- Deliverables written: `schema/data_dictionary_v3.0.md`, `schema/controlled_vocabularies_v3.0.md`, `buddhist-bridges/schema_v3.md` (status FINAL v3.0), `buddhist-bridges/provenance_audit_v3.0.md`, `buddhist-bridges/data_quality_report_v3.0.md`, `buddhist-bridges/coverage_analysis_v3.0.md`, `buddhist-bridges/unresolved_v3.0.md`; `docs/unresolved_cases.md` §1.2/§1.4 updated to the P5 closures.
- **STOPPED per user instruction**: no GIS/network analysis, no website, no new collection. Next phase begins only on approval; this list below is the exact prioritized set for that phase.

**COMPLETED this round:**
- §1 P1 EVENTS: EV-0001..EV-0014 seeded; builds green.
- §2 P1: I-0022..I-0029, PL-0032..PL-0039 added.
- §3: 12 source keys appended (registry at 177 keys).
- §7 Q1 (GBS participation): CLOSED — GBS 2023 = Jeongbeom (hyunbulnews_gbs2023); 2nd GBS 2026 = Munjong/Jinwoo message (tongbulgyo_gbs2026); ICYBS 2025 = no Korea (ibcworld_icybs2025, pib_icybs2025).
- §7 Q2 (distinct 2026 pilgrimage): CLOSED — KBPF 2026 (EV-0012) + BBS Seon Tour (EV-0013) are distinct 2026 programs; no separate Jogye 2026 pilgrimage found.
- §7 Q3 (Piparhawa): CLOSED — no Korean participation documented (negative result, southasiatime_piparhawa2026).
- §5 B5: **1982 국제불교문제연구소 6-member delegation** — PRIMARY SOURCE retrieved from Naver News Library API (Dong-A 1982-01-19 p.6): EV-0015, I-0030, EP-0010 (+donga_delegation_1982).
- §5 B5: **Hwang Su-yŏng 1962-63** — PRIMARY SOURCE retrieved (Kyonghyang 1963-05-11 p.5): P-0073, T-0042, L-0035 (+kyunghyang_hwang_1963).
- §6 P3 (partial): **Dongguk–Nalanda University MOU 2023-02-24** — EV-0016, I-0031 (+hyunbul_dongguk_nalanda).
- Builds: build_dataset.py 0 errors/0 warnings (people=72, travels=41, institutions=31, events=16, person_event=12, event_participants=10, sources=177); build_classification.py 0/0 (PRIMARY=167, KEEP=167, carry=194, people carried=38; B5=52, B6=118).

**P4 (B2) round — COMPLETED:**
- Jikong circle verified and CORRECTED: circle = Naong / Muhak / Baegun / Ch'ukwŏn (NOT Ch'anyŏng / T'aego Pou — earlier assumption wrong).
- Added P-0074 Muhak Chach'o (MEDIATOR/ADAPT), P-0075 Baegun Gyeonghan (SECONDARY/ADAPT), R-0019, R-0020, EV-0017 (1370 relic stupa for Jikong at Hoeamsa), EV-0018 (2024 Boston MFA relic return to Hoeamsa), PERSON_EVENT P-0024@EV-0017 (ORGANIZER); +5 source keys (registry at 182).
- "16 Goryeo monks in Yuan-era India/Tibet" claim: UNVERIFIED (negative so far — only generic Mongolian Empire material).
- §6 B1: **WOJ record ADDED** — EV-0019 (world-first public display of the BnF manuscript at NMK 2010-11; second loan 2019-20); +3 source keys (museum_woj_2010, kbs_woj_2010, hani_woj_2019); Fuchs translation year disputed (1928 vs 1938) — flagged for encykorea verification.
- Builds: build_dataset.py 0/0 (people=74, rels=20, events=19, person_event=13, sources=185); build_classification.py 0/0 (PRIMARY=171, KEEP=171, MEDIATOR=20, SECONDARY=13, carry=202, people carried=40; B2=19, B6=120).

**P5 (REVIEW closure + B5 sweep + B2/B1 resolution) round — COMPLETED:**
- §4 REVIEW **CLOSED (both)**: P-0068 Sŏ Chŏng-ju → VERIFIED India link (Dongguk University newspaper 동대신문, reposted 2010-08-11: Indian Gujarati poet Sitanshu Yashaschandra visited Dongguk and met Sŏ; discussed Indian poetry + Korean-Indian literary exchange; proposed mutual translation and a '자비회' society; visit year unstated, ~1970s) → SECONDARY/ADAPT/B5/(ENCOUNTER); P-0070 Kim Chi-ha → documented NEGATIVE (Hani 2026-07-03 interview with 임진택: Kim's thought is Donghak-rooted — 시천주/향아설위, 증산도 개벽사상, Buddhism, Christianity; no Gandhi/India influence) → NONE/EXCLUDE/B5/(INDIRECT).
- Added P-0076 Sitanshu Yashaschandra (Indian poet, SECONDARY/ADAPT/B5/(ENCOUNTER)) + R-0021 (P-0068–P-0076 MET_IN_PERSON); +2 source keys (donggukmedia_seo_yashaschandra, hani_kimchiha_2026; registry at 187).
- §5 B5 sweep: **Kelaniya–Bongeunsa sisterhood (agreed Dec 1981, Dong-A 1982)** — no evidence of realisation (English + Korean searches; only find: BBSI 2018-06-24 Bongeunsa Korean-Sri Lankan cultural exchange, a residents' event, not the twinning) → documented negative. **Nav Nalanda Mahavihara pre-Pŏpchŏng Koreans** — no Korean students documented in Nalanda literature (Wikipedia: only "few Indian and foreign students" after Bihar restoration; no Korean names); corroborated by Hwang Su-yŏng's 1963 note of absent Korean students → documented negative.
- §6 B2: **Ch'ukwŏn Chijŏn ADDED** — P-0077 (축원 지천, 竺源 智泉, 1324–1395, 정지국사; Jikong's disciple per tradition; SECONDARY/ADAPT/B2/(INDIRECT)) + R-0022 (P-0023–P-0077 TEACHER_STUDENT). Jikong circle now complete: Naong / Muhak / Baegun / Ch'ukwŏn.
- §6 B1: **Fuchs year RESOLVED — 1938**: bibliographic record (W. Fuchs, *Huei-ch'ao's Pilgerreise durch Nordwest-Indien und Zentral-Asien um 726*, Sitzungsberichte der Preußischen Akademie der Wissenschaften, Phil.-hist. Klasse XXX, 1938; pub. 1939 per KCI 이재원 2016) vs encykorea E0039126 "1928" — the 1928 date is an error (contradicted by the primary bibliographic record and the peer-reviewed KCI article); TX-0001 notes updated.
- Builds: build_dataset.py 0/0 (people=76, rels=22, events=19, person_event=13, sources=187); build_classification.py 0/0 (PRIMARY=171, KEEP=171, MEDIATOR=19, SECONDARY=17, REVIEW=0, carry=207, people carried=43; B2=21, B5=54, B6=120).

**REMAINING (see §4-§5):** §4 candidates Paek Yong-sŏng / Kim Iryŏp / Pang Han-am (still RESEARCH, not records); §5 1950s–60s Korean monks in India before Pŏpchŏng + 1960s–70s organised pilgrimages + post-1973 embassy-sponsored events beyond EV-0014.

---


## 1. P1 — EVENTS table records (11 confirmed events, READY)

Create the EVENTS table per `schema_v3.md` §3 and seed it with the confirmed contemporary developments. Contemporary actors (Jung Won-ju, Abhijit Halder, Wonhaeng) appear as `participant_person_ids` at event level — they do NOT become PEOPLE records.

| Proposed ID | Event (from proposal_v3.md E-series) | Date | Where | Primary source(s) |
|-------------|--------------------------------------|------|-------|-------------------|
| EV-0001 | Sangwol 1167-km / 43-day walking pilgrimage (108+ monastics) | 2023 | Bodh Gaya → Sarnath | PIB PRID=1896682 (in registry) |
| EV-0002 | Bexpo 2026 Buddhist lounge: IBC–Jogye lay exchange | 2026-04-04 | New Delhi | Korea Herald 10713686 (in registry) |
| EV-0003 | 2nd Global Buddhist Summit | 2026-01-24/25 | New Delhi (Vigyan Bhawan) | ddnews_gbs2026 (pending key) — no Korean in speaker list |
| EV-0004 | Jungto annual India pilgrimage program (35th: early 2026; 36th: 2027-01-14~30) | annual | Bodh Gaya region | jungto_india (in registry) |
| EV-0005 | Delhi University – BGICBS MOU | 2026-04-23 | Delhi | Korea Herald 10713686 (in registry) |
| EV-0006 | Jogye delegation Sarnath → Bodh Gaya (May 2022) | 2022-05 | Sarnath/Bodh Gaya | beopbo_2022_jogye (in registry) |
| EV-0007 | Jogye pilgrimage: 8 Indian sites + Nepal incl. Yeoraesunwon | 2014 | India/Nepal | jogyesa_2014_pilgrimage (in registry) |
| EV-0008 | Bunhwangsa India groundbreaking | 2020-03-28 | Bodh Gaya | ibulgyo_bunhwangsa_2020 (pending) |
| EV-0009 | Bunhwangsa India dedication (대웅보전 준공식; 150-person delegation led by 총무원장 Wonhaeng) | 2022-05 | Bodh Gaya | hyunbulnews_bunhwangsa_2022, buddhismorkr_bunhwangsa_2022, koreatimes_bunhwangsa_2022 (pending) |
| EV-0010 | Global Buddhist Summit 2023 | 2023-11 (approx.) | New Delhi | ibcworld_gbs2023, drishtiias_gbs2023 (pending) — Korea presence unconfirmed |
| EV-0011 | ICYBS 2025 — 3rd Int'l Conf. of Young Buddhist Scholars | 2025-08 | New Delhi (Dr Ambedkar Int'l Centre) | ddindia_icybs2025 (pending) — Korea unconfirmed |

## 2. P1 — Institutions (5, READY) and Places (7, READY)

| Proposed ID | Name | Band | Source(s) |
|-------------|------|------|-----------|
| I-0022 | Jogye Order of Korean Buddhism (대한불교조계종) | B6 | PIB, beopbo_2022_jogye, hyunbulnews_bunhwangsa_2022 |
| I-0023 | Sangwol Society (상월결사) — 2023 pilgrimage organizer | B6 | PIB PRID=1896682 |
| I-0024 | Jungto Society (정토회) | B6 | jungto_india |
| I-0025 | Yeoraesunwon (여래선원), Bodh Gaya — Korean temple, founded ~2000–01; abbot Wonman sunim; 달마학교 (Dharma School) | B6 | beopbo_yeoraesunwon (pending) |
| I-0026 | International Buddhist Confederation (IBC), New Delhi | B6 | ibcworld_gbs2023, Korea Herald 10713686 |

| Proposed ID | Name | Band | Notes |
|-------------|------|------|-------|
| PL-0032 | Sarnath (Varanasi) | B6 | 2023 pilgrimage endpoint; EV-0006 |
| PL-0033 | Kushinagar | B6 | 2023 route; 2014 itinerary |
| PL-0034 | Lumbini (Nepal) | B6 | 2023 route; 2014 itinerary |
| PL-0035 | Vaishali | B6 | 2023 route |
| PL-0036 | Shravasti | B6 | 2023 route |
| PL-0037 | Rajgir / Vulture Peak | B6 | 2023 route; Nalanda proximity |
| PL-0038 | Kapilavastu | B6 | 2023 route |

## 3. P1 — Source registry: append 12 pending keys (READY)

Append to `data_sources.py` (slug, description, type, url, publisher, reliability):

1. `hyunbulnews_bunhwangsa_2022` — NEWS — https://www.hyunbulnews.com/news/articleView.html?idxno=405034 — Hyunbul News (2022-05-19): 150-person Jogye delegation, 총무원장 Wonhaeng, "공식대표단 첫 순례", Bunhwangsa India dedication — INSTITUTIONAL
2. `ibulgyo_bunhwangsa_2020` — NEWS — https://www.ibulgyo.com/news/articleView.html?idxno=204382 — Ibulgyo (2020-02-06): Bunhwangsa construction start 2020-03-28, 2022 completion target — INSTITUTIONAL
3. `buddhismorkr_bunhwangsa_2022` — NEWS — buddhism.or.kr board view (2022): 대웅보전 준공식, 36th administration's 2019-04 백만원력결집 — INSTITUTIONAL
4. `koreatimes_bunhwangsa_2022` — NEWS — https://www.koreatimes.net/ArticleViewer/Article/146716 — Korea Times (2022-05-24): Jogye 성지순례단 — POPULAR
5. `beopbo_yeoraesunwon` — NEWS — https://www.beopbo.com/news/articleView.html?idxno=66399 — Beopbo (2011-06-30): Yeoraesunwon 10-year alms operation, Wonman abbot, Dharma School — INSTITUTIONAL
6. `ibcworld_gbs2023` — WEBSITE — https://ibcworld.org/events/view/35 — IBC: GBS 2023, 700+ delegates, ~175 overseas from 31 countries — INSTITUTIONAL
7. `drishtiias_gbs2023` — NEWS — drishtiias.com (2023): GBS 2023, 173 international participants incl. 84 Sangha — POPULAR
8. `ddnews_gbs2026` — NEWS — https://ddnews.gov.in/en/second-global-buddhist-summit-to-be-held-in-delhi-on-january-24-25/ — DD News (2026-01-18): 2nd GBS speakers, ~200 delegates/800+ overall, 5 thematic sessions; no Korean named — INSTITUTIONAL
9. `ddindia_icybs2025` — NEWS — ddindia.co.in (2025-08): ICYBS 3rd, Dr Ambedkar Int'l Centre, IBC + Ministry of Culture — POPULAR
10. `ggbn_delhi_pune` — NEWS — https://www.ggbn.co.kr/news/articleView.html?idxno=38055 — Korean Buddhist outlet (2019-03-19): Delhi University and Pune University are the most-chosen universities by Korean Buddhist-students — POPULAR
11. `encykorea_kim_iryeop` — WEBSITE — http://encykorea.aks.ac.kr/Contents/Item/E0010283 — EncyKorea (AKS): Kim Iryŏp biography — INSTITUTIONAL
12. `wiki_paek_yongsong` — WEBSITE — https://ko.wikipedia.org/wiki/백용성 — Korean Wikipedia: Paek Yong-sŏng (verification aid only, low reliability) — POPULAR

## 4. P2 — REVIEW closure research (CLOSED for P-0068/P-0070; candidates still RESEARCH)

**CLOSED (2026-08-17):**
- **P-0068 Sŏ Chŏng-ju → VERIFIED India link** (SECONDARY/ADAPT/B5/(ENCOUNTER)): Dongguk University newspaper (동대신문, reposted 2010-08-11) documents Indian Gujarati poet Sitanshu Yashaschandra's visit to Dongguk University and meeting with Sŏ (문리대학장, ~1970s); discussed Indian poetry's mainstream/state and Korean-Indian literary exchange; Yashaschandra praised Sŏ's Hwasa (화사) for compassion (자비심); proposed mutual poetry translation and a '자비회' literary society. No evidence of Sŏ himself visiting India → travel question closed as NO.
- **P-0070 Kim Chi-ha → documented NEGATIVE** (NONE/EXCLUDE/B5/(INDIRECT)): Hani 2026-07-03 (강성만; interview with 임진택, '김지하를 다시 본다') documents his life philosophy as Donghak-rooted (시천주/향아설위), 증산도 개벽사상, Buddhism, Christianity — no Gandhi/ahimsa/India influence documented.

Still RESEARCH (candidates, NOT records):

## 5. P2 — B5 verification (RESEARCH)

**DONE (third round):** 1982 국제불교문제연구소 6-monk delegation (EV-0015, I-0030, EP-0010 — Dong-A 1982-01-19 primary); Hwang Su-yŏng 1962-63 (P-0073, T-0042, L-0035 — Kyonghyang 1963-05-11 primary); embassy-sponsored 50th-anniversary exchange (EV-0014, I-0029).

**DONE (P5 round, documented negatives):**
- Kelaniya Temple (Sri Lanka) – Bongeunsa sisterhood (agreed Dec 1981 per Dong-A 1982): no evidence of realisation in English or Korean searches; only find = BBSI 2018-06-24 Bongeunsa Korean-Sri Lankan cultural exchange (bbsi.co.kr idxno=885759 — a Sri Lankan-residents event, not the twinning). Treat as documented negative unless an archive hit surfaces.
- Nav Nalanda Mahavihara pre-Pŏpchŏng Koreans: no Korean students documented in Nalanda mahavihara literature (Wikipedia: only "few Indian and foreign students" post-Bihar-government restoration; no Korean names); Hwang Su-yŏng's 1963 regret about absent Korean students corroborates.

Still open:
- 1950s–60s Korean monks studying in India before Pŏpchŏng (1971) — searches NEGATIVE so far; Nav Nalanda Mahavihara archives (hosted Asian monks from the 1950s) unchecked.
- 1960s–70s organised Korean pilgrimages before the 1980s boom.
- Temple twinning: Dong-A 1982 reports an agreed Kelaniya Temple (Sri Lanka) – Bongeunsa sisterhood (Dec 1981); verify if realised; hunt other twinnings.
- Post-1973 institutional contacts (embassy-sponsored Buddhist events beyond EV-0014).

## 6. P4 — B2 and B1 refinements (RESEARCH; in progress)

- B2 **Jikong circle — COMPLETE (2026-08-17)**: Naong (P-0024), **Muhak Chach'o (P-0074)**, **Baegun Gyeonghan (P-0075)**, **Ch'ukwŏn Chijŏn (P-0077, added — 축원 지천, 竺源 智泉, 1324-1395, 정지국사; SECONDARY/ADAPT/B2/(INDIRECT); R-0022 TEACHER_STUDENT with P-0023)**. Ch'anyŏng (목암 찬영) and T'aego Pou are NOT Jikong-circle members (Taego's inka came from Shiwu Qinggong; Ch'anyŏng is Taego's disciple) — do not add them as Jikong-circle records.
- B2 **Hoeamsa Nalanda-model**: recorded as "reportedly modeled on Nalanda" (P-0023/I-0003) — tradition-based (Jikong's own terrain remark); Nalanda destroyed 1193 vs Jikong's claimed study there → scholarly skepticism (Jahyeon 2017); archaeology shows Goryeo-style terraced layout; UNESCO tentative list 2022, priority list 2025-03-19. No new record needed beyond existing notes.
- B2 **Relic legacy — ADDED**: EV-0017 (1370 relic stupa for Jikong at Hoeamsa; Kongmin's order; Naong supervised — Dongguk Buddhist Culture Portal) and EV-0018 (2024 return of Jikong/Naong + Buddha relics from Boston MFA to Hoeamsa; relics of India provenance).
- B2 **"16 Goryeo monks in India/Tibet (Yuan era)" — UNVERIFIED**: targeted searches returned only generic Mongolian Empire material; treat as a documented negative unless a Korean academic source (KCI/encykorea) surfaces.
- B1: *Wang ocheonchukguk jeon* (WOJ) translation/edition history — **EV-0019 ADDED** (world-first public display of the BnF manuscript at NMK, 18 Dec 2010 - 3 Apr 2011; second BnF loan Dec 2019 - Apr 2020; sources: museum_woj_2010, kbs_woj_2010, hani_woj_2019). Translation milestones confirmed: **Fuchs German translation = 1938 RESOLVED** (W. Fuchs, *Huei-ch'ao's Pilgerreise durch Nordwest-Indien und Zentral-Asien um 726*, Sitzungsberichte der Preußischen Akademie der Wissenschaften, Phil.-hist. Klasse XXX, 1938; pub. 1939 per KCI 이재원 2016 — encykorea E0039126's "1928" is an error contradicted by the bibliographic record and the peer-reviewed KCI article; TX-0001 notes updated); Ch'oe Nam-sŏn 1943 Korean introduction (Hani); 지안/정수일 editions noted in TX-0001 context.

## 7. Open questions — one targeted research round will settle these (RESEARCH)

1. Korean participation in GBS 2023, 2nd GBS 2026, ICYBS 2025 — no Korean appears in the published 2026 speaker list; search Korean Buddhist press (불교신문, beopbo, hyunbulnews) for "글로벌불교정상회의".
2. Is there a distinct "2026 Jogye pilgrimage" event, or is 2026 coverage = the Jungto program + GBS + Bexpo?
3. Piparhawa relics exhibition ↔ Korea: any Korean delegation/participation at the Modi-inaugurated exhibition (Jan 2026)?

## 8. Explicitly NOT to add yet (WAIT)

- **Pomnyun Sunim** (Jungto founder) — no PEOPLE record until a documented India activity is sourced beyond the program page (Jungto's India program is documented; his personal India movement is not yet).
- **Jung Won-ju, Abhijit Halder, Wonhaeng** — event-level participants only; no PEOPLE records.
- **Do-eom sunim** (Indian-ordained Korean monk in Korea) — YouTube-only source; nothing until a named institutional source appears.
- **GBS 2023/2026 and ICYBS 2025 Korean participation** — no claim until sourced; EVENTS records stand as-is with the unconfirmed flag.
- **Paek Yong-sŏng, Kim Iryŏp, Pang Han-am** — not records yet; candidates pending the P2 research.
- **No bulk V3 record additions of any kind** until this list is approved item by item.

## 9. Suggested execution order

1. Append the 12 source keys (§3) — 5 minutes, unlocks everything else.
2. Add I-0022..I-0026 and PL-0032..PL-0038 (§2) to `data_links_2.py` / `data_links_1.py`.
3. Add EVENTS table module (`data_events.py`) + `build_dataset.py` integration; seed EV-0001..EV-0011 (§1).
4. Re-run `build_dataset.py` and `build_classification.py`; classify the new records (all PRIMARY/INSTITUTIONAL, B6).
5. One targeted research round (§7) → close or flag REVIEW items (§4) → B5 verification (§5).
