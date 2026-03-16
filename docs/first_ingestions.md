# First Ingestions — ClimaScope-PACA

## Objectif
Figer les 3 premiers jeux de données à intégrer dans le pipeline raw.

## Jeu 1 — Météo-France / data.gouv
- **source_key** : `meteo`
- **niveau cible** : département 13 (Bouches-du-Rhône)
- **type** : historique quotidien
- **usage** : température moyenne, jours >30°C, jours de gel, précipitations, séquences sèches
- **format attendu** : `csv.gz`
- **mode d’acquisition** : téléchargement depuis la page officielle data.gouv
- **statut** : à récupérer

## Jeu 2 — CITEPA Secten
- **source_key** : `citepa`
- **niveau cible** : France
- **type** : émissions GES par secteur
- **usage** : transport, résidentiel-tertiaire
- **format attendu** : `zip`
- **mode d’acquisition** : téléchargement direct
- **statut** : à récupérer

## Jeu 3 — DRIAS
- **source_key** : `drias`
- **niveau cible** : région PACA
- **type** : projections climatiques
- **usage** : 2030 / 2050 / 2100, scénarios, température, précipitations, chaleur, gel
- **format attendu** : `csv` ou `nc`
- **mode d’acquisition** : extraction personnalisée depuis le portail DRIAS
- **statut** : compte requis puis export à faire

## Priorité
1. Météo historique
2. CITEPA sectoriel
3. DRIAS projections
