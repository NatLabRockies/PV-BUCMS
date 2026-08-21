# Security policy

## Supported versions

This repository contains legacy research software prepared for archival review. No version is currently designated as receiving ongoing security maintenance.

## Reporting a concern

Do not disclose credentials, sensitive data, or an exploitable vulnerability in a public issue. Report concerns privately to the repository owner or the responsible institutional cybersecurity/software-release contact.

## Operational cautions

- Review dataset-retrieval scripts before execution; they access external network resources and may replace local input files.
- Run the legacy environment in an isolated Conda environment, not a privileged system Python installation.
- Treat all input spreadsheets and downloaded datasets as untrusted until their provenance and integrity have been checked.
- Do not enable spreadsheet macros from untrusted sources. The committed model workbooks are `.xlsx` or `.xls`, not macro-enabled `.xlsm` files.

