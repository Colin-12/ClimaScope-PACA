from pathlib import Path

import pandas as pd


def build_station_profile(df: pd.DataFrame) -> pd.DataFrame:
    profile = (
        df.groupby(["station_id", "station_name", "latitude", "longitude", "altitude_m"], dropna=False)
        .agg(
            min_date=("date", "min"),
            max_date=("date", "max"),
            n_rows=("date", "count"),
            n_years=("year", "nunique"),
            missing_tm=("tm_c", lambda s: s.isna().sum()),
            missing_tx=("tx_c", lambda s: s.isna().sum()),
            missing_tn=("tn_c", lambda s: s.isna().sum()),
            missing_rr=("rr_mm", lambda s: s.isna().sum()),
        )
        .reset_index()
        .sort_values(["n_years", "n_rows"], ascending=[False, False])
        .reset_index(drop=True)
    )

    return profile


def save_station_profile(df: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "meteo_dep13_station_profile_v1.csv"
    parquet_path = output_dir / "meteo_dep13_station_profile_v1.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    print(f"Saved CSV: {csv_path}")
    print(f"Saved Parquet: {parquet_path}")


if __name__ == "__main__":
    input_path = "data/processed/climate/meteo_dep13_daily_normalized_v1.parquet"

    df = pd.read_parquet(input_path)
    profile = build_station_profile(df)

    print(profile.head(10))
    print(profile.columns.tolist())
    print(profile.shape)

    save_station_profile(profile, "data/processed/climate")
    