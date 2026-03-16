from pathlib import Path

import pandas as pd


def read_drias_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Read a DRIAS exported CSV file.

    The file contains metadata lines starting with '#'
    and uses ';' as separator.
    """
    return pd.read_csv(
        file_path,
        sep=";",
        comment="#",
        header=None,
        names=["date", "latitude", "longitude", "tas_adjust_k", "prtot_adjust_kg_m2_s"],
    )


def read_meteo_csv_gz(file_path: str | Path) -> pd.DataFrame:
    """
    Read a Meteo-France compressed CSV (.csv.gz).
    """
    return pd.read_csv(file_path, sep=";", compression="gzip", low_memory=False)
