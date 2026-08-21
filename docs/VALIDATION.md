# Validation targets

## Purpose

The values below are publication-level acceptance targets from NREL/TP-7A40-83586. They are not yet automated regression tests. A software-record reviewer should run each model, map the generated output fields to these values, document any rounding or post-processing, and archive the comparison.

All values are Q1 2022 benchmarks expressed in 2021 real U.S. dollars.

| Model | Representative system | MSP | MMP |
| --- | --- | ---: | ---: |
| Residential rooftop | 7.9-kWdc rooftop PV | $2.55/Wdc ($3.09/Wac) | $2.95/Wdc ($3.57/Wac) |
| Commercial rooftop | 200-kWdc rooftop PV | $1.63/Wdc ($2.00/Wac) | $1.84/Wdc ($2.26/Wac) |
| Commercial ground-mount | 500-kWdc ground-mounted PV | $1.71/Wdc ($2.10/Wac) | $1.94/Wdc ($2.38/Wac) |
| Utility scale | 100-MWdc one-axis-tracking PV | $0.87/Wdc ($1.17/Wac) | $0.99/Wdc ($1.33/Wac) |

## Acceptance procedure

For each model:

1. Create the archived environment from `environment.yml`.
2. Record the Git commit and SHA-256 checksums of every input file.
3. Run the primary entry point from the model's `python/` directory without running data-update scripts.
4. Record runtime, warnings, and output checksums.
5. Identify the exact cells or rows containing total MSP/MMP output.
6. Compare the output with the corresponding published target.
7. Explain any difference, including unit conversion, rounding, inflation basis, post-processing, or divergence between the archived workbook and the final publication.

Do not alter code or inputs merely to force agreement. Record discrepancies as reproducibility findings and, if a correction is approved, issue a new version while preserving the original tag.

## Known validation gap

At the time this documentation was created, the four models had not been rerun in a clean Python 3.7 environment. Therefore, the repository should be described as an archival software-record candidate, not yet a fully verified reproducible release.

