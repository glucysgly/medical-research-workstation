# Protected statistical-unit rule

For biological comparisons in single-cell or single-nucleus analyses, the donor
is the inferential unit. Cells and technical libraries are observations nested
within donors. A cell-level test may be used only for descriptive QC or marker
visualization and must not be reported as independent biological replication.

Required downstream evidence:

- `donor_id`, group and tissue are present in cell metadata.
- Donor-level pseudobulk or a donor-aware mixed model is used for inference.
- The number of donors, effect estimate, uncertainty and multiple-testing rule
  are reported.
- Technical replicates are aggregated or modeled within donor.
