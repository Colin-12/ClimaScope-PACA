from pathlib import Path

import pandas as pd


def build_department_annual_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate annual indicators at department level (dept 13),
    using the average across stations for each year.
    """
    annual = (
        df.groupby("year", dropna=False)
        .agg(
            station_count=("station_id", "nunique"),
            avg_annual_temperature_c=("avg_annual_temperature_c", "mean"),
            annual_precipitation_mm=("annual_precipitation_mm", "mean"),
            hot_days_over_30=("hot_days_over_30", "mean"),
            frost_days=("frost_days", "mean"),
            dry_days=("dry_days", "mean"),
            avg_daily_gel_duration=("avg_daily_gel_duration", "mean"),
            max_dry_spell_length=("max_dry_spell_length", "mean"),
        )
        .reset_index()
    )

    annual["territory"] = "Bouches-du-Rhone"
    annual["territory_code"] = "13"

    return annual[
        [
            "territory",
            "territory_code",
            "year",
            "station_count",
            "avg_annual_temperature_c",
            "annual_precipitation_mm",
            "hot_days_over_30",
            "frost_days",
            "dry_days",
            "avg_daily_gel_duration",
            "max_dry_spell_length",
        ]
    ].sort_values("year").reset_index(drop=True)


def save_department_indicators(df: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "meteo_dep13_annual_indicators_department_v1.csv"
    parquet_path = output_dir / "meteo_dep13_annual_indicators_department_v1.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    print(f"Saved CSV: {csv_path}")
    print(f"Saved Parquet: {parquet_path}")


if __name__ == "__main__":
    input_path = "data/processed/climate/meteo_dep13_annual_indicators_by_station_v1.parquet"

    df = pd.read_parquet(input_path)
    department = build_department_annual_indicators(df)

    print(department.head())
    print(department.columns.tolist())
    print(department.shape)

    save_department_indicators(department, "data/processed/climate")