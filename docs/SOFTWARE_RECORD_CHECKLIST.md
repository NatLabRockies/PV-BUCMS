# Original software-record release checklist

## Identity and ownership

- [ ] Confirm the official software title and expansion of `PV-BUCMS`.
- [ ] Assign the institutional software-record identifier.
- [ ] Confirm software authors/developers separately from report authors.
- [ ] Add author order, affiliations, email/contact role, and ORCID identifiers where approved.
- [ ] Confirm copyright ownership and any contractor or third-party contributions.

## Legal and data review

- [x] Add the standard BSD 3-Clause License with the approved Alliance copyright statement.
- [ ] Review all workbooks and CSV files for proprietary, licensed, export-controlled, sensitive, or personally identifiable information.
- [ ] Confirm redistribution permission for market datasets, especially `WM_USSMI_2019.xlsx` and other commercial-source data.
- [ ] Confirm that report notice, funding, and attribution language are correct for the software.
- [ ] Run credential and secret scanning before release.

## Technical review

- [ ] Build `environment.yml` on a clean system and save the resolved environment export.
- [ ] Run all four primary model entry points.
- [ ] Compare results with `docs/VALIDATION.md` and archive the evidence.
- [ ] Document every discrepancy between software output and published values.
- [ ] Verify that update scripts do not modify the frozen release inputs during reproduction.
- [ ] Record SHA-256 checksums for distributed input and reference-output files.
- [ ] Decide whether archived scripts, Mac-specific copies, PowerPoint instructions, and unrelated storage inputs belong in the release.

## Documentation and release

- [ ] Confirm README terminology, support contact, and intended audience.
- [ ] Confirm `CITATION.cff` against the approved software-author list.
- [ ] Add a final release date and software-record identifier to citation metadata.
- [ ] Tag the reviewed commit as `v1.0.0` (or the institutionally approved version).
- [ ] Create an immutable GitHub release with release notes and checksums.
- [ ] Deposit or link the release in the required institutional archive.
- [ ] Preserve the private review snapshot before any public release.
