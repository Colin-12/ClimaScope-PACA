from pathlib import Path

import pandas as pd


RAW_DRIAS_FILE = "data/raw/drias/drias_projection_raw_v1.csv"

OUTPUT_DIR = Path("data/processed/climate")
OUTPUT_CSV = OUTPUT_DIR / "drias_projection_pilot_v1.csv"
OUTPUT_PARQUET = OUTPUT_DIR / "drias_projection_pilot_v1.parquet"


def read_drias_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Lit un export DRIAS brut.

    Le fichier :
    - contient des lignes de métadonnées commençant par '#'
    - utilise ';' comme séparateur
    - ne contient pas forcément d'en-tête exploitable directement
    """
    return pd.read_csv(
        file_path,
        sep=";",
        comment="#",
        header=None,
        names=[
            "date",
            "latitude",
            "longitude",
            "tas_adjust_k",
            "prtot_adjust_kg_m2_s",
        ],
    )


def transform_drias_projection(file_path: str | Path) -> pd.DataFrame:
    """
    Transforme un export DRIAS brut en dataframe exploitable.

    Conversions :
    - tas_adjust_k -> tas_c (Kelvin vers Celsius)
    - prtot_adjust_kg_m2_s -> pr_mm_day (kg/m²/s vers mm/jour)
    """
    df = read_drias_csv(file_path).copy()

    df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d", errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["tas_adjust_k"] = pd.to_numeric(df["tas_adjust_k"], errors="coerce")
    df["prtot_adjust_kg_m2_s"] = pd.to_numeric(df["prtot_adjust_kg_m2_s"], errors="coerce")

    # Conversions d'unités
    df["tas_c"] = df["tas_adjust_k"] - 273.15
    df["pr_mm_day"] = df["prtot_adjust_kg_m2_s"] * 86400

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["scenario"] = "RCP4.5"
    df["model_chain"] = "CNRM-CERFACS-CNRM-CM5 / CNRM-ALADIN63 / ADAMONT"
    df["source_file"] = Path(file_path).name

    return df[
        [
            "date",
            "year",
            "month",
            "latitude",
            "longitude",
            "tas_adjust_k",
            "tas_c",
            "prtot_adjust_kg_m2_s",
            "pr_mm_day",
            "scenario",
            "model_chain",
            "source_file",
        ]
    ]


def save_outputs(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_CSV, index=False)
    df.to_parquet(OUTPUT_PARQUET, index=False)

    print(f"Saved CSV: {OUTPUT_CSV}")
    print(f"Saved Parquet: {OUTPUT_PARQUET}")


def print_quick_checks(df: pd.DataFrame) -> None:
    print("\n=== HEAD ===")
    print(df.head())

    print("\n=== COLUMNS ===")
    print(df.columns.tolist())

    print("\n=== SHAPE ===")
    print(df.shape)

    print("\n=== DATE RANGE ===")
    print(df["date"].min(), "->", df["date"].max())

    print("\n=== YEAR RANGE ===")
    print(df["year"].min(), "->", df["year"].max())

    print("\n=== TAS_C SUMMARY ===")
    print(df["tas_c"].describe())

    print("\n=== PR_MM_DAY SUMMARY ===")
    print(df["pr_mm_day"].describe())

    if {"latitude", "longitude"}.issubset(df.columns):
        print("\n=== SAMPLE GRID POINTS ===")
        print(df[["latitude", "longitude"]].drop_duplicates().head(10))


if __name__ == "__main__":
    input_path = Path(RAW_DRIAS_FILE)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Fichier DRIAS introuvable : {input_path}\n"
            "Vérifie qu'il est bien placé dans data/raw/drias/ avec ce nom exact."
        )

    df = transform_drias_projection(input_path)
    print_quick_checks(df)
    save_outputs(df)