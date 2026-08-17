# Timeline MVP Report

**Date:** 2026-08-17  
**Baseline:** frozen V3.0, validated derived tables, and validated prosopography outputs

## What it shows

The MVP provides one continuous 300–2027 CE axis with B1–B6 shading, separate lanes for people, travels, texts/translations, institutions, events, encounters, and documented negatives. It shows explicit dates, derived approximate windows, dated activity ticks, source-density and record-density ribbons, the B3 annotation, and the 1370–1981 event gap. Filters cover period, entity type, direction, confidence, tradition, connection type, scope, and corroboration. Hover cards expose evidence and source keys; click cards expose the full generated record.

## Mark accounting and interpretation

The generated dataset contains **182 timeline marks**. These are visualization units, not automatically 182 unique historical persons, events, connections, or occurrences. A carried record can produce a lifeline, a dated activity marker, a translation marker, or another display mark; one underlying record can therefore contribute more than one mark, and some marks represent derived display relationships. Of the 182 marks, 118 have `CARRIED` scope. The data also retains 21 records without a safe date in the unplaced table; those records are not placed on the chronological axis. “Carried records,” “marks,” and “unplaced records” must therefore be read as different accounting units.

## What it cannot show

It does not provide a map, route geometry, a network view, inferred continuity, automatic animation, or a text-transmission chain. Several frozen records have no safe date and therefore appear only in the unplaced table. The source-density ribbon represents source-linked/documented evidence density for the relevant source-linked records, currently dated carried people and events; it is not a measure of overall Buddhist activity or historical importance. Institution activity spans are deliberately band-based approximations, not documentary continuous institutional lifespans.

## Descriptive findings only

Visible clustering, empty periods, source-linked evidence-density variation, direction counts, and the B3 finding of **no carried records under the current inclusion criteria** are descriptive properties of this curated dataset and its inclusion criteria. B3 must not be interpreted as evidence of an absence of Buddhism. These patterns are not estimates of overall Buddhist activity, historical importance, or the volume of undocumented exchange. Source count is never used to size a mark.

## Uncertainty representation

Explicit dates use solid/date-specific marks. Floruit and derived travel windows are fuzzy or dashed and carry `?`; uncertain confidence uses dashed/dotted opacity; unresolved events receive a dashed ring; single-source records are hatched and badged; negatives use X marks; legendary material is off by default and undated legendary records remain unplaced. Context and excluded records are dimmed and separately filterable.

## Design deviations

No substantive design decision in `timeline_design_v1.md` was changed. The implementation keeps the single axis, bands, lanes, ribbons, visible gaps, filters, and no-autoplay/no-inferred-route safeguards. The data builder normalizes classification `KEEP`/`ADAPT` to the UI's `CARRIED` scope label. This is a display-layer normalization, not a dataset change. The MVP remains intentionally simpler than the advanced GIS, network, and transmission-chain versions.

## Validation

`validate_timeline.py` checks the generated data against the frozen manifest and required structural safeguards. The timeline is ready for review; no further analysis layer was started.
