---
topology: parallel
seats: [pragmatist, risk-officer, first-principles]
quick_seats: [pragmatist, risk-officer]
model_overrides:
  chairman: strong-model
---

# Council Default — minimal generic council

The off-the-shelf bench behind `/council` (FR3): three seats with
orthogonal, person-agnostic reasoning methods — cost-benefit triage,
failure-mode enumeration, first-principles decomposition — plus the
implicit chairman. It reads DECISIONS, not people: no profiles, no
transcripts, no database (FR8).

Quick mode (default) runs the Pragmatist and Risk Officer with no peer
review — the gut-check tier. `--full` adds First Principles, anonymized
peer review, and the devil's-advocate pass.

This file is the portable roster format (FR9): copy it, rename it, swap
seats, and run it anywhere the engine runs.
