# Meteo Processing Notes — ClimaScope-PACA

## Objectif
Préparer un dataset météo quotidien propre pour le département 13 à partir des 3 fichiers bruts Météo-France.

## Fichiers sources
- `meteo_dep13_daily_1786_1949_rr_t_vent_v1.csv.gz`
- `meteo_dep13_daily_1950_2024_rr_t_vent_v1.csv.gz`
- `meteo_dep13_daily_2025_2026_rr_t_vent_v1.csv.gz`

## Vérifications à faire
- confirmer les noms exacts des colonnes
- vérifier le format de la date
- vérifier les unités de température
- vérifier l’unité de `RR`
- vérifier la présence éventuelle de colonnes station / latitude / longitude

## Variables cibles
- `date`
- `station_id`
- `station_name`
- `latitude`
- `longitude`
- `tn_c`
- `tx_c`
- `tm_c`
- `rr_mm`
- `dg`

## Indicateurs dérivés
- `hot_day_over_30`
- `frost_day`
- `dry_day`

## Sorties attendues
- `data/processed/climate/meteo_dep13_daily_normalized_v1.csv`
- `data/processed/climate/meteo_dep13_daily_normalized_v1.parquet`
