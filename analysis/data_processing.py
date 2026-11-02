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
