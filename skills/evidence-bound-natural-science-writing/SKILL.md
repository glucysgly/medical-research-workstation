---
name: evidence-bound-natural-science-writing
description: Use when a natural-science manuscript has a defined study design and results but its contribution is buried under defensive prose, reviewer prebuttal, redundant caveats, or pressure to make association, mechanism, validation, novelty, or clinical relevance sound stronger than the evidence permits.
metadata:
  short-description: Evidence-bounded natural-science manuscript revision
---

# Evidence-Bound Natural-Science Manuscript Revision

## Overview

Make the strongest supported scientific contribution visible without moving the
evidence ceiling. This Skill adapts contribution-forward revision to laboratory,
clinical, epidemiological, computational, omics, and quantitative manuscripts;
it is not a method for manufacturing stronger results.

The governing order is:

```text
claim -> measurement/design -> result and uncertainty -> interpretation -> boundary
```

Do not replace it with `qualification -> apology -> reviewer prebuttal -> vague
conclusion`, but do not delete a qualification that changes how the result must
be interpreted.

## When to use

Use this Skill when the manuscript is complete or near-complete and the author
asks to make it more direct, active, contribution-forward, less defensive, or
stronger after peer review while preserving scientific meaning. It is especially
useful when the draft contains:

- repeated limitations, self-deprecation, or hypothetical reviewer rebuttals;
- a buried result or contribution statement;
- association written close to causal language;
- mRNA/RNA, protein, activity, phenotype, or clinical utility treated as the same
  evidence;
- internal analysis called validation, or directional disagreement hidden;
- missing effect size, denominator, uncertainty, figure/table linkage, or source role;
- pressure to remove negative findings, contradictory datasets, or unresolved
  author decisions.

Do not use it for first drafting, new analysis, data/QC repair, literature search,
citation discovery, fact checking, generic grammar polishing, Humanizer requests,
or changing outcomes, inclusion rules, methods, ethics, statistical units,
outlier rules, or primary analyses. Route those tasks to their specific Skills.
If the evidence itself is weak or unverified, this Skill must expose that problem,
not disguise it with confident prose.

## Composition with `avoid-overkill`

For a natural-science request explicitly involving defensive writing, self-
weakening, “make it stronger,” or scope control, use `avoid-overkill` as the
proportionality gate and this Skill as the scientific-integrity gate. The two
layers have different jobs and must not be collapsed:

| Layer | Owns | Output |
|---|---|---|
| `avoid-overkill` | user goal, frozen scope, minimum sufficient intervention, no speculative expansion, stop check | proportionality contract |
| This Skill | claim ceiling, design/unit, measurement level, effect/uncertainty, citation/figure roles, contradictions, scientific regression | evidence contract and claim-delta report |

Use this order: `avoid-overkill` scope gate -> this Skill evidence contract and
read-only audit -> explicit author authorization -> smallest coherent revision ->
this Skill scientific regression -> `avoid-overkill` stop check. Never use
“minimal change” to remove a necessary limitation, and never use scientific
rigor as a reason to add unrequested analysis, citations, or a full rewrite.
If the two layers appear to conflict, preserve the scientific boundary and ask a
`QUERY`; proportionality constrains scope, not evidence integrity.

## Required authority and inputs

Collect only the smallest current set needed:

1. the latest manuscript and, for revision, its tracked baseline;
2. study design, analysis plan, and author-locked methods/outcomes;
3. result tables, figures, captions, and the source data or result manifest when
   needed to verify numbers;
4. verified citation map and any target-journal/reporting-guideline requirements;
5. author decisions, prohibited changes, unresolved queries, and revision authority.

Apply this order: verified study/result artifacts and explicit author decisions ->
locked design and estimand -> verified sources and reporting guidance -> this Skill.
Do not invent a missing number, citation, sample size, mechanism, ethics detail,
or validation claim. Use `VERIFY_REQUIRED` or `QUERY` instead.

## Non-negotiable evidence firewall

Before editing, write an evidence contract containing:

| Field | Required content |
|---|---|
| Core contribution | One sentence stating the primary supported scientific payoff |
| Study design and unit | Design, population/model, biological/statistical unit, and sampling boundary |
| Primary estimand/result | What was compared or estimated, with effect measure and uncertainty if available |
| Evidence ladder | Measured observation, association, prediction, temporal evidence, perturbation, mechanism, replication, or clinical utility |
| Claim ceiling | Maximum permitted certainty, causality, novelty, generality, portability, and clinical relevance |
| Load-bearing boundaries | Design limitations, negative/discordant evidence, assay level, confounding, multiplicity, and provenance |
| Citation/figure roles | What each source, table, figure, and caption is allowed to support |
| Edit authority | Sections authorized, locked content, tracking requirements, and live author decisions |

If design, evidence status, claim ceiling, or edit authority cannot be established,
stop after diagnosis. Diagnosis never authorizes rewriting.

Read `references/natural-science-guardrails.md` before classifying candidates.
Use `assets/claim-evidence-audit-template.csv` or an equivalent table for the
register. The template is an audit surface, not a scientific scoring system.

## Phase 1 — read-only whole-manuscript audit

Read title, abstract, introduction, methods, results, figures/tables and captions,
discussion, conclusion, supplements, and references where they affect visible
claims. Do not start with global cue replacement.

For each candidate, record:

`location | original wording | rhetorical function | measured evidence | design/unit |
 effect/uncertainty | citation/figure role | claim delta | disposition | author query`

Use these dispositions:

- `KEEP`: necessary evidence, uncertainty, scope, contradiction, provenance, or method boundary;
- `TIGHTEN`: the boundary is needed but repeated or bloated;
- `REFRAME`: keep the proposition, change defensive ordering or self-deprecation;
- `RELOCATE`: move a real qualification to where it does analytical work;
- `CUT`: remove rhetoric only; never remove a factual proposition or evidence boundary;
- `QUERY`: meaning, data, source status, or author authority is unresolved.

Classify candidates by function rather than by cue word:

| Code | Candidate pattern | Default handling |
|---|---|---|
| D1-D8 | apology, reviewer prebuttal, hedge stack, work-log, buried contribution, volunteered loss, broad self-judgment, misplaced caveat | tighten/reframe/relocate only after context review |
| E1 | measurement-level conflation: RNA/mRNA, protein, activity, phenotype, clinical endpoint | keep distinction; `QUERY` if source is unclear |
| E2 | design-to-claim mismatch: cross-sectional, in vitro, animal, public-data, retrospective, or exploratory evidence overextended | narrow claim; preserve design |
| E3 | statistical inflation or omission: P value without effect/precision, subgroup result without denominator, multiplicity hidden | keep/restore result context; do not invent values |
| E4 | citation, figure, table, or caption role drift | keep original support role; verify source |
| E5 | internal consistency or replication inflation | distinguish concordance, robustness, internal replication, and external validation |
| K1-K5 | scope, uncertainty, negative/discordant evidence, ethics/provenance/reproducibility, or method limitation | `KEEP` or `RELOCATE` |

Run the three-question test before changing any sentence:

1. What does this wording do: rhetoric, measurement, method, result, uncertainty,
   scope, rival explanation, or citation function?
2. What scientific proposition, denominator, boundary, or reader safeguard would
   disappear if it were removed?
3. Is the replacement identical or narrower on certainty, causality, novelty,
   generality, portability, and clinical relevance?

For natural-science claims, also ask: what was actually measured; in which unit;
under which design; with what effect and uncertainty; and which figure/table/source
allows the reader to verify it?

## Phase 2 — authorized contribution-forward revision

Edit only after the author has authorized the identified sections. Revise by
section role, not by global replacement:

1. **Title/abstract:** surface the study question, design, population/model,
   principal result, effect/precision when available, and evidence-bounded implication.
2. **Introduction:** state the problem and gap without claiming novelty, importance,
   or clinical utility beyond the verified literature.
3. **Methods:** improve precision and reproducibility; never hide missing details or
   rewrite the protocol retrospectively.
4. **Results:** lead with the observed result, preserve denominators, effect size,
   uncertainty, units, multiple-testing context, non-significant/negative findings,
   and figure/table correspondence.
5. **Discussion:** use `result -> interpretation -> boundary -> next test`; separate
   association from causality, expression from activity, and exploration from validation.
6. **Conclusion:** state the strongest supported answer and the single most important
   boundary; do not add a new mechanism, biomarker, treatment, or general claim.

One useful form is:

> In [defined design/population], [measured result] was associated with [outcome],
> with [effect and uncertainty if verified]. This supports [bounded interpretation],
> but does not establish [unmeasured causal/mechanistic/clinical claim].

Example: “In this small cross-sectional cohort, LGALS8 mRNA was associated with PE
status, supporting its evaluation as a candidate molecular correlate; the result
does not establish a protein-level biomarker, causal mediator, or clinical utility.”
Do not add a number or citation unless it is supplied and verified.

For every changed sentence, preserve or narrow: claim strength, evidence status,
design and unit, statistical meaning, citation/figure role, terminology, and scope.
When a change would alter a locked method, estimand, outcome, or author judgment,
return `QUERY` rather than improvising.

## Phase 3 — whole-manuscript regression

Read the revised manuscript independently of the change list. Return a regression
report covering:

- claim delta: no inflation of certainty, causality, novelty, generality, portability,
  prediction, diagnostic value, mechanism, or clinical relevance;
- measurement level: RNA/mRNA, protein, activity, cell phenotype, animal phenotype,
  and clinical endpoint remain distinct;
- design/unit: the prose matches sampling, biological replicate, donor/patient/cell
  unit, controls, timing, and estimand;
- statistics: n/denominator, effect measure, uncertainty, P value, multiplicity,
  model, and clinically relevant magnitude are not silently changed or omitted;
- evidence: negative, null, discordant, subgroup, failed, and competing explanations
  remain visible when they affect interpretation;
- citations/figures/tables: each still supports the same proposition and caption;
- reproducibility/provenance: methods, accession, code, assay and ethics details are
  not upgraded, invented, or retrospectively normalized;
- voice: direct and contribution-forward, but not promotional or self-congratulatory.

## Required deliverables and stop rules

For diagnosis, return the evidence contract, candidate register with visible `KEEP`
decisions, section concentration map, claim/evidence risk summary, author queries,
and a bounded revision recommendation. Do not modify the manuscript.

Do not return a ready-to-paste replacement paragraph during a diagnostic-only pass.
If the author explicitly requests an illustration, label it `ILLUSTRATIVE_ONLY`,
keep it separate from the manuscript, and do not present it as an authorized edit.

For authorized revision, additionally return tracked and clean files when supported,
a change summary, claim-delta table, statistics/figure/citation regression report,
deliberate non-edits, unresolved author decisions, and residual blockers.

Stop after the requested diagnostic or authorized revision pass. Do not perform new
analysis, discover citations, submit a manuscript, upload restricted data, change
scientific methods, or describe an unverified result as completed.

## Common failure modes

| Temptation | Required response |
|---|---|
| “Make it sound like a validated biomarker” | Define validation and report the missing validation gate |
| “Remove all limitations” | Remove repetition only; retain load-bearing boundaries |
| “The datasets agree” | Compare direction, effect, uncertainty, sample/platform and analysis compatibility |
| “The intervention proves mechanism” | Separate perturbation effect from mechanism and require the missing mechanistic tests |
| “P < 0.05 is enough” | Preserve effect size, precision, denominator, multiplicity, and practical relevance |
| “Only return polished prose” | Complete the required audit/regression record first; diagnostic-only mode does not produce a ready-to-paste replacement |
