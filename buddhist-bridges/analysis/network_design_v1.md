# Network Design v1 — Structure Without Overclaiming

**Phase:** 2 — Analysis Design · **Date:** 2026-08-17 · **Baseline:** frozen V3.0
**Answers:** Q1.1, Q1.2, Q1.4, Q1.5, Q2.2 (see `analysis_blueprint_v1.md` §3)

---

## 1. Principle

The network is **small (43 people, 19 institutions, 13 texts, 19 events)** and **heterogeneously sourced**. The design therefore favors: typed edges over untyped ones, explicit direction over symmetry, evidence encoding over fake weights, and per-band snapshots over one misleading aggregate graph.

## 2. Node types (decision + rationale)

| Node layer | Nodes | Source | Role |
|---|---|---|---|
| PEOPLE | 43 carried | people.csv | primary actors |
| INSTITUTIONS | 19 carried | institutions.csv | organizational anchors |
| TEXTS | 13 carried | texts.csv | transmission objects |
| EVENTS | 19 | events.csv | temporal developments |

**PLACES are NOT network nodes in the main view.** They are geographic anchors (the GIS layer's job). A secondary "place network" (places connected by travels) may be built later as a derived view, but the primary analysis is people–institution–text–event.

**Rationale:** mixing 32 places into a 43-person network would inflate degree counts with geography, not relationships.

## 3. Edge types (from the frozen connection_type vocabulary)

| Edge type | Built from | Directionality |
|---|---|---|
| PHYSICAL_MOVEMENT | travels.csv (person → origin/dest places) + movement_status | directed (origin → destination) |
| TEXTUAL_TRANSMISSION | person_text.csv (AUTHOR/TRANSLATOR/READ/INFLUENCED_BY) + texts.author_person_id | directed (author → text; translator → text) |
| INSTITUTIONAL | institution_org mapping (person → I-####) + events.organizer_institution_ids + person_event roles | directed (person → institution; institution → event) |
| PERSON_ENCOUNTER | person_person.csv (MET_IN_PERSON) | undirected |
| INDIRECT_INFLUENCE | person_person.csv (INFLUENCED, DOCUMENTED) + direction_of_influence | directed (influencer → influenced) |
| LEGENDARY | P-0007/P-0008 links | undirected, distinct styling, toggleable |

**Edge count estimate (carried):** ~10 RELS + ~14 PTX + ~18 PPL (as person–place, used only in the place view) + ~13 PERSON_EVENT + ~26 travels (person–place) + institution mapping (~20–30 person–institution edges) + event organizers (~15 institution–event edges). Total ≈ 100–130 edges — small enough for full manual inspection, which is itself a quality control.

## 4. Directionality

- Directed where evidence supports: TEACHER_STUDENT (teacher → student), AUTHOR/TRANSLATOR (person → text), influence (per `direction_of_influence`: INDIA_TO_KOREA / KOREA_TO_INDIA / BIDIRECTIONAL), travel (origin → destination).
- Undirected: MET_IN_PERSON, RESIDENCE, co-participation.
- **BIDIRECTIONAL and UNCERTAIN are rendered as such** (double-headed / dashed arrows) — never forced to one direction.

## 5. Weighting (decision)

| Option | Verdict |
|---|---|
| Unweighted edges | **Primary view.** No frequency data exists; weights would be fabricated. |
| Weight = number of distinct connection types between a pair | **Secondary view** (multiplicity), labeled as such. |
| Weight = confidence | **No** — confidence is an encoding (line style), not a magnitude. |
| Weight = source count | **No** — conflates evidence with importance. |

## 6. Temporal network possibilities

- **Static per-band snapshots (primary):** B1, B2, B4, B5, B6 — each with its own node set and edges active in that band. **B3 renders as an empty state with the annotation** ("no carried records — Joseon"), never as a missing panel.
- **Stepped transitions (secondary):** B1 → B2 → B4 → B5 → B6, showing node/edge turnover (who disappears, what institutions appear). Answers Q2.2 (person-mediated → institution-mediated).
- **Event-anchored temporal edges:** events carry dates; person–event edges are active only at the event date.
- **No continuous animation** (implies continuity; rejected).

## 7. Metrics (with n-caveats)

| Metric | Use | Caveat |
|---|---|---|
| Degree | hub identification (institutions, e.g., Dongguk University, Jogye Order) | descriptive only |
| Betweenness | mediator identification (cross-check against the 19 MEDIATOR records) | n too small for inference; report as observation |
| Components | disconnected clusters per band (e.g., B1 Silla cluster vs B6 institutional cluster) | expected; the *absence* of a B3 component is the finding |
| Density | per-band comparison | must be read against source density (B6's density is partly source-driven) |
| Two-mode projections | people×institutions, people×texts, people×events | the workhorse views for Q1.2 |

**Rejected:** community detection as evidence (43 nodes — will overfit; exploratory only, clearly labeled), centrality as "importance" claims, force-directed layout as the primary analytical view (layout is cosmetic; use it only for exploration).

## 8. Layout and rendering

- Layout: layered (people center, institutions/texts/events around) or bipartite projections; force-directed only as an exploratory toggle.
- Edge styling: color = connection type; line style = confidence (solid/dashed/dotted); hatching = single-source; arrowheads = direction.
- Node styling: shape = layer (people circle, institution square, text diamond, event triangle); fill = band or tradition; badge = single-source; ◈ = legendary.
- Tooltip: record card with evidence + sources.

## 9. How the five data limitations appear

| Limitation | Rendering |
|---|---|
| B3 zero carried | Empty-state snapshot with annotation; the network never "bridges" B2→B4. |
| B1 small primary core | B1 graph shows its ~18 people with solid/dashed styling by confidence; per-band source counts in the caption. |
| B6 source-rich | B6 graph is denser — caption shows NEWS-heavy source mix; single-source hatching on 8 events; corroboration filter. |
| Single-source HIGH | Hatched nodes/edges; tooltip names the source; "≥2 sources" view isolates the defensible core. |
| Uneven density | Per-band graphs are never compared without their source counts; density metric reported alongside source counts. |

## 10. Data prep required (blueprint §7, items 4, 5, 8)

Tradition taxonomy (node color) · institution_org → I-#### mapping (INSTITUTIONAL edges) · density tables. All derived; frozen data untouched.