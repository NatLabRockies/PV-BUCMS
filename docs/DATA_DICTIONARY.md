# Input and output data dictionary

## Purpose and provenance classes

Each model has its own `input_data/` and `results/` directories. This inventory describes file roles from the archived repository and code. It does not assert redistribution rights. Before public release, classify every file as one of:

- **Original:** created specifically for the model.
- **Derived:** transformed from one or more cited sources.
- **Third-party:** copied or downloaded from an external provider.
- **Generated:** produced by the software.

The final software record should add source URLs, access dates, license/terms, responsible curator, units, and checksums for each distributed data file.

## Common inputs

| File or pattern | Role | Provenance/release note |
| --- | --- | --- |
| `inputs.xlsx` | Primary scenario and system assumptions consumed by model scripts | Confirm worksheet-level definitions and units before release. |
| `Bill of Material Input.xlsx` | Component quantities and material assumptions | Likely original/derived model input; confirm authorship. |
| `Labor_Info.xlsx` | Labor categories, hours, or rates used in installation calculations | Derived; document year, geography, and burden assumptions. |
| `BLS Labor Database.xlsx` | Labor-rate database used by cost functions | Derived from U.S. Bureau of Labor Statistics data; document retrieval date and transformation. |
| `state_data.csv` | State-level factors or lookup values | Document each column, unit, and source. |
| `consumer_price_index.csv` | Consumer price index series used for inflation adjustments | Derived from public economic data; document series identifier and base year. |
| `historical_cost_index.csv` | Historical cost escalation/index values | Document source series and conversion method. |
| `datasets/CPIAUCSL.xls` | Archived CPI series | Third-party public economic dataset; verify redistribution terms and series metadata. |
| `datasets/WPU101704.xls` | Archived producer-price series | Third-party public economic dataset; verify series metadata. |
| `datasets/WM_USSMI_2019.xlsx` | Archived market dataset | Potentially restricted third-party content; confirm redistribution permission before public release. |
| `datasets/bls_labor_database*.xlsx` | Archived national/state labor data | Derived from BLS data; document processing and access date. |

## Residential-specific inputs

| File | Role |
| --- | --- |
| `BLS Wage Index.xlsx` | Wage-index data used for geographic or temporal labor adjustments. |
| `Integrator Market Share.xlsx` | Installer/integrator market-share assumptions. Review redistribution rights. |
| `Inverter Cost Kelsey.xlsx` | Archived inverter-cost assumptions; identify source and responsible curator. |
| `Inverter Shipments.xlsx` | Inverter shipment or market-weighting assumptions. Review redistribution rights. |
| `Labor Hours.xlsx` | Installation labor-hour assumptions. |
| `Microinverter.xlsx` | Microinverter configuration and/or price assumptions. |
| `Soft Costs.xlsx` | Permitting, customer acquisition, overhead, or related soft-cost inputs. |

## Commercial rooftop-specific inputs

| File | Role |
| --- | --- |
| `Commercial - Material Labor Equipment.csv` | Commercial rooftop material, labor, and equipment assumptions. |
| `Developer Profit & Overhead.xlsx` | Developer overhead and profit assumptions. |
| `commercial_storage.xlsx` | Storage-related workbook present in the archived folder; it is not part of the PV-only scope and should be reviewed for removal or separate documentation. |
| `inverter.csv` | Commercial inverter assumptions. |
| `module_database.xlsx` | PV module specifications or pricing assumptions. |
| `loading_combo.csv` | Structural loading combinations or design assumptions. |

## Commercial ground-mount and utility-specific inputs

| File | Role |
| --- | --- |
| `600_1000_1500v.xlsx` | Electrical architecture assumptions for different DC voltage levels. |
| `Utility - Material Labor Equipment.csv` | Ground-mount/utility material, labor, and equipment assumptions. |
| `Overhead.xlsx` | EPC/developer overhead assumptions. |
| `loading_combo.csv` | Structural loading combinations or design assumptions. |
| `module_database.csv` | PV module specifications or pricing assumptions. |

## Outputs

Files in each `results/` directory are generated or curated result workbooks. The principal archived outputs include:

- `Q1 2022 Residential Benchmark Table for Chart.xlsx`
- `Commercial Rooftop PV Benchmark National Average.xlsx`
- `Commercial Ground Mount Benchmark National Results.xlsx`
- `Utility Benchmark National Results.xlsx`

Before release, record which outputs were generated from commit `22774de`, which were manually post-processed, and the exact entry point and input checksums for each.

## Files excluded from the record

Temporary Office lock files (`~$*`), `.DS_Store`, Python bytecode/cache files, IDE metadata, and Windows `Zone.Identifier` metadata are excluded through `.gitignore` because they are not scientific inputs or source code.

