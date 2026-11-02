# Manhattan Affordable Housing and Neighborhood Income

This project looks at whether the location of affordable housing projects across Manhattan is associated with neighborhood household income.

## Current Repository Structure

```text
manhattan-housing-affordability/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_analysis.ipynb
├── analysis/
│   ├── __init__.py
│   ├── data_processing.py
│   └── visualize.py
├── visualizations/
├── README.md
├── requirements.txt
└── .gitignore
```

## Current Progress

So far, the repository includes the beginning of the data cleaning and geography setup.

In `01_analysis.ipynb`, we have:

- loaded the NYC 2020 Neighborhood Tabulation Area shapefile
- filtered it to the 38 Manhattan NTAs
- confirmed the CRS is `EPSG:2263`
- loaded 2024 ACS household income and household count data
- filtered the ACS data to Manhattan census tracts
- removed 9 census tracts with 0 households and missing income
- created a cleaned tract GEOID
- saved the cleaned ACS data to `data/processed/`

The current cleaned ACS output is:

```text
data/processed/manhattan_acs_income_by_tract.csv
```

## Data

Raw datasets should be stored in:

```text
data/raw/
```

Processed datasets created by the code should be stored in:

```text
data/processed/
```

The raw files should not be edited manually.

## Running the Analysis

Install the required packages with:

```bash
pip install -r requirements.txt
```

Then open:

```text
notebooks/01_analysis.ipynb
```

and run the notebook from top to bottom.

All file paths in the project should be relative so the analysis can run on another computer.

## Main Datasets

The project currently uses:

- NYC 2020 Neighborhood Tabulation Areas
- 2024 American Community Survey 5-Year Estimates

Additional housing datasets will be added as the analysis continues.