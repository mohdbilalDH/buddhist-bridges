# Network Data Audit — Phase 3, Step 1

**Baseline:** frozen V3.0, validated derived tables, prosopography outputs. Frozen inputs were read-only.

## Frozen inventory

- **people.csv:** 76 rows
- **institutions.csv:** 31 rows
- **texts.csv:** 30 rows
- **events.csv:** 19 rows
- **person_person.csv:** 22 rows
- **person_place.csv:** 35 rows
- **person_text.csv:** 32 rows
- **person_event.csv:** 13 rows
- **event_participants.csv:** 10 rows
- **travels.csv:** 41 rows

## Scope reconciliation

- **PEOPLE:** 43 carried records (classification KEEP/ADAPT)
- **INSTITUTIONS:** 19 carried records (classification KEEP/ADAPT)
- **TEXTS:** 13 carried records (classification KEEP/ADAPT)
- **EVENTS:** 19 carried records (classification KEEP/ADAPT)
- Canonical carried primary nodes: 43 PEOPLE, 19 INSTITUTIONS, 13 TEXTS, 19 EVENTS.
- Additional explicit event-participant PEOPLE nodes: 10 (`EP-*`); these are not canonical `people.csv` identities.
- Legendary `P-0007`/`P-0008` nodes are retained separately and off by default in scholarly interpretation.

## Edge construction decisions

- Built **71 deduplicated edges** from explicit person-person, person-text, institution mapping, organizer, and person-event records.
- Places and travels were audited but are not primary network nodes. Therefore no PHYSICAL_MOVEMENT edge is emitted in this primary graph; adding place endpoints would change the approved node architecture. Travel evidence remains available for a later place/network view.
- `SUBJECT`, `COLLEAGUE`, `FAMILY` (except the explicit P-0007/P-0008 legend), and unsupported relationship rows are not silently converted into historical transmission edges.
- Confidence and source counts are metadata/style fields, never edge weights.

## Direction, confidence, and missingness audit

- People directionality: {'BIDIRECTIONAL': 9, 'INDIA_TO_KOREA': 44, 'UNCERTAIN': 6, 'KOREA_TO_INDIA': 17}.
- Person-person relationship kinds: {'FAMILY': 1, 'MET_IN_PERSON': 5, 'TEACHER_STUDENT': 4, 'TRANSLATOR_OF': 3, 'INFLUENCED': 4, 'COLLEAGUE': 4, 'DOCUMENTED': 1}; confidence: {'SPECULATIVE': 1, 'MEDIUM': 13, 'HIGH': 8}.
- Person-text link types: {'AUTHOR': 21, 'TRANSLATOR': 6, 'SUBJECT': 5}; confidence: {'HIGH': 32}.
- Person-event roles: {'REPRESENTATIVE': 5, 'SPEAKER': 1, 'DELEGATION_LEADER': 1, 'HOST': 2, 'ORGANIZER': 2, 'MONASTIC_LEADER': 1, 'PARTICIPANT': 1}; confidence: {'MEDIUM': 2, 'HIGH': 11}.
- Travel date precision: {'APPROX': 3, 'YEAR': 23, 'UNKNOWN': 14, 'DECADE': 1}; undated travel starts: 14.
- Person-place links without year: 5; legendary person-place links: 1.
- Legendary canonical people: ['P-0007', 'P-0008']; legendary person-person edges retained: 1 and flagged.

- Frozen classification connection vocabulary observed: {'PHYSICAL_MOVEMENT; TEXTUAL_TRANSMISSION': 7, 'TEXTUAL_TRANSMISSION': 68, 'PHYSICAL_MOVEMENT; INSTITUTIONAL': 16, 'LEGENDARY': 5, 'PHYSICAL_MOVEMENT': 92, 'PHYSICAL_MOVEMENT; INSTITUTIONAL; PERSON_ENCOUNTER': 1, 'PERSON_ENCOUNTER': 15, 'INDIRECT_INFLUENCE': 32, 'TEXTUAL_TRANSMISSION; PERSON_ENCOUNTER': 1, 'INDIRECT_INFLUENCE; PERSON_ENCOUNTER': 1, 'INDIRECT_INFLUENCE; TEXTUAL_TRANSMISSION': 1, 'PHYSICAL_MOVEMENT; PERSON_ENCOUNTER': 1, '-': 42, 'INSTITUTIONAL': 55, 'TEXTUAL_TRANSMISSION; INSTITUTIONAL': 1}.

## Counts

```text
INDIRECT_INFLUENCE: 2
INSTITUTIONAL: 49
LEGENDARY: 1
PERSON_ENCOUNTER: 8
TEXTUAL_TRANSMISSION: 11
```

## Review flags

- The frozen event-participant table contains 10 `EP-*` people not present in `people.csv`; they are represented as separate event-only nodes rather than identity-matched.
- The primary graph intentionally has no `PHYSICAL_MOVEMENT` edges because Places are excluded as primary nodes. Review whether a later secondary place view is desired.
