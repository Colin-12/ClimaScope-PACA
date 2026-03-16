"""
Central registry of external data sources for ClimaScope-PACA.
"""

DATA_SOURCES = {
    "meteo": {
        "name": "Meteo-France / data.gouv",
        "type": "historical_climate",
        "description": "Historical climate observations used for temperature, precipitation and extreme event indicators.",
        "base_url": "https://meteo.data.gouv.fr/",
        "priority": 1,
    },
    "drias": {
        "name": "DRIAS",
        "type": "climate_projections",
        "description": "Future climate projections used for 2030, 2050 and 2100 scenario analysis.",
        "base_url": "https://www.drias-climat.fr/",
        "priority": 1,
    },
    "citepa": {
        "name": "CITEPA Secten",
        "type": "ghg_emissions",
        "description": "Greenhouse gas emissions by sector used to contextualize pressure from human activities.",
        "base_url": "https://www.citepa.org/donnees-air-climat/donnees-gaz-a-effet-de-serre/secten/",
        "priority": 1,
    },
    "data_gouv_defis": {
        "name": "Defis data.gouv - Changement climatique",
        "type": "challenge_context",
        "description": "Challenge context and complementary open datasets for climate-related use cases.",
        "base_url": "https://defis.data.gouv.fr/defis/changement-climatique",
        "priority": 2,
    },
}


def list_sources() -> list[str]:
    """Return the list of registered source keys."""
    return list(DATA_SOURCES.keys())


def get_source(source_key: str) -> dict:
    """Return metadata for a given source."""
    if source_key not in DATA_SOURCES:
        raise KeyError(f"Unknown source: {source_key}")
    return DATA_SOURCES[source_key]
