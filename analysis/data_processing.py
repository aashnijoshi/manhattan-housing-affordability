import pandas as pd
import geopandas as gpd

HPD_COLUMNS = [
    "Project ID",
    "Project Name",
    "Building ID",
    "Project Start Date",
    "Reporting Construction Type",
    "Latitude",
    "Longitude",
    "Extremely Low Income Units",
    "Very Low Income Units",
    "Low Income Units",
    "Moderate Income Units",
    "Middle Income Units",
    "Other Income Units",
    "All Counted Units",
    "Total Units",]

def record_drops(label, before, after):
    removed = before - after
    if before:
        p = removed / before * 100
    else:
        p = 0
    print(f"{label}: ({p:.2f}%) removed from {before} to {after}")

def process_hpd_data(path, borough="Manhattan"):
    df = pd.read_csv(path)
    initial_rows = len(df)
    manhattan_df = df[df['Borough'] == borough].copy()
    record_drops("Manhattan filter", initial_rows, len(manhattan_df))
    valid_cord = manhattan_df['Latitude'].notnull() & manhattan_df['Longitude'].notnull()
    located_df = manhattan_df[valid_cord].copy()
    record_drops("Missing coordinates filter", len(manhattan_df), len(located_df))
    dedup = located_df.drop_duplicates(subset=['Project ID', 'Building ID']).copy()
    record_drops("Deduplication filter", len(located_df), len(dedup))
    clean_df = dedup[HPD_COLUMNS].copy()
    unit_cols = [
        "Extremely Low Income Units",
        "Very Low Income Units",
        "Low Income Units",
        "Moderate Income Units",
        "Middle Income Units",
        "Other Income Units",
        "All Counted Units",
        "Total Units",
    ]
    for col in unit_cols:
        clean_df[col] = pd.to_numeric(
            clean_df[col].astype(str).str.replace(",", ""), errors="coerce"
        ).fillna(0)
    return clean_df

def points_lonlat(df):
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']),
        crs="EPSG:4326"
    )
    return gdf.to_crs("EPSG:2263")  # Convert to NAD83 / New York Long Island (ftUS)

def spatial_join_to_nta(points_gdf, nta_gdf, nta_cols):
    if points_gdf.crs != nta_gdf.crs:
        points_gdf = points_gdf.to_crs(nta_gdf.crs)
    initial_count = len(points_gdf)
    joined = gpd.sjoin(points_gdf, nta_gdf[nta_cols + ["geometry"]], how="inner", predicate="within")
    joined = joined.drop(columns=["index_right"]).copy()
    record_drops("Spatial join to NTA", initial_count, len(joined))
    return joined

def load_acs_table(file_path, id_col, columns=None, rename_dict=None):
    df = pd.read_csv(file_path, skiprows=[1])
    initial_rows = len(df)
    df = df[df[id_col].astype(str).str.startswith("1400000US36061")].copy()
    record_drops("Manhattan tract filter", initial_rows, len(df))
    df["tract_geoid"] = df[id_col].astype(str).str.replace("1400000US", "")
    if columns:
        cols_to_keep = ["tract_geoid"] + [c for c in columns if c in df.columns]
        df = df[cols_to_keep].copy()
    if rename_dict:
        df = df.rename(columns=rename_dict)
    num_cols = [c for c in df.columns if c != "tract_geoid"]
    for c in num_cols:
        df[c] = pd.to_numeric(
            df[c].astype(str).str.replace(",", ""), errors="coerce"
        )
    return df

def aggregate_tracts_to_nta(acs_tract_df, crosswalk_df):
    merged = acs_tract_df.merge(
        crosswalk_df[["GEOID", "NTA2020"]],
        left_on="tract_geoid",
        right_on="GEOID",
        how="inner",
        validate="many_to_one",)
    record_drops("Tract to NTA crosswalk", len(acs_tract_df), len(merged))
    acs_nta = (
        merged.groupby("NTA2020")
        .agg(
            aggregate_household_income=("aggregate_household_income", "sum"),
            total_households=("total_households", "sum"),
        )
        .reset_index())
    acs_nta["mean_household_income"] = (
        acs_nta["aggregate_household_income"] / acs_nta["total_households"]
    ).where(acs_nta["total_households"] > 0)
    return acs_nta