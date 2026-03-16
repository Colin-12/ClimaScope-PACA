from pathlib import Path

import pandas as pd


HERO_STATION_ID = "13055001"
HERO_STATION_NAME = "MARSEILLE-OBS"


def build_hero_station_daily(df: pd.DataFrame) -> pd.DataFrame:
    hero = df[df["station_id"] == HERO_STATION_ID].copy()
    hero = hero.sort_values("date").reset_index(drop=True)
    hero["territory"] = "Marseille"
    hero["territory_code"] = HERO_STATION_ID
    return hero


def build_hero_station_annual(df: pd.DataFrame) -> pd.DataFrame:
    hero = df[df["station_id"] == HERO_STATION_ID].copy()
    hero = hero.sort_values("year").reset_index(drop=True)
    hero["territory"] = "Marseille"
    hero["territory_code"] = HERO_STATION_ID
    return hero


def save_dashboard_datasets(
    hero_daily: pd.DataFrame,
    hero_annual: pd.DataFrame,
    dept_annual: pd.DataFrame,
    output_dir: str | Path,
) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "dashboard_hero_station_daily_v1.csv": hero_daily,
        "dashboard_hero_station_daily_v1.parquet": hero_daily,
        "dashboard_hero_station_annual_v1.csv": hero_annual,
        "dashboard_hero_station_annual_v1.parquet": hero_annual,
        "dashboard_department_annual_v1.csv": dept_annual,
        "dashboard_department_annual_v1.parquet": dept_annual,
    }

    for file_name, df in files.items():
        path = output_dir / file_name
        if file_name.endswith(".csv"):
            df.to_csv(path, index=False)
        else:
            df.to_parquet(path, index=False)
        print(f"Saved: {path}")


if __name__ == "__main__":
    daily_path = "data/processed/climate/meteo_dep13_daily_normalized_v1.parquet"
    annual_station_path = "data/processed/climate/meteo_dep13_annual_indicators_by_station_v1.parquet"
    annual_dept_path = "data/processed/climate/meteo_dep13_annual_indicators_department_v1.parquet"

    daily_df = pd.read_parquet(daily_path)
    annual_station_df = pd.read_parquet(annual_station_path)
    annual_dept_df = pd.read_parquet(annual_dept_path)

    hero_daily = build_hero_station_daily(daily_df)
    hero_annual = build_hero_station_annual(annual_station_df)

    print(hero_daily.head())
    print(hero_annual.head())
    print(annual_dept_df.head())

    save_dashboard_datasets(
        hero_daily=hero_daily,
        hero_annual=hero_annual,
        dept_annual=annual_dept_df,
        output_dir="data/processed/final",
    )