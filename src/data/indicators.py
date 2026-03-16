"""
Indicator registry for ClimaScope-PACA.
"""

INDICATORS = {
    "avg_annual_temperature": {
        "label": "Température moyenne annuelle",
        "family": "climate_change",
        "unit": "°C",
        "source": "meteo",
        "projected": True,
        "used_in_score": False,
    },
    "hot_days_over_30": {
        "label": "Jours de forte chaleur (>30°C)",
        "family": "climate_change",
        "unit": "days",
        "source": "meteo",
        "projected": True,
        "used_in_score": True,
    },
    "frost_days": {
        "label": "Jours de gel",
        "family": "climate_change",
        "unit": "days",
        "source": "meteo",
        "projected": True,
        "used_in_score": False,
    },
    "annual_precipitation": {
        "label": "Cumul annuel de précipitations",
        "family": "climate_change",
        "unit": "mm",
        "source": "meteo",
        "projected": True,
        "used_in_score": True,
    },
    "max_dry_spell_length": {
        "label": "Longueur maximale des séquences sèches",
        "family": "climate_change",
        "unit": "days",
        "source": "meteo",
        "projected": True,
        "used_in_score": True,
    },
    "ghg_transport": {
        "label": "Émissions de GES du transport",
        "family": "human_pressure",
        "unit": "tCO2e",
        "source": "citepa",
        "projected": False,
        "used_in_score": True,
    },
    "ghg_buildings": {
        "label": "Émissions de GES du résidentiel-tertiaire",
        "family": "human_pressure",
        "unit": "tCO2e",
        "source": "citepa",
        "projected": False,
        "used_in_score": True,
    },
    "wildfire_pressure": {
        "label": "Fréquence ou intensité des feux de forêt",
        "family": "visible_impact",
        "unit": "index",
        "source": "impacts",
        "projected": False,
        "used_in_score": True,
    },
}


def list_indicator_keys() -> list[str]:
    """Return all indicator keys."""
    return list(INDICATORS.keys())


def get_indicator(indicator_key: str) -> dict:
    """Return one indicator definition."""
    if indicator_key not in INDICATORS:
        raise KeyError(f"Unknown indicator: {indicator_key}")
    return INDICATORS[indicator_key]
