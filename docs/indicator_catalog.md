# Indicator Catalog — ClimaScope-PACA

## Objectif
Documenter les 8 indicateurs retenus pour le MVP, leur rôle métier, leur source, leur usage analytique et leur valeur citoyenne.

## Indicateurs retenus

### 1. Température moyenne annuelle
- **Famille** : Évolution climatique
- **Définition** : moyenne annuelle des températures observées
- **Source principale** : Météo-France / meteo.data.gouv.fr
- **Projection** : oui, via DRIAS
- **Usage dashboard** : tendance historique + comparaison passé / futur
- **Usage citoyen** : rendre visible le réchauffement local
- **Usage score** : secondaire

### 2. Nombre de jours de forte chaleur (>30°C)
- **Famille** : Évolution climatique
- **Définition** : nombre annuel de jours dont la température maximale dépasse 30°C
- **Source principale** : Météo-France / meteo.data.gouv.fr
- **Projection** : oui, via DRIAS
- **Usage dashboard** : indicateur clé de canicule
- **Usage citoyen** : santé, confort urbain, adaptation du logement
- **Usage score** : principal

### 3. Nombre de jours de gel
- **Famille** : Évolution climatique
- **Définition** : nombre annuel de jours dont la température minimale est inférieure à 0°C
- **Source principale** : Météo-France / meteo.data.gouv.fr
- **Projection** : oui, via DRIAS
- **Usage dashboard** : contraste climatique et évolution saisonnière
- **Usage citoyen** : agriculture, biodiversité, saisonnalité
- **Usage score** : secondaire

### 4. Cumul annuel de précipitations
- **Famille** : Évolution climatique
- **Définition** : quantité totale annuelle de précipitations
- **Source principale** : Météo-France / meteo.data.gouv.fr
- **Projection** : oui, via DRIAS
- **Usage dashboard** : stress hydrique et contraste avec chaleur
- **Usage citoyen** : ressource en eau, irrigation, adaptation locale
- **Usage score** : principal

### 5. Longueur maximale des séquences sèches
- **Famille** : Évolution climatique
- **Définition** : plus longue séquence annuelle de jours secs consécutifs
- **Source principale** : calcul dérivé à partir des données de précipitations
- **Projection** : oui, si dérivable des données DRIAS
- **Usage dashboard** : proxy de sécheresse lisible
- **Usage citoyen** : gestion de l’eau, végétation, prévention incendie
- **Usage score** : principal

### 6. Émissions de GES du transport
- **Famille** : Pressions humaines
- **Définition** : émissions de gaz à effet de serre associées au secteur transport
- **Source principale** : CITEPA Secten
- **Projection** : non prioritaire dans le MVP
- **Usage dashboard** : levier d’action majeur
- **Usage citoyen** : mobilité douce, report modal
- **Usage score** : principal

### 7. Émissions de GES du résidentiel-tertiaire / bâtiment
- **Famille** : Pressions humaines
- **Définition** : émissions liées au chauffage, aux bâtiments et à leur usage
- **Source principale** : CITEPA Secten
- **Projection** : non prioritaire dans le MVP
- **Usage dashboard** : levier d’action local concret
- **Usage citoyen** : rénovation énergétique, sobriété
- **Usage score** : principal

### 8. Fréquence ou intensité des feux de forêt
- **Famille** : Impact visible
- **Définition** : indicateur de fréquence, d’occurrence ou d’intensité des feux
- **Source principale** : données d’événements extrêmes / données complémentaires
- **Projection** : indirecte via climat futur et sécheresse
- **Usage dashboard** : indicateur très narratif
- **Usage citoyen** : prévention, aménagement, sécurité
- **Usage score** : principal

## Synthèse d’usage

### Indicateurs principalement projetés
- Température moyenne annuelle
- Jours > 30°C
- Jours de gel
- Précipitations annuelles
- Séquences sèches

### Indicateurs principalement contextuels / de pression
- GES transport
- GES bâtiment

### Indicateur d’impact visible
- Feux de forêt

## Logique métier
Cette sélection vise un équilibre entre :
- lisibilité pour le grand public,
- faisabilité technique en hackathon,
- cohérence territoriale pour PACA / Marseille,
- capacité à produire des recommandations citoyennes concrètes.
