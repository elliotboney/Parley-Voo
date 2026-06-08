# Council Protocol — Deliberation Contract

Adapted for Parley Voo from the council-review skill in
[`ngmeyer/skills`](https://github.com/ngmeyer/skills)
(path `skills/productivity/council-review/`), Copyright (c) 2026 Neal Meyer,
released under the MIT License. Quoted lines below are verbatim from that source.

The protocol exists to defeat two failure modes: **sycophancy** (seats telling
you what the framing expects) and **majority smoothing** (a correct minority
read getting averaged away). Every rule below traces to one of those two.

## 1. Anonymization shuffle

Before peer review, collect all seat responses, shuffle them, and relabel
A, B, C… — one anonymous label per participating seat.

> "Randomize the mapping — Advisor 1 should NOT always be Response A."

Rationale (upstream): "Reviewers defer to role names if visible." A reviewer
who knows Response C came from the security seat will defer on security
questions instead of judging the reasoning. The mapping must be random per
run — a fixed seat→label order leaks identity across runs.

## 2. Devil's advocate vs. consensus

After responses and peer reviews are in, the chairman:

1. States the emerging consensus in **one sentence**.
2. Spawns ONE devil's advocate on a strong model with the instruction:
   "make the strongest possible case that this answer is WRONG."
3. The attack must answer three demands:
   - What does the consensus overlook that flips the decision?
   - Construct the concrete failure scenario.
   - What evidence would force abandoning this answer?

This is explicitly NOT a 2-vs-2 debate structure — it is one sharp attack on
the *converged* answer. The chairman must rebut or concede the attack before
finalizing the verdict.

## 3. Sycophancy guardrail (seat prompts)

Every seat prompt in stage 1 carries this rule verbatim:

> "Do not defer to any answer the framing seems to expect. Reason from your
> method to wherever it actually leads; if that's against the apparent
> expected answer, say so plainly. Hedging toward the obvious answer is the
> failure this council exists to prevent."

## 4. Peer-review conformity check

Every peer-review prompt in stage 2 carries this check verbatim:

> "Where these responses agree, is the agreement genuine — or could it be
> conformity to a shared framing? Flag any consensus that looks like
> deference rather than independent reasoning."

Agreement is only evidence when it is *independent* agreement. Five seats
repeating the framing's implicit answer is one data point, not five.

## 5. Chairman output contract

The chairman's synthesis renders exactly these headings, in this order:

1. **Agrees** — where the council genuinely converged (post conformity check)
2. **Clashes** — each clash classified as **value tension** (both positions
   valid, different priorities) or **error catch** (one seat found a real flaw)
3. **Blind Spots** — what no seat addressed until peer review surfaced it
4. **Recommendation** — the verdict; may side with a strong minority
5. **What You Lose** — the real cost of following the recommendation
6. **Do This First** — the single highest-leverage next action
7. **Verify** — how to check the recommendation against reality

Dissent is never smoothed into the recommendation: minority positions
survive under an explicit `Dissent:` label with attribution
`— {Display Name}, {method}`.

## 6. Composable flags (pattern note — not implemented)

Upstream composes behavior with flags: `--quick`, `--adaptive`,
`--confidence`, `--measure-diversity`, `--jury`. Parley Voo adopts the
composable-flag pattern but implements none of it here — quick/full mode
lands in Story 1.3; `--adaptive` and `--jury` are out of scope entirely.
