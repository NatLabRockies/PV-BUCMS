# Installation and usage

## Archived environment

The original per-model instructions specify Python 3.7 and Conda. Create the consolidated root environment:

```bash
conda env create -f environment.yml
conda activate pv-bucms-q1-2022
```

The old dependency set may not solve on every modern platform. Preserve the pins for record fidelity; document any compatibility changes rather than silently upgrading packages.

## Working-directory requirement

The scripts use relative paths to sibling `input_data/` and `results/` directories. Run each entry point from that model's `python/` directory.

## Entry points

### Residential

```bash
cd Residential_System_Benchmark_Model/python
python main.py
```

Additional archived analyses include `main_sensitivity.py` and `main_sensitivity_system_size_efficiency.py`.

### Commercial rooftop

```bash
cd "Commercial_ Rooftop_System_Benchmark_Model/python"
python main_national.py
```

The folder also contains `main_state.py` and `main_national_sensitivity.py`.

### Commercial ground-mount

```bash
cd Commercial_Ground_Mount_System_Benchmark_Model/python
python main_national.py
```

The folder also contains `main_state.py` and `main_national_sensitivity.py`.

### Utility scale

```bash
cd Utility_System_Benchmark_Model/python
python main_national.py
```

The folder also contains `main_state.py` and `main_national_sensitivity.py`.

## Updating external datasets

Several models include `retrieve_datasets.py`, `update_labor_database.py`, or `update_wage_index.py`. These scripts access external resources and may change the archived inputs. Do not run them when attempting to reproduce the frozen Q1 2022 record. Run them only in a working copy, record the retrieval date and source URL, and create a new version if results change.

## Inputs and outputs

- Edit model assumptions in the applicable `input_data/` spreadsheets and CSV files.
- Preserve units and worksheet/column names expected by the Python scripts.
- Results are written under the corresponding `results/` folder, commonly as Excel workbooks.
- Existing results may be overwritten. Copy the original file before rerunning a model.

## Reproducibility record

For each run, record:

- Git commit and software version
- Model directory and entry point
- Operating system and architecture
- Conda environment export
- Input-file checksums
- Whether any update/retrieval script was run
- Start/end time and console errors or warnings
- Output-file checksums
- Comparison with `docs/VALIDATION.md`

