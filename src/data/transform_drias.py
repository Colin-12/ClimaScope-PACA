from pathlib import Path

import pandas as pd

from .readers import read_drias_csv


def transform_drias_projection(file_path: str | Path) -> pd.DataFrame:
    """
    Load and transform a DRIAS projection file into an analysis-ready dataframe.
    """
    df = read_drias_csv(file_path).copy()

    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d", errors="coerce")
    df["tas_c"] = df["tas_adjust_k"] - 273.15
    df["pr_mm_day"] = df["prtot_adjust_kg_m2_s"] * 86400

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

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
        ]
    ]


if __name__ == "__main__":
    sample_path = "data/raw/drias/tasAdjustprtotAdjust_France_CNRM-CERFACS-CNRM-CM5_CNRM-ALADIN63_rcp4.5_METEO-FRANCE_ADAMONT-France_SAFRAN_day_20310101-20601231.csv"
    df = transform_drias_projection(sample_path)
    print(df.head())
    print(df.info())
