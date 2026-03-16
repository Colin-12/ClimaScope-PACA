from pathlib import Path

import pandas as pd

from .inspect_meteo import read_meteo_file


def normalize_column_name(col: str) -> str:
    return (
        str(col)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
    )


def find_first_matching_column(columns: list[str], candidates: list[str]) -> str | None:
    normalized = {normalize_column_name(col): col for col in columns}

    for candidate in candidates:
        candidate_norm = normalize_column_name(candidate)
        if candidate_norm in normalized:
            return normalized[candidate_norm]

    return None


def to_numeric_safe(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(",", ".", regex=False),
        errors="coerce",
    )


def load_and_standardize_meteo_file(file_path: str | Path) -> pd.DataFrame:
    df = read_meteo_file(file_path).copy()
    original_columns = list(df.columns)

    date_col = find_first_matching_column(
        original_columns,
        ["DATE", "date", "AAAAMMJJ", "date_obs"],
    )
    station_col = find_first_matching_column(
        original_columns,
        ["NUM_POSTE", "num_poste", "station_id", "poste"],
    )
    rr_col = find_first_matching_column(
        original_columns,
        ["RR", "rr", "precipitations", "precipitation"],
    )
    tn_col = find_first_matching_column(
        original_columns,
        ["TN", "tn", "tmin", "temp_min"],
    )
    tx_col = find_first_matching_column(
        original_columns,
        ["TX", "tx", "tmax", "temp_max"],
    )
    tm_col = find_first_matching_column(
        original_columns,
        ["TM", "tm", "tmoy", "temp_moy", "temperature_moyenne"],
    )
    dg_col = find_first_matching_column(
        original_columns,
        ["DG", "dg", "duree_gel"],
    )
    lat_col = find_first_matching_column(
        original_columns,
        ["LAT", "lat", "latitude"],
    )
    lon_col = find_first_matching_column(
        original_columns,
        ["LON", "lon", "longitude"],
    )
    name_col = find_first_matching_column(
        original_columns,
        ["NOM_USUEL", "nom_usuel", "nom_station", "libelle_station"],
    )

    result = pd.DataFrame()

    if date_col is not None:
        result["date"] = pd.to_datetime(df[date_col], errors="coerce")
    else:
        result["date"] = pd.NaT

    result["source_file"] = Path(file_path).name

    if station_col is not None:
        result["station_id"] = df[station_col].astype(str)
    if name_col is not None:
        result["station_name"] = df[name_col].astype(str)

    if lat_col is not None:
        result["latitude"] = to_numeric_safe(df[lat_col])
    if lon_col is not None:
        result["longitude"] = to_numeric_safe(df[lon_col])

    if rr_col is not None:
        result["rr_mm"] = to_numeric_safe(df[rr_col])
    if tn_col is not None:
        result["tn_c"] = to_numeric_safe(df[tn_col])
    if tx_col is not None:
        result["tx_c"] = to_numeric_safe(df[tx_col])
    if tm_col is not None:
        result["tm_c"] = to_numeric_safe(df[tm_col])
    if dg_col is not None:
        result["dg"] = to_numeric_safe(df[dg_col])

    result["year"] = result["date"].dt.year
    result["month"] = result["date"].dt.month

    if "tx_c" in result.columns:
        result["hot_day_over_30"] = result["tx_c"] > 30
    else:
        result["hot_day_over_30"] = pd.NA

    if "tn_c" in result.columns:
        result["frost_day"] = result["tn_c"] < 0
    else:
        result["frost_day"] = pd.NA

    if "rr_mm" in result.columns:
        result["dry_day"] = result["rr_mm"] == 0
    else:
        result["dry_day"] = pd.NA

    return result


def combine_meteo_files(file_paths: list[str | Path]) -> pd.DataFrame:
    frames = [load_and_standardize_meteo_file(path) for path in file_paths]
    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values(["date"], na_position="last").reset_index(drop=True)
    return combined


def save_meteo_processed(df: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "meteo_dep13_daily_normalized_v1.csv"
    parquet_path = output_dir / "meteo_dep13_daily_normalized_v1.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    print(f"Saved CSV: {csv_path}")
    print(f"Saved Parquet: {parquet_path}")


if __name__ == "__main__":
    files = [
        "data/raw/meteo/Q_13_1786-1949_RR-T-Vent.csv.gz",
        "data/raw/meteo/Q_13_previous-1950-2024_RR-T-Vent.csv.gz",
        "data/raw/meteo/Q_13_latest-2025-2026_RR-T-Vent.csv.gz",
    ]

    df = combine_meteo_files(files)
    print(df.head())
    print(df.columns.tolist())
    print(df.shape)

    save_meteo_processed(df, "data/processed/climate")
