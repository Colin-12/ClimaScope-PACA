from pathlib import Path

import pandas as pd


def read_meteo_file(file_path: str | Path) -> pd.DataFrame:
    """
    Read a Meteo-France raw CSV.GZ file with a few encoding fallbacks.
    """
    file_path = Path(file_path)

    errors = []
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            return pd.read_csv(
                file_path,
                sep=";",
                compression="gzip",
                encoding=encoding,
                low_memory=False,
            )
        except Exception as exc:
            errors.append(f"{encoding}: {exc}")

    raise RuntimeError(
        f"Unable to read file {file_path}. Tried encodings:\n" + "\n".join(errors)
    )


def inspect_file(file_path: str | Path, n_rows: int = 5) -> None:
    df = read_meteo_file(file_path)

    print("=" * 100)
    print(f"FILE: {file_path}")
    print("=" * 100)
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    for col in df.columns:
        print(f"- {col}")

    print("\nDtypes:")
    print(df.dtypes)

    print("\nHead:")
    print(df.head(n_rows))

    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).head(20))


if __name__ == "__main__":
    files = [
        "data/raw/meteo/Q_13_1786-1949_RR-T-Vent.csv.gz",
        "data/raw/meteo/Q_13_previous-1950-2024_RR-T-Vent.csv.gz",
        "data/raw/meteo/Q_13_latest-2025-2026_RR-T-Vent.csv.gz",
    ]

    for file_path in files:
        inspect_file(file_path)
