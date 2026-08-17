# GIS / Spatial Design v1 — Mapping What Can Be Mapped

**Phase:** 2 — Analysis Design · **Date:** 2026-08-17 · **Baseline:** frozen V3.0
**Answers:** Q0.2, Q1.1 (see `analysis_blueprint_v1.md` §3)

---

## 1. Principle

**Map only what the evidence supports.** A map is a claim about geography; every rendered line or point must carry its evidence class. Where evidence is weak, the map shows uncertainty — it does not hide it.

## 2. What can be mapped reliably (three tiers)

### Tier 1 — Point-to-point with known coordinates (reliable)
- **30 of 39 places** have lat/lon (all cities, sites, temples, universities, monasteries).
- **All 41 travels** have origin + destination place IDs; 27 have start years.
- **All 19 events** have locations and dates (1370 → 2027-01-14).
- Pilgrimage routes between known sites: EV-0001 (Bodh Gaya → Sarnath, 1167 km), EV-0006 (Sarnath → Bodh Gaya), EV-0007 (8 great sites + Nepal), EV-0012 (Dharamsala/Ajanta-Ellora/Sanchi), EV-0013 (India–Nepal).
- **Render:** points by place type; straight dashed "schematic" lines between endpoints for travels WITHOUT intermediate evidence (labeled SCHEMATIC — not a claimed route).

### Tier 2 — Routed journeys with intermediate evidence (8 travels)
| Travel | Person | Intermediates |
|---|---|---|
| T-0001 | Hyecho | Gandhara; PL-0011; PL-0020; PL-0019 (Serindia) — the only fully documented ancient route (from his own text) |
| T-0003 | P-0011 | PL-0030 |
| T-0005 / T-0006 / T-0007 | Silla monks | PL-0015 / PL-0015;PL-0009 / PL-0009 |
| T-0010 | P-0020 | PL-0015 |
| T-0013 | Jikong (Dhyānabhadra) | PL-0021; PL-0017 |
| T-0042 | Hwang Su-yŏng | PL-0009 |

**Render:** polylines through the documented intermediates, with per-segment confidence styling. **Do NOT invent segments** between intermediates (e.g., Hyecho's sea leg Korea→China is a corridor, not a line).

### Tier 3 — Region-level schematic (ancient, fuzzy)
- Silla/Goryeo → India journeys without route evidence (T-0005..T-0009, T-0012, T-0039): render as **hatched corridor arrows** between region centroids (e.g., Silla coast → Chang'an → India), explicitly labeled "schematic corridor, route unknown".
- Sea routes (Korea → China → India) rendered as corridors, never as precise paths.

## 3. What cannot be mapped (and how it is handled)

| Item | Handling |
|---|---|
| 9 non-point places (PL-0001 Silla, PL-0002 Baekje, PL-0004 Goguryeo, PL-0005 Goryeo, PL-0006 Joseon, PL-0008 Gandhara, PL-0012 Central India/Sangana, PL-0019 Serindia, PL-0031 India unspecified) | Region centroids from standard gazetteers, marked `REGION_CENTROID` (uncertainty class), rendered as labeled hatched regions, never as precise points. |
| 33 travels without intermediate evidence | Schematic dashed lines between endpoints (Tier 1), never interpolated routes. |
| Legendary journeys (Suro/Heo Hwang-ok, P-0007/0008) | Only in a toggleable "legend" layer with a distinct glyph; off by default. |
| Undated travels (14) | Rendered without a time position in static maps; in the interactive map they appear only when the time window covers their floruit span (fuzzy). |
| Documented negatives | X markers at the relevant location (Kelaniya, Nav Nalanda, Piparhawa) with a "negative result" label — the map records the search, not the event. |

## 4. Layer stack (interactive map)

1. Base map — light, neutral, Asia-focused, equirectangular projection (no decorative styling).
2. PLACES — points by `place_type` (CITY/SITE/MONASTERY/TEMPLE/UNIVERSITY/REGION…); regions as hatched centroids.
3. TRAVELS — polylines by tier (Tier 1 schematic dashed / Tier 2 routed solid / Tier 3 corridor hatched); color by direction (Korea→India, India→Korea, via third country).
4. EVENTS — point markers by `event_type` (pilgrimage, conference, exhibition, relic transfer, MOU, dedication/foundation).
5. NEGATIVES — X markers (toggleable).
6. LEGEND layer — legendary content (toggleable, off by default).

## 5. Uncertainty rendering (legend is mandatory)

| State | Encoding |
|---|---|
| Known point (lat/lon in data) | solid point |
| Region centroid (derived) | hatched region + hollow point |
| Routed journey (intermediates documented) | solid polyline |
| Schematic journey (endpoints only) | dashed polyline, labeled SCHEMATIC |
| Corridor (no route evidence) | hatched band between regions |
| Legendary | ◈ glyph, distinct color, "legend" label |
| Negative | X marker |
| Undated | no time position; appears only in matching time window |

## 6. Static vs interactive

- **Static (V4):** one map per band with carried data — B1 (Silla/Gaya network + Hyecho route), B2 (Jikong circle + Hoeamsa), B4 (colonial-era), B5 (1945–1990), B6 (contemporary events). **No B3 map** — the legend states "B3 Joseon: no carried records (see timeline)". Each static map carries its source count.
- **Interactive (V5):** time slider synced to the timeline; layers toggleable; click-through record cards.

## 7. How the five data limitations appear

| Limitation | Rendering |
|---|---|
| B3 zero carried | No B3 layer; legend note; the Joseon-era excluded records are not mapped (they are textual, not spatial). |
| B1 small primary core | Hyecho's route is the only solid ancient polyline; everything else is corridor/schematic; per-map source counts. |
| B6 source-rich | Event markers dominate B6 maps — the legend shows the source-type mix (NEWS-heavy) so density is not read as importance. |
| Single-source HIGH | Hatched markers for the 8 single-source events; tooltip names the source. |
| Uneven density | Per-band maps are never compared side by side without their source counts displayed. |

## 8. Data prep required (blueprint §7, items 1, 3, 8)

Region centroids for 9 places · APPROX dates for 14 travels · density tables. All derived; frozen data untouched.