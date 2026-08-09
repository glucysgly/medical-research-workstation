# WSL Repair After Snapshot

Validated 2026-08-09 after Windows restart.

## Change

- Applied: bcdedit /set hypervisorlaunchtype auto.
- No BIOS, Secure Boot, WSL feature installation, distribution unregister,
  reset, deletion, or data movement was performed.

## Verification

- HypervisorPresent: true.
- CPU virtualization firmware: true.
- SystemStartOptions: HYPERVISORLAUNCHTYPE=AUTO.
- WSL2 probe: PASS.
- Existing Windows doctor: 0 warnings, 0 failures.
- WSL bridge regression: 17/17 PASS.
- Linux doctor: 0 warnings, 0 failures.
- bio-base samtools, bcftools, bedtools, FastQC and MultiQC: PASS.
- R and Bioconductor baseline checks: PASS.
- JupyterLab, Docker Engine and NVIDIA WSL GPU: PASS.
- Research project bridge smoke: PASS; WSL can read the D-drive project and
  execute Python 3.14.4, samtools 1.24 and Rscript 4.5.2.

The historical baseline conflict is resolved by this live post-restart result.
