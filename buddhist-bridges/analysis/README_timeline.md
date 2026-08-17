# Timeline MVP — Reproducible Pipeline

This directory contains the Phase 2, Step 3 minimum viable historical timeline for **Buddhist Bridges**.

## Rebuild

From `india-korea-mediators/`:

```bash
python3 buddhist-bridges/analysis/build_timeline_data.py
python3 buddhist-bridges/analysis/validate_timeline.py
```

The builder reads the read-only snapshot in `buddhist-bridges/v3.0_frozen/`, the validated derived tables in `analysis/data/`, and the prosopography register. It writes:

- `analysis/data/timeline_data.json` — generated, auditable timeline data
- `analysis/timeline_mvp.html` — self-contained HTML with the JSON embedded

The current generated output contains 182 visualization marks: 118 marks with `CARRIED` scope and 21 undated/unplaced source records retained outside the axis. These are different accounting units. A mark is a display unit, not necessarily a unique person, event, relationship, or historical occurrence; one source record can generate multiple marks.

No frozen CSV is modified. `validate_timeline.py` also checks the V3.0 SHA-256 manifest, carried-people reconciliation, unplaced-record safeguards, required gaps, lanes, and embedded HTML data.

## Data rules

- Explicit event, text, travel, founding, and biographical dates are used where present.
- Floruit windows and derived travel ranges are marked `APPROX`/`FLORUIT` and rendered fuzzy.
- Undated records remain in the unplaced table; no dates are invented.
- B3 is labelled **no carried records under the current inclusion criteria**, not evidence of no Buddhist activity.
- The source-density ribbon is source-linked/documented evidence density for the relevant source-linked records, not a measure of overall Buddhist activity or historical importance.
- Institutional soft spans are band-based approximations and must not be read as documented continuous institutional lifespans.
- Source count is evidence metadata only. Single-source records receive hatching and a `1` badge.
- Legendary records are off by default and currently remain unplaced because the frozen records have no safe date.

Open `timeline_mvp.html` directly or serve this directory with a local HTTP server. The MVP has no external dependencies or build framework.
