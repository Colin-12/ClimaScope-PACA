from pathlib import Path

import pandas as pd


def longest_true_streak(series: pd.Series) -> int:
    """
    Return the maximum consecutive streak length for True values.
    """
    max_streak = 0
    current = 0

    for value in series.fillna(False):
        if bool(value):
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0

    return max_streak


def build_annual_station_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build annual climate indicators by station and year.
    """
    group_cols = ["station_id", "station_name", "latitude", "longitude", "altitude_m", "year"]

    annual = (
        df.groupby(group_cols, dropna=False)
        .agg(
            avg_annual_temperature_c=("tm_c", "mean"),
            annual_precipitation_mm=("rr_mm", "sum"),
            hot_days_over_30=("hot_day_over_30", "sum"),
            frost_days=("frost_day", "sum"),
            dry_days=("dry_day", "sum"),
            avg_daily_gel_duration=("dg", "mean"),
        )
        .reset_index()
    )

    dry_spell = (
        df.sort_values(["station_id", "date"])
        .groupby(["station_id", "year"], dropna=False)["dry_day"]
        .apply(longest_true_streak)
        .reset_index(name="max_dry_spell_length")
    )

    annual = annual.merge(dry_spell, on=["station_id", "year"], how="left")

    return annual.sort_values(["year", "station_id"]).reset_index(drop=True)


def save_annual_indicators(df: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "meteo_dep13_annual_indicators_by_station_v1.csv"
    parquet_path = output_dir / "meteo_dep13_annual_indicators_by_station_v1.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    print(f"Saved CSV: {csv_path}")
    print(f"Saved Parquet: {parquet_path}")


if __name__ == "__main__":
    input_path = "data/processed/climate/meteo_dep13_daily_normalized_v1.parquet"

    df = pd.read_parquet(input_path)
    annual = build_annual_station_indicators(df)

    print(annual.head())
    print(annual.columns.tolist())
    print(annual.shape)

    save_annual_indicators(annual, "data/processed/climate")
