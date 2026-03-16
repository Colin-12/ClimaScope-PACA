# Source Inventory — ClimaScope-PACA

## Objectif
Lister les sources officielles, le type de données attendu, le mode d’acquisition et le statut de chaque source pour le MVP.

## Principes
- utiliser d’abord les sources obligatoires du cahier des charges
- documenter toute source ajoutée
- garder une trace du mode d’acquisition
- ne pas committer de gros fichiers bruts dans le repository

## Sources cibles

### 1. Météo-France / meteo.data.gouv.fr
- **source_key** : `meteo`
- **type** : données climatiques historiques
- **usage** : température, précipitations, jours chauds, jours de gel, séquences sèches
- **niveau visé** : station / département / région selon disponibilité
- **format attendu** : CSV, CSV.GZ, JSON
- **mode d’acquisition** : téléchargement direct ou script HTTP
- **statut** : à faire

### 2. DRIAS
- **source_key** : `drias`
- **type** : projections climatiques futures
- **usage** : projections 2030 / 2050 / 2100
- **niveau visé** : région / grille / indicateurs agrégés
- **format attendu** : CSV, NetCDF, ZIP
- **mode d’acquisition** : téléchargement portail / script si URL directe
- **statut** : à faire

### 3. CITEPA Secten
- **source_key** : `citepa`
- **type** : émissions de gaz à effet de serre
- **usage** : transport, résidentiel-tertiaire, contexte pression humaine
- **niveau visé** : national avec possibilité d’agrégation ou contextualisation territoriale
- **format attendu** : XLSX, CSV, PDF
- **mode d’acquisition** : téléchargement direct
- **statut** : à faire

### 4. Données d’impact / feux / aléas
- **source_key** : `impacts`
- **type** : événements extrêmes
- **usage** : feux de forêt, pression incendie, exposition
- **niveau visé** : PACA / département / commune selon disponibilité
- **format attendu** : CSV, GeoJSON, SHP
- **mode d’acquisition** : à préciser
- **statut** : à faire

## Fichiers attendus pour le MVP
- un historique climatique exploitable
- un fichier de projections climatiques
- un fichier émissions GES par secteur
- un fichier impact visible / aléa

## Convention de nommage
Format recommandé :
`source_zone_granularite_periode_version.ext`

Exemples :
- `meteo_paca_station_daily_1950_2024_v1.csv`
- `drias_paca_grid_rcp45_2030_2100_v1.nc`
- `citepa_france_sector_annual_1990_2024_v1.xlsx`

## Suivi
Chaque téléchargement devra être tracé dans un manifeste.
