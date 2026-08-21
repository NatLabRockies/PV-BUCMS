# Contributing

This repository is an archival software-record candidate. Changes should preserve the ability to reproduce the reviewed Q1 2022 snapshot.

1. Create a branch for each change.
2. Keep scientific-method changes separate from documentation or maintenance changes.
3. Document changes to assumptions, input sources, units, or formulas in `CHANGELOG.md` and the relevant methodology/data documentation.
4. Do not commit credentials, proprietary datasets, temporary Office files, Python caches, or generated IDE metadata.
5. Run the affected model from its `python/` directory and compare outputs with `docs/VALIDATION.md`.
6. Include the operating system, Python/Conda environment, commands run, and validation results in the review description.
7. Do not replace license, copyright, funding, or attribution language without institutional approval.

For a preservation-only correction, explain why the change does not alter scientific results. For a scientific update, use a new version and retain the original tagged software-record release.

