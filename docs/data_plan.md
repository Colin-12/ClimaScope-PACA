# Data Plan — ClimaScope-PACA

## Objectif
Définir les sources, les variables, la granularité et la logique de transformation des données utilisées dans le projet.

## Territoire MVP
- Région PACA
- Zoom local : Marseille / Bouches-du-Rhône

## Sources pressenties

### 1. Données climatiques historiques
- Source : Météo-France / meteo.data.gouv.fr
- Usage : température, précipitations, jours chauds, jours de gel
- Niveau attendu : station / commune / département selon disponibilité

### 2. Projections climatiques futures
- Source : DRIAS
- Usage : projections 2030 / 2050 / 2100
- Scénarios : optimiste, médian, pessimiste

### 3. Émissions de gaz à effet de serre
- Source : CITEPA Secten
- Usage : émissions par secteur
- Niveau attendu : France / éventuellement régionalisable selon disponibilité

### 4. Données d’impact et vulnérabilité
- Source : à préciser selon disponibilité
- Usage : feux, catastrophes, exposition territoriale

## Indicateurs pressentis
1. Température moyenne annuelle
2. Nombre de jours de forte chaleur (>30°C)
3. Nombre de jours de gel
4. Cumul annuel de précipitations
5. Indicateur sécheresse / déficit hydrique
6. Émissions GES par secteur
7. Empreinte carbone
8. Impact ou exposition aux aléas

## Structure de stockage

### Raw
Données brutes téléchargées sans modification :
- `data/raw/meteo/`
- `data/raw/drias/`
- `data/raw/citepa/`
- `data/raw/impacts/`

### Processed
Données nettoyées et transformées :
- `data/processed/climate/`
- `data/processed/projections/`
- `data/processed/emissions/`
- `data/processed/final/`

## Convention de nommage
Format conseillé :
`source_zone_granularite_periode.csv`

Exemples :
- `meteo_paca_station_daily_1950_2024.csv`
- `drias_paca_grid_rcp45_2030_2100.csv`
- `citepa_france_sector_annual_1990_2024.csv`

## Principes
- toujours conserver une copie brute des données
- séparer clairement raw et processed
- documenter toute transformation
- éviter les traitements manuels non traçables
