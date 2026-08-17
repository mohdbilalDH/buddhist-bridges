# Network Audit v2

**Status:** complete; underlying V3.0 remains immutable.

## Data integrity

- Current network tables: **106 nodes, 71 edges**.
- Non-legendary active graph: **104 nodes, 70 edges**.
- Institutional edges: **49**; families: {'LEGENDARY_RELATIONSHIP': 1, 'PERSON_RELATIONSHIP': 10, 'TEXT_LINK': 11, 'PERSON_INSTITUTION_MAPPING': 14, 'INSTITUTION_EVENT_ORGANIZER': 22, 'PERSON_EVENT_PARTICIPATION': 13}.
- Legendary material: **2 nodes, 1 edge**, excluded from default centrality.
- Event-only participant nodes: **10 `EP-*` nodes**, all present in event_participants.csv and kept distinct from canonical people.csv.
- Frozen checksums and network validation pass.

## Edge-semantic audit

- All 71 edges have been audited individually in `network_edge_audit.csv`. Every endpoint exists, every edge uses the approved six-type ontology, and every edge retains its direction, band, confidence, evidence/source field, legendary flag, and underlying record ID.
- No unsupported edge was found. No new ontology type was required.
- The 1 legendary edge is explicitly authorized by R-0001 and is not treated as documented historical connectivity.

## Institutional-edge audit

- Institutional edges dominate numerically because they combine three structurally different explicit constructions: person–institution mappings, institution–event organizer links, and person–event participation links. They are not interchangeable evidence.
- The audit uses only source-row distinctions: `INSTITUTION_MAPPING`, `ORGANIZER`, and `EVENT_PARTICIPATION`. It does not invent finer affiliation categories where the frozen data does not support them.
- This dominance can create an institutional-structure effect: institutions connect many otherwise separate modalities by design. Therefore institutional degree/betweenness cannot be read as historical importance without the sensitivity networks.

## Sensitivity results

- A full documented graph is compared with non-institutional, person–person, person–institution, person–text, and person–event diagnostic graphs in `network_sensitivity.csv`. Degree and betweenness are calculated on undirected projections for comparability; original edge direction remains in the edge table.
- **A_FULL_DOCUMENTED:** 70 edges; 85 incident nodes; 38 components; 19 isolates; degree candidates: Dhyānabhadra (6), Jogye Order of Korean Buddhism (5), Dongguk University (5).
- **B_NON_INSTITUTIONAL:** 21 edges; 33 incident nodes; 83 components; 71 isolates; degree candidates: Dhyānabhadra (4), Pŏpchŏng (3), Rabindranath Tagore (3).
- **C_PERSON_PERSON:** 8 edges; 13 incident nodes; 96 components; 91 isolates; degree candidates: Dhyānabhadra (4), Ch'ukwŏn Chijŏn (1), Sitanshu Yashaschandra (1).
- **D_PERSON_INSTITUTION:** 14 edges; 20 incident nodes; 90 components; 84 isolates; degree candidates: Dongguk University (4), Nalanda Mahavihara (3), Buddhavara (Ven.) (2).
- **E_PERSON_TEXT:** 11 edges; 22 incident nodes; 93 components; 82 isolates; degree candidates: Seong yusik non hakki (1), Morning Calm and The Pensive Beyond (1), Wookwan's Korean Temple Food (1).
- **F_PERSON_EVENT:** 13 edges; 22 incident nodes; 91 components; 82 isolates; degree candidates: Korea-India 50th anniversary cultural exchange (Jogye + ROK Embassy) (2), 2nd Global Buddhist Summit (2), Bexpo 2026 Buddhist exchange (IBC - Jogye lay) (2).

## Event participants

All 10 `EP-*` rows are present in the frozen event_participants.csv and are referenced by person_event.csv. They have no safe identity match in canonical people.csv in the available frozen data. They remain event-only participant nodes; no identity matching was invented.

## Physical movement

No `PHYSICAL_MOVEMENT` edges were created. Places are not primary nodes, so the current network is a **mediation network, not a movement network**. Travels remain available for a future GIS/place layer; no synthetic movement edges were added.

## Legendary material and B3

Legendary nodes and the legendary edge remain identifiable and reproducible, but are excluded from all default sensitivity centrality calculations. B3 is an empty network state under the current carried-record inclusion criteria in every diagnostic graph; this is not evidence of an absence of Buddhism.

## Structural observations vs. historical interpretation

**Observed structural patterns:** institutional edges dominate the full graph; removing them changes the graph substantially; person–text and person–event layers are smaller; person–person encounters are sparse; B3 remains empty.

**Possible historical interpretations:** institutional settings may have functioned as documented channels for connecting people, texts, and events, but the observed institutional prominence is partly produced by the multimodal architecture and explicit organizer/participation encoding. It cannot by itself establish institutional historical importance or causal mediation.

## Recommendation

**REVISE — methodological issues remain.** The data layer passes validation and no ontology problem was found, but the institutional-structure effect and the absence of movement edges should be reviewed before a final network visualization or historical centrality claims.
