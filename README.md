# PV-BUCMS

**Photovoltaic Bottom-Up Cost Model Suite - Q1 2022**

PV-BUCMS is a research software collection for estimating bottom-up installed costs for representative U.S. photovoltaic (PV) systems. It contains separate models for residential rooftop, commercial rooftop, commercial ground-mount, and utility-scale PV systems. The models support national and, where implemented, state-level cost analysis using editable spreadsheet and CSV inputs.

This repository is the software companion to NREL Technical Report [NREL/TP-7A40-83586](https://www.nrel.gov/docs/fy22osti/83586.pdf), *U.S. Solar Photovoltaic System and Energy Storage Cost Benchmarks, With Minimum Sustainable Price Analysis: Q1 2022*.

## Software record status

This repository is being prepared as an archival software-record submission. Version `1.0.0` identifies the Q1 2022 model snapshot. The code is research software and has not been packaged as a supported production application.

The software license is pending formal approval. Until approved license text replaces [LICENSE.md](LICENSE.md), no permission to use, copy, modify, or redistribute the software should be inferred.

## What the models estimate

The models disaggregate the installed cost of representative PV configurations into equipment, balance-of-system (BOS), installation labor, permitting/inspection/interconnection, overhead, contingency, tax, and profit components. The associated report distinguishes:

- **Minimum sustainable price (MSP):** a theoretical, long-term benchmark intended to mute short-term market and policy distortions.
- **Modeled market price (MMP):** an estimated sales price under market conditions during the Q1 2022 analysis period.

The software in this repository is the PV-only subset. Battery storage and PV-plus-storage models are outside this repository.

## Included models

| Directory | Representative configuration in the report | Primary entry point |
| --- | --- | --- |
| `Residential_System_Benchmark_Model` | 7.9-kWdc, 22-module rooftop system with microinverters | `python/main.py` |
| `Commercial_ Rooftop_System_Benchmark_Model` | 200-kWdc, 1,000-Vdc commercial flat-roof system with ballasted racking and string inverters | `python/main_national.py` |
| `Commercial_Ground_Mount_System_Benchmark_Model` | 500-kWdc, 1,000-Vdc fixed-tilt ground-mounted system with driven-pile foundations and string inverters | `python/main_national.py` |
| `Utility_System_Benchmark_Model` | 100-MWdc, 1,500-Vdc single-axis-tracking system with central inverters | `python/main_national.py` |

The space in `Commercial_ Rooftop_System_Benchmark_Model` is part of the archived directory name. Quote that path in shell commands.

## Requirements

- Conda or Miniconda
- Python 3.7 (legacy reference environment)
- Excel-compatible software for reviewing `.xlsx` outputs
- Internet access only when running the optional dataset-update scripts

The root [environment.yml](environment.yml) consolidates dependencies found in the four model environments and source imports. Because several packages are intentionally pinned to legacy versions, use a separate environment.

```bash
conda env create -f environment.yml
conda activate pv-bucms-q1-2022
```

## Quick start

Each model expects to run from its own `python` directory because the scripts use relative paths.

Residential model:

```bash
cd Residential_System_Benchmark_Model/python
python main.py
```

Commercial rooftop model:

```bash
cd "Commercial_ Rooftop_System_Benchmark_Model/python"
python main_national.py
```

Commercial ground-mount model:

```bash
cd Commercial_Ground_Mount_System_Benchmark_Model/python
python main_national.py
```

Utility-scale model:

```bash
cd Utility_System_Benchmark_Model/python
python main_national.py
```

Review generated workbooks in the corresponding `results/` directory. Existing result workbooks may be overwritten; preserve a copy before rerunning a model.

See [docs/USAGE.md](docs/USAGE.md) for entry points and operating cautions, [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) for input provenance categories, and [docs/VALIDATION.md](docs/VALIDATION.md) for published Q1 2022 reference values.

## Scope and limitations

- Results represent simplified, representative systems and national-average assumptions; they do not describe every project or local market.
- Q1 2022 results in the associated report are reported in 2021 real U.S. dollars unless otherwise stated.
- Financing costs are excluded from the benchmark scope.
- MSP is a theoretical construct and should not be treated as an observed transaction price.
- MMP reflects the market and policy conditions of the analysis period and is not a current-price forecast.
- Input workbooks may contain third-party data subject to separate terms or redistribution restrictions. Review [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) before external distribution.
- The archived environment and scripts require reproducibility testing on current operating systems before a public release.

## Documentation

- [Methodology and representative systems](docs/METHODOLOGY.md)
- [Installation and usage](docs/USAGE.md)
- [Input and output data dictionary](docs/DATA_DICTIONARY.md)
- [Validation targets](docs/VALIDATION.md)
- [Software-record release checklist](docs/SOFTWARE_RECORD_CHECKLIST.md)
- [Authors and affiliations](AUTHORS.md)
- [Citation metadata](CITATION.cff)
- [Change history](CHANGELOG.md)

## Citation

If the software is used to reproduce or interpret the Q1 2022 benchmarks, cite both this software record and the associated report. GitHub can read the machine-readable [CITATION.cff](CITATION.cff).

> Ramasamy, Vignesh, Jarett Zuboy, Eric O'Shaughnessy, David Feldman, Jal Desai, Michael Woodhouse, Paul Basore, and Robert Margolis. 2022. *U.S. Solar Photovoltaic System and Energy Storage Cost Benchmarks, With Minimum Sustainable Price Analysis: Q1 2022*. Golden, CO: National Renewable Energy Laboratory. NREL/TP-7A40-83586. https://www.nrel.gov/docs/fy22osti/83586.pdf.

## Funding and notice

This work was authored in part by the National Renewable Energy Laboratory, operated by Alliance for Sustainable Energy, LLC, for the U.S. Department of Energy under Contract No. DE-AC36-08GO28308. Funding was provided by the U.S. Department of Energy Office of Energy Efficiency and Renewable Energy Solar Energy Technologies Office. The views expressed do not necessarily represent the views of the U.S. Department of Energy or the U.S. Government.

## Support

This archival snapshot does not yet define a public support channel. Questions about the software-record submission should be directed to the repository owner or the responsible institutional software-record administrator.

