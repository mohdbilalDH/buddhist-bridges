# Data Quality Report — Buddhist Bridges V3.0 (FINAL)

**Date:** 2026-08-17 · **Status:** FROZEN · **Audit:** 0 errors / 0 warnings · **Builds:** 0/0 both

## 1. Dataset at a glance

| Table | Rows | Table | Rows |
|---|---|---|---|
| people | 76 | events | 19 |
| places | 39 | person_event | 13 |
| travels | 41 | event_participants | 10 |
| texts | 30 | sources | 187 |
| institutions | 31 | classification | 325 |
| person_person | 22 | person_place | 35 |
| person_text | 32 | | |

Classification: PRIMARY=171, SECONDARY=17, MEDIATOR=19, CONTEXTUAL=46, NONE=85; scope KEEP=171, ADAPT=36, CONTEXT=46, EXCLUDE=85; carry (KEEP+ADAPT)=207; REVIEW=0; people carried=43.

## 2. Quality observations

**Strong:**
- 0 errors / 0 warnings across audit dimensions A–H; both builders green.
- Every carried record has ≥1 source; all source keys resolve (187-key registry).
- All 6 PTX TRANSLATOR links carry evidence notes (fixed this round).
- REVIEW scope empty — no unresolved classification decisions remain.
- Documented negatives preserved and traceable (see provenance audit §3).

**Watch items (accepted, documented):**
1. **Single-source HIGH records** — 5 people + 8 events rest on one institutional source each (list in `provenance_audit_v3.0.md` §3). Corroborate in the next research phase; treat as HIGH-with-caveat until then.
2. **Event confidence** — events were seeded from one primary source each; statuses VERIFIED/PARTIAL/UNCONFIRMED are recorded per event.
3. **B3 (Joseon) near-empty** — see coverage analysis: genuine historical gap, not collection failure.
4. **P-0047 Syed Muzaffar Aga** — Seoul tenure 1974-77 vs 1975-78 discrepancy unadjudicated (minor).
5. **P-0026 Yi Kyu-gyŏng** — India content in Oju yŏnmun changjŏn san'go not yet verified against the 1850s text (research gap).
6. **P-0050 Lee Kun-hee** — corporate India connection verified; personal travel UNCERTAIN.

## 3. What is safe to analyse now (V3.0)

**Safe (HIGH-confidence, multi-source or primary-source):**
- **B1 ancient network**: Hyecho's pilgrimage (T-0001, TX-0001, Fuchs 1938 translation resolved), Woncheuk (P-0002), the Silla monk cluster (P-0003..P-0019), Gyeongheung, Hyeil (P-0010), the 7 sacred sites, Suro/Heo Hwang-ok as LEGENDARY (flagged SPECULATIVE — analyse only as legend, never as fact).
- **B2 Goryeo network**: Jikong circle complete (Naong, Muhak, Baegun, Ch'ukwŏn + R-0019..R-0022), Hoeamsa relic legacy (EV-0017/0018), WOJ display history (EV-0019).
- **B5/B6 contemporary**: 19 events with institutional sources (pilgrimages, GBS, Bunhwangsa India, MOUs, relic returns), 43 carried people, 187 sources.
- **Network structure**: 22 person–person, 35 person–place, 32 person–text links; connection-type and exchange-type distributions (see coverage analysis).

**Not safe (flagged):**
- Any claim of Korean participation in GBS 2023/2026 or ICYBS 2025 (unconfirmed).
- Kim Chi-ha–Gandhi influence (documented negative).
- Suro/Heo Hwang-ok as historical fact (legend).
- "16 Goryeo monks in Yuan-era India/Tibet" (unverified).
- Personal India travel of P-0050 Lee Kun-hee (UNCERTAIN).
- Any single-source event as sole evidence for a strong claim.

## 4. Recommended next-phase priorities (after freeze)

1. Corroborate the 8 single-source events + 5 single-source people.
2. B5 gap: 1950s–60s Korean monks in India pre-Pŏpchŏng (Nav Nalanda archives unchecked).
3. B5 gap: 1960s–70s organised pilgrimages; post-1973 embassy-sponsored events.
4. B3: verify Yi Kyu-gyŏng's India entries (only realistic Joseon-era lead).
5. §7 open questions in collect_next.md (GBS/ICYBS Korean participation; distinct 2026 Jogye pilgrimage; Piparhawa).