# Natural-science evidence guardrails

This reference is loaded when the manuscript audit needs design-specific claim
ceilings. It is a decision aid, not a replacement for the study protocol,
statistical analysis plan, reporting guideline, or domain expert review.

## Evidence ladder

Keep these levels separate unless the supplied design and evidence explicitly
justify a transition:

1. hypothesis or protocol;
2. assay or measurement validity;
3. descriptive observation;
4. group difference or association;
5. adjusted association;
6. prediction or diagnostic performance;
7. temporal/longitudinal evidence;
8. intervention or perturbation effect;
9. mechanism supported by specific, orthogonal, and ideally rescue/mediation evidence;
10. replication, external validation, clinical utility, or transportability.

An effect can be statistically credible at one level while remaining unsupported
at the next. A polished sentence is not a transition between levels.

## Design-to-claim ceilings

| Design or evidence source | Usually supports | Does not establish by itself |
|---|---|---|
| Cross-sectional human sample | prevalence/context-specific association | temporal order, incidence, prognosis, causality, clinical utility |
| Case-control study | case-control association under sampling scheme | population risk, incidence, prospective prediction, causality |
| Cohort/longitudinal study | temporal association and outcome patterns | causality without adequate design/analysis and confounding control |
| Randomized intervention | effect of assigned intervention in the studied setting | mechanism, long-term safety, generalizability beyond the enrolled population |
| In-vitro cell experiment | perturbation effect under the tested conditions | organismal efficacy, clinical benefit, complete mechanism |
| Animal model | model-specific biological or treatment response | human disease equivalence or clinical effectiveness |
| Public omics dataset | dataset-specific exploratory/associational signal | independent validation unless the validation design and compatibility are demonstrated |
| Internal split, repeat assay, or second analysis | robustness or internal reproducibility | external validation or clinical utility |
| Meta-analysis | pooled estimate conditional on included studies and heterogeneity | causal interpretation or universal applicability |
| Prediction model | discrimination/calibration in the assessed sample | biological mechanism or external clinical usefulness without validation |

## Measurement-level firewall

Do not silently substitute one level for another:

- DNA variant is not gene expression; mRNA is not protein abundance;
- protein abundance is not protein activity, localization, or pathway flux;
- molecular signal is not cell phenotype; cell phenotype is not tissue or patient outcome;
- a surrogate endpoint is not the clinical endpoint it may correlate with;
- a computational score is not a measured biological mechanism;
- a significant expression difference is not proof of functional importance.

When a paragraph crosses levels, label the transition as interpretation or a
testable hypothesis rather than as an established result.

## Statistics and uncertainty

Prefer the complete result unit when the source is available: sample/replicate
denominator, effect measure and scale, uncertainty (for example CI or dispersion),
P value where relevant, model/contrast, multiplicity context, and practical or
clinical magnitude. Never invent a missing component. Mark it `VERIFY_REQUIRED`.

Do not use “significant” as a synonym for large, important, reproducible, or causal.
Do not turn a non-significant result into “no effect” without considering precision.
Do not describe a subgroup or cell-level result as an individual-level result when
the statistical unit is different.

## Replicate, validation, and concordance terms

- technical replicate: repeated measurement, not an independent biological sample;
- biological replicate: independent experimental unit, subject to the protocol;
- internal reproducibility: same cohort, laboratory, or analysis family;
- external validation: independent data with a prespecified or otherwise justified
  validation procedure and compatible target definition;
- concordance: agreement in direction or pattern, not necessarily agreement in size;
- robustness: persistence under specified alternative analyses or perturbations;
- mechanistic support: evidence for a causal biological path, not merely co-variation.

Use the narrowest term that the evidence supports.

## Discordant data

If datasets, assays, tissues, platforms, species, or models disagree, retain the
disagreement when it changes interpretation. Check and report, as applicable:

- population, disease stage, tissue/cell composition, and inclusion criteria;
- biological versus technical replication and statistical unit;
- platform, assay target, reference/normalization, batch and preprocessing;
- effect direction, scale, precision, missingness and multiplicity;
- prespecified versus exploratory analysis and independent validation status.

Do not call discordant data “consistent validation” merely because one P value is
small or because the prose can be made smoother.

## Reporting-guideline gate

Select the applicable current reporting guideline from the supplied study context
(for example, an observational, randomized, diagnostic, systematic-review,
animal, single-cell, omics, or qPCR guideline). A checklist improves reporting;
it does not upgrade study quality, prove causality, or replace source verification.
For qPCR, preserve assay identity, normalization, replicate/QC and analysis details
required by the applicable MIQE version rather than replacing them with prose.
