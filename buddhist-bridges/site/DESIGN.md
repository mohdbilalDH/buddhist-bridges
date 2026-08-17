# DESIGN.md — Buddhist Bridges

Design system for the project pages. Follows the DESIGN.md convention (VoltAgent/awesome-design-md):
document the identity so every later addition stays coherent.

## Identity

A Digital Humanities research report by a Korean Studies scholar. The page argues from evidence;
the design's job is hierarchy and restraint, in the tradition of a well-set journal article with
one interactive instrument. Research → evidence → visualization → interpretation.

## Typography

| Role | Face | Notes |
|---|---|---|
| Narrative (body, titles, figure takeaways) | Source Serif 4 Variable (self-hosted) | optical sizing on; body 1.075rem/1.62 |
| Apparatus (labels, captions, tables, chart text, nav) | IBM Plex Sans 400/500/600 (self-hosted) | captions 0.8rem; kickers 0.7rem, +0.13em tracking, uppercase |
| Data identifiers, citation block | IBM Plex Mono 400 | record IDs, cite block |

Scale: 2.35 / 1.5 / 1.1 / 1.075 / 0.85 / 0.8 / 0.7 rem. Korean text falls back to Apple SD
Gothic Neo / Noto Sans KR inside both stacks.

## Color

Warm-tinted neutrals only; no pure gray or black. Ground `#FAF9F5`, ink `#23211C`, muted
`#5F5B51`, rules `#E2DED2`. Accent (ochre) `#96591B` for kickers and evidence markers; link
slate `#3E5A75`. Dark mode is a separately stepped set, not an inversion.

The only categorical palette is the five cohorts, machine-validated for CVD safety in both modes
(dataviz six checks; the 6–8 ΔE band on blue↔magenta is covered by direct labels and gaps):

| Cohort | Light | Dark |
|---|---|---|
| B1 300–900 | `#eda100` | `#c98500` |
| B2 900–1392 | `#008878` | `#17a08b` |
| B4 1900–1945 | `#2a78d6` | `#3987e5` |
| B5 1945–1990 | `#a8509d` | `#c063b5` |
| B6 1990–2026 | `#c2551c` | `#d96a2e` |
| B3 void | `#B5AF9F` | `#4E4B42` |

Cohort colors mean cohorts, everywhere, and nothing else. Semantic negative `#A03B33` is
reserved for documented negatives and single-source warnings.

## Uncertainty grammar (fixed across every view)

- solid mark = explicitly dated record
- dashed/translucent = floruit-derived or approximate
- hatched = single-source record
- ✕ = documented negative
- dotted line = the Joseon void (absence, annotated in place)
- undated records are listed, never placed on an axis

## Figures

Every figure carries: `Figure N` kicker → serif takeaway title stating the finding → chart →
sans caption → `details` data table. Chart text is Plex Sans; axis/gridwork uses `--rule` and
`--faint`; density never encodes importance.

## Spacing & shape

Rhythm on a 0.25rem base: 0.5 / 0.75 / 1 / 1.5 / 2.25 / 3.5 rem. Reading column 44rem;
instrument pages 66rem. Radius 4px everywhere (6px for the era panel); no shadows except the
person-record dialog. Sections separated by 1px rules, not cards.

## Motion

Lenis smooth scroll (lerp 0.16), disabled under `prefers-reduced-motion`. Otherwise only hover
and focus states. No entrance animations, no parallax, no bounce easing.

## Do / Don't

- Do direct-label marks; legends only when labeling is impossible.
- Do keep captions in the apparatus face so narrative and apparatus stay distinguishable.
- Don't introduce new hues, gradients, icon sets, or card-in-card nesting.
- Don't use the accent for decoration; it marks evidence and structure only.
- Don't let any chart claim more than its caption can defend.
