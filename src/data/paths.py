from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_METEO_DIR = RAW_DIR / "meteo"
RAW_DRIAS_DIR = RAW_DIR / "drias"
RAW_CITEPA_DIR = RAW_DIR / "citepa"
RAW_IMPACTS_DIR = RAW_DIR / "impacts"

PROCESSED_CLIMATE_DIR = PROCESSED_DIR / "climate"
PROCESSED_PROJECTIONS_DIR = PROCESSED_DIR / "projections"
PROCESSED_EMISSIONS_DIR = PROCESSED_DIR / "emissions"
PROCESSED_FINAL_DIR = PROCESSED_DIR / "final"

RAW_MANIFEST_PATH = RAW_DIR / "download_manifest.csv"


def ensure_data_dirs() -> None:
    """Create all required data directories if they do not exist."""
    directories = [
        RAW_DIR,
        PROCESSED_DIR,
        RAW_METEO_DIR,
        RAW_DRIAS_DIR,
        RAW_CITEPA_DIR,
        RAW_IMPACTS_DIR,
        PROCESSED_CLIMATE_DIR,
        PROCESSED_PROJECTIONS_DIR,
        PROCESSED_EMISSIONS_DIR,
        PROCESSED_FINAL_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
