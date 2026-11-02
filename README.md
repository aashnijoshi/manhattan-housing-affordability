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

- loaded NYC HPD Affordable Housing Production by Building, filtered to Manhattan, dropped records without coordinates, and deduplicated on (Project ID, Building ID)
- spatially joined HPD buildings to the 2020 Manhattan NTAs (EPSG:2263) and summed affordable units per NTA
- aggregated ACS tract income and households to NTAs using the DCP 2020 census tract → NTA crosswalk, and computed mean household income
- produced one map and three charts with captions (saved to `visualizations/`)

The current outputs of `01_analysis.ipynb` are:

```text
data/processed/manhattan_acs_income_by_tract.csv
data/processed/manhattan_hpd_units_by_nta.csv
data/processed/manhattan_acs_income_by_nta.csv
data/processed/manhattan_nta_income_hpd.csv
visualizations/map_income_hpd_buildings.png
visualizations/scatter_income_vs_affordable_units.png
visualizations/bar_top10_nta_affordable_units.png
visualizations/bar_hpd_units_by_income_band.png
```

In 02_pluto_analysis.ipynb, we have:

- Loaded the NYC PLUTO 26v2 dataset directly from its compressed ZIP file.
- Filtered the dataset to Manhattan.
- Checked for duplicate tax-lot identifiers and missing values.
- Removed records with missing residential-unit counts.
- Standardized land-use and construction-period categories.
- Saved the cleaned Manhattan PLUTO dataset to data/processed/.
- Generated two preliminary housing-stock visualizations.

The current cleaned PLUTO outputs are:

```text
data/processed/manhattan_pluto_26v2_cleaned.csv.gz
data/processed/pluto_residential_units_by_land_use.csv
data/processed/pluto_residential_units_by_construction_period.csv
visualizations/pluto_residential_units_by_land_use.png
visualizations/pluto_residential_units_by_construction_period.png
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

1. Install the required packages from the repository root:

```bash
pip install -r requirements.txt
```

2. Make sure every raw file listed under **Data Sources** below is in `data/raw/` (all of them are committed to the repository except where noted).

3. Start Jupyter and open the notebooks from the `notebooks/` folder. Each notebook uses relative paths such as `../data/raw/`, so its working directory must be `notebooks/` (Jupyter's default when you open a notebook there).

4. Run each notebook top to bottom with **Kernel → Restart & Run All**:

```text
notebooks/01_analysis.ipynb        HPD + ACS cleaning, spatial joins, NTA aggregation, figures
notebooks/02_pluto_analysis.ipynb  PLUTO cleaning and housing-stock charts
```

Cleaning steps print how many rows each filter removed. Outputs are written to `data/processed/` and figures to `visualizations/`.

## Data Sources

All raw files go in `data/raw/`. Projected CRS used throughout: **EPSG:2263** (NAD83 / New York Long Island, US feet).

| Dataset | Source | Files in `data/raw/` | How to download |
|---|---|---|---|
| 2020 Neighborhood Tabulation Areas (NTAs) | NYC Dept. of City Planning | `nynta2020.shp` (+ `.shx`, `.dbf`, `.prj`) | [NYC Planning – Community/NTA boundaries](https://www.nyc.gov/content/planning/pages/resources/datasets/neighborhood-tabulation) → "2020 Neighborhood Tabulation Areas (NTAs)", Shapefile (clipped to shoreline); unzip into `data/raw/` |
| 2020 Census Tracts (tract → NTA crosswalk) | NYC Dept. of City Planning | `nyct2020.shp` (+ `.shx`, `.dbf`, `.prj`) | [NYC Planning – Census Tracts](https://www.nyc.gov/content/planning/pages/resources/datasets/census-tracts) → "2020 Census Tracts", Shapefile (clipped to shoreline); unzip into `data/raw/` |
| ACS 2024 5-Year, B19025 Aggregate Household Income | U.S. Census Bureau | `ACSDT5Y2024.B19025-Data.csv` | [data.census.gov](https://data.census.gov) → search `B19025` → Geography: Census Tract → New York → New York County → All tracts → **Download Table Data** → check only "2024 ACS 5-Year Estimates Detailed Tables", CSV → unzip and copy the `-Data.csv` |
| ACS 2024 5-Year, B11001 Household Type (total households) | U.S. Census Bureau | `ACSDT5Y2024.B11001-Data.csv` | Same steps as above, searching `B11001` |
| ACS 2024 5-Year, B25070 Gross Rent as % of Income | U.S. Census Bureau | `ACSDT5Y2024.B25070-Data.csv` | Same steps as above, searching `B25070` (not yet used in the analysis) |
| Affordable Housing Production by Building | NYC HPD, NYC Open Data | `Affordable_Housing_Production_by_Building_20261102.csv` | [NYC Open Data hg8x-zxpr](https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr) → Export → CSV (downloaded Nov 2, 2026) |
| PLUTO 26v2 | NYC Dept. of City Planning | `nyc_pluto.zip` (read directly; not unzipped) | [NYC Planning – PLUTO and MapPLUTO](https://www.nyc.gov/content/planning/pages/resources/datasets/mappluto-pluto-change) → PLUTO (CSV), save the zip as `data/raw/nyc_pluto.zip` |

Do **not** use the "Export" button on data.census.gov tables; it produces a transposed file without `GEO_ID`. Use "Download Table Data" so the format matches the code.

## Main Datasets

- **NYC 2020 Neighborhood Tabulation Areas:** the unit of analysis (38 Manhattan NTAs).
- **NYC 2020 Census Tracts:** each tract's `NTA2020` code is used to aggregate ACS tract data to NTAs.
- **2024 ACS 5-Year Estimates:** tract-level aggregate household income and household counts, used to compute NTA mean household income.
- **NYC HPD Affordable Housing Production by Building:** affordable units started since 2014, spatially joined to NTAs.
- **NYC PLUTO 26v2:** tax-lot data on residential units, land use, and building age.

## Helper Functions

Repeated steps live in `analysis/data_processing.py` and are imported by `01_analysis.ipynb`:

- `record_drops`: logs rows and percentage removed by each cleaning step
- `process_hpd_data`: filters HPD to Manhattan, drops rows without coordinates, deduplicates on (Project ID, Building ID)
- `points_lonlat`: builds point geometries and reprojects EPSG:4326 → EPSG:2263
- `spatial_join_to_nta`: point-in-polygon join to NTAs (`predicate="within"`)
- `load_acs_table`: loads a data.census.gov ACS CSV and keeps Manhattan tracts
- `aggregate_tracts_to_nta`: sums tract income and households by NTA and computes mean household income
