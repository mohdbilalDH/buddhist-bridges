# Final Network Visualization Readiness Review

**Baseline:** frozen V3.0, validated derived tables, prosopography outputs, and Network Audit v2.

## Decision

**APPROVED — proceed to network visualization**, subject to the claim boundaries and minimal architecture below. No visualization is built in this review.

## Ontology and relation families

The frozen six-type edge ontology is unchanged: PHYSICAL_MOVEMENT, INSTITUTIONAL, TEXTUAL_TRANSMISSION, INDIRECT_INFLUENCE, PERSON_ENCOUNTER, and LEGENDARY. `relation_family` is a derived accounting field; it is not a new edge type.

For all edges, `network_relation_families.csv` assigns either `NON_INSTITUTIONAL` or one of these exact institutional families:

- **PERSON_INSTITUTION** — subtype `INSTITUTION_MAPPING`; explicit normalized person–institution mapping.
- **INSTITUTION_EVENT_ORGANIZER** — subtype `ORGANIZER`; institution explicitly listed as an event organizer.
- **PERSON_EVENT_PARTICIPATION** — subtype `EVENT_PARTICIPATION`; person explicitly linked to an event with a recorded role.

## Family-specific centrality

- **PERSON_INSTITUTION:** 14 edges; 20 incident nodes; 90 components; 84 isolates; node types: INSTITUTIONS=8; PEOPLE=12.
  - Degree candidates: Dongguk University (4), Nalanda Mahavihara (3), Buddhavara (Ven.) (2), Dhyānabhadra (2), Hoeamsa (2).
  - Betweenness candidates: Nalanda Mahavihara (7.000000), Dhyānabhadra (6.000000), Dongguk University (6.000000), Hoeamsa (4.000000), Buddhavara (Ven.) (1.000000).
- **INSTITUTION_EVENT_ORGANIZER:** 22 edges; 31 incident nodes; 82 components; 73 isolates; node types: EVENTS=18; INSTITUTIONS=13.
  - Degree candidates: Jogye Order of Korean Buddhism (5), International Buddhist Confederation (IBC) (4), Bunhwangsa India (2), Hoeamsa (2), Dongguk University - Nalanda University MOU (2).
  - Betweenness candidates: Jogye Order of Korean Buddhism (24.000000), Bunhwangsa India dedication (대웅보전 준공식) (12.000000), Bunhwangsa India (7.000000), Sangwol/Jogye walking pilgrimage India-Nepal (7.000000), International Buddhist Confederation (IBC) (6.000000).
- **PERSON_EVENT_PARTICIPATION:** 13 edges; 22 incident nodes; 91 components; 82 isolates; node types: EVENTS=10; PEOPLE=12.
  - Degree candidates: Korea-India 50th anniversary cultural exchange (Jogye + ROK Embassy) (2), 2nd Global Buddhist Summit (2), Bexpo 2026 Buddhist exchange (IBC - Jogye lay) (2), Abhijit Halder (2), Buddhavara (Ven.) (1).
  - Betweenness candidates: Bexpo 2026 Buddhist exchange (IBC - Jogye lay) (2.000000), Abhijit Halder (2.000000), Korea-India 50th anniversary cultural exchange (Jogye + ROK Embassy) (1.000000), 2nd Global Buddhist Summit (1.000000).

The family-specific results show that institutional centrality is not one stable phenomenon. Dongguk University and Nalanda Mahavihara are prominent in the person–institution family; event nodes and event participants are prominent in the organizer/participation families. These findings are not interchangeable.

### Robustness assessment

- **Robust across institutional families:** no single institution is top-ranked across all three families. Institutional prominence is therefore family-dependent rather than a single robust historical centrality result.
- **Robust in the wider network:** Dhyānabhadra remains structurally prominent in the full, non-institutional, and person–person diagnostics from Audit v2; this is a structural robustness observation, not a claim of historical importance.
- **Not robust across families:** Jogye Order and Dongguk University are prominent in institutional/full structures but do not remain central in the non-institutional or person–text layers.
- The visualization must permit family filtering and must not collapse these families into one undifferentiated institutional edge.

## Historical claims the visualization can make

It can show:

- which documented nodes are connected by which explicit relation family;
- whether a connection is person–institution, institution–event organizer, or person–event participation;
- direction, confidence, historical band, evidence identifiers, and legendary status;
- structural degree/betweenness within the curated graph, clearly labelled as descriptive;
- that B3 is an empty network state under the current carried-record inclusion criteria.

It cannot show:

- who was historically “most important”;
- total Buddhist activity or the complete historical network;
- causality, influence beyond the explicit evidence, or continuity between periods;
- undocumented relationships, inferred acquaintance, or inferred movement;
- geographic movement, because PHYSICAL_MOVEMENT edges are absent from the primary graph;
- absence of Buddhism in B3;
- source count as historical importance.

## Minimal visualization architecture

1. **Layered static view:** PEOPLE, INSTITUTIONS, TEXTS, and EVENTS as distinct node layers; no Places.
2. **Relation-family filter:** PERSON_INSTITUTION, INSTITUTION_EVENT_ORGANIZER, PERSON_EVENT_PARTICIPATION, plus a separate non-institutional view.
3. **Edge encoding:** frozen connection type by color; relation family by dash/panel/filter; direction by arrows where supported; confidence by line style; legendary by distinct styling and off by default.
4. **Node encoding:** shape by node type; historical band as a secondary fill/accent; event-only `EP-*` nodes visibly marked; no size-by-importance scaling.
5. **Controls:** band, relation family, connection type, confidence, direction, corroboration, legendary toggle, and search.
6. **Record card:** every edge exposes endpoint IDs, relation family, frozen underlying record, evidence/source identifier, confidence, and caveat.
7. **B3 state:** explicit empty-state annotation: “No carried records under the current inclusion criteria,” never a visual gap implying no Buddhism.

No force-directed layout is required for the MVP; a layered or small-multiple family view is analytically safer. Community detection, GIS, movement edges, and transmission-chain analysis remain out of scope.

## Reproducibility and validation

Run:

```bash
python3 buddhist-bridges/analysis/network/network_readiness.py
python3 buddhist-bridges/analysis/network/network_validation.py
```

The relation-family file and family-specific centrality table are derived from the current network tables. V3.0 is not modified.
