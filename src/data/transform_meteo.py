from pathlib import Path

import pandas as pd

from .inspect_meteo import read_meteo_file


def load_and_standardize_meteo_file(file_path: str | Path) -> pd.DataFrame:
    """
    Load one Meteo-France daily raw file and return a standardized dataframe.
    """
    df = read_meteo_file(file_path).copy()

    result = pd.DataFrame()

    result["date"] = pd.to_datetime(df["AAAAMMJJ"].astype(str), format="%Y%m%d", errors="coerce")
    result["year"] = result["date"].dt.year
    result["month"] = result["date"].dt.month

    result["station_id"] = df["NUM_POSTE"].astype(str)
    result["station_name"] = df["NOM_USUEL"].astype(str)

    result["latitude"] = pd.to_numeric(df["LAT"], errors="coerce")
    result["longitude"] = pd.to_numeric(df["LON"], errors="coerce")
    result["altitude_m"] = pd.to_numeric(df["ALTI"], errors="coerce")

    result["rr_mm"] = pd.to_numeric(df["RR"], errors="coerce")
    result["tn_c"] = pd.to_numeric(df["TN"], errors="coerce")
    result["tx_c"] = pd.to_numeric(df["TX"], errors="coerce")
    result["tm_c"] = pd.to_numeric(df["TM"], errors="coerce")
    result["dg"] = pd.to_numeric(df["DG"], errors="coerce")

    result["qrr"] = pd.to_numeric(df["QRR"], errors="coerce")
    result["qtn"] = pd.to_numeric(df["QTN"], errors="coerce")
    result["qtx"] = pd.to_numeric(df["QTX"], errors="coerce")
    result["qtm"] = pd.to_numeric(df["QTM"], errors="coerce")
    result["qdg"] = pd.to_numeric(df["QDG"], errors="coerce")

    result["hot_day_over_30"] = result["tx_c"] > 30
    result["frost_day"] = result["tn_c"] < 0
    result["dry_day"] = result["rr_mm"] == 0

    result["source_file"] = Path(file_path).name

    return result


def combine_meteo_files(file_paths: list[str | Path]) -> pd.DataFrame:
    frames = [load_and_standardize_meteo_file(path) for path in file_paths]
    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values(["date", "station_id"], na_position="last").reset_index(drop=True)
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
    print(df[["date", "station_id", "station_name", "rr_mm", "tn_c", "tx_c", "tm_c", "dg"]].head())

    save_meteo_processed(df, "data/processed/climate")
