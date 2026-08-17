# Phase 3 Multimodal Network Layer

## Rebuild and validate

From `india-korea-mediators/`:

```bash
python3 buddhist-bridges/analysis/build_network_data.py
python3 buddhist-bridges/analysis/network/network_validation.py
python3 buddhist-bridges/analysis/network/network_analysis.py
python3 buddhist-bridges/analysis/network/network_sensitivity.py
python3 buddhist-bridges/analysis/network/network_readiness.py
python3 buddhist-bridges/analysis/network/build_network_visualization.py
python3 buddhist-bridges/analysis/network/validate_network_mvp.py
```

The builder reads only the immutable `buddhist-bridges/v3.0_frozen/` snapshot plus validated derived tables (`register.csv`, `tradition_taxonomy.csv`, and `institution_mapping.csv`). It writes `network_nodes.csv`, `network_edges.csv`, and `network_audit.md`. The analysis script writes `network_statistics.csv` and `network_findings_v1.md`.

`network_sensitivity.py` performs Network Audit v2: it audits every edge into `network_edge_audit.csv`, calculates diagnostic networks A–F into `network_sensitivity.csv`, and writes `network_audit_v2.md`.

`network_readiness.py` adds the derived `relation_family` field, writes `network_relation_families.csv` and `network_relation_family_centrality.csv`, and writes the final `network_visualization_readiness.md`. It does not build a visualization.

`build_network_visualization.py` embeds the current node, edge, relation-family, and family-centrality tables into `network_mvp.html`. The HTML is self-contained, uses a deterministic layered SVG layout, and has no external dependencies. `validate_network_mvp.py` checks the embedded counts, ontology safeguards, legendary handling, and absence of movement edges.

The MVP uses four readable zones rather than a force-directed graph: PEOPLE (two compact columns), INSTITUTIONS, TEXTS, and EVENTS. Edges are routed between deterministic zone coordinates; clicking a node focuses its documented connections and dims unrelated paths. The full network is intentionally tall so all people remain inspectable without shrinking labels to unreadable size.

## Architecture

The primary graph contains PEOPLE, INSTITUTIONS, TEXTS, and EVENTS. Places and travels are audited but do not become primary nodes, so no physical-movement edge is emitted at this stage. Ten explicit `EP-*` event-participant records are represented as separate event-only people nodes; they are not identity-matched to canonical `P-####` records. Legendary P-0007/P-0008 nodes and their family edge are retained and flagged, but excluded from default statistics.

Edges are explicit only: person-person relationships, person-text AUTHOR/TRANSLATOR links, approved derived institution mappings, event organizers, and person-event participation. Confidence and source IDs are metadata, not weights.
