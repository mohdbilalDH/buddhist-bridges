# Network Findings v1 — Descriptive Initial Analysis

**Scope:** static, unweighted primary multimodal graph; legendary nodes/edges excluded by default. These are descriptive observations, not importance rankings.

- The graph contains **104 active nodes** and **70 explicit edges**.
- Isolated active nodes: **19**. Isolation means no edge in this primary architecture, not historical irrelevance.
- Edge types: {'PERSON_ENCOUNTER': 8, 'INDIRECT_INFLUENCE': 2, 'TEXTUAL_TRANSMISSION': 11, 'INSTITUTIONAL': 49}.
- Direction labels: {'UNDIRECTED': 8, 'UNCERTAIN': 2, 'PERSON_TO_TEXT': 11, 'PERSON_TO_INSTITUTION': 14, 'INSTITUTION_TO_EVENT': 22, 'PERSON_TO_EVENT': 13}; undirected encounters remain undirected.

## Mediation observations

- Institutional edges are the largest explicit edge class in this graph, while textual transmission and person encounters form smaller typed layers. This is a property of the curated edge construction, not a claim that institutions were historically more important.
- The primary graph does not include PHYSICAL_MOVEMENT edges because Places are excluded as primary nodes. Travel is therefore not silently converted into person-person or person-event ties.
- Degree and betweenness are reported as structural descriptors. A high value identifies a bridge candidate for qualitative review, not an importance ranking.

## Highest structural values (review candidates, not rankings)

Degree projection: Dhyānabhadra (6), Jogye Order of Korean Buddhism (5), Dongguk University (5), Pŏpchŏng (4), International Buddhist Confederation (IBC) (4)

Betweenness in undirected projection: Jogye Order of Korean Buddhism (73.000), Bunhwangsa India dedication (대웅보전 준공식) (62.000), Bunhwangsa India (54.000), Buddhavara (Ven.) (36.000), Dhyānabhadra (34.000)

## Period caution

- B3 is retained as an empty network state because there are no carried records under the current inclusion criteria. This must not be interpreted as an absence of Buddhism.
- Band counts should not be read as continuous connectivity or compared without the source-density and inclusion-criteria context established by the Timeline and prosopography reports.
- Community detection was not run; the approved design warns that it would overfit this small heterogeneous graph.

## Key question status

The data layer supports comparing direct person encounters with institutional, textual, and event-mediated edges. It does not yet establish which mechanism dominated historically; that requires band-aware, source-aware interpretation and review of the explicit edges.
