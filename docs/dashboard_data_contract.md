# Dashboard Data Contract — ClimaScope-PACA

## Fichiers utilisés par le dashboard

### 1. Vue station héroïne — journalier
- `data/processed/final/dashboard_hero_station_daily_v1.parquet`
- Niveau : station Marseille-OBS
- Granularité : jour
- Usage : séries détaillées, extrêmes, exemples locaux

### 2. Vue station héroïne — annuel
- `data/processed/final/dashboard_hero_station_annual_v1.parquet`
- Niveau : station Marseille-OBS
- Granularité : année
- Usage : tendances longues

### 3. Vue départementale — annuel
- `data/processed/final/dashboard_department_annual_v1.parquet`
- Niveau : département 13
- Granularité : année
- Usage : vue territoire consolidée

## Remarque méthodologique
La vue départementale est une série composite indicative calculée à partir de la moyenne des stations disponibles par année.
Elle sert à la narration territoriale du dashboard et ne remplace pas une série homogénéisée officielle.