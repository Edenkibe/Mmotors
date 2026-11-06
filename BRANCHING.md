# Convention de gestion des branches - Mmotors

## Branches principales

- main : version stable destinée à la production.
- develop : branche principale de développement et d'intégration.

## Branches secondaires

- feature/nom-fonctionnalite : ajout d'une fonctionnalité.
- fix/nom-correction : correction d'un bug.
- hotfix/nom-correction : correction urgente en production.
- chore/nom-tache : maintenance et configuration.

## Exemples

- feature/authentification
- feature/gestion-voitures
- fix/erreur-connexion
- hotfix/securite-paiement
- chore/configuration-render

## Règles

1. Toute nouvelle fonctionnalité part de develop.
2. Les fonctionnalités sont intégrées dans develop après validation.
3. Les versions validées sont fusionnées dans main.
4. Les corrections urgentes sont appliquées à main puis réintégrées dans develop.
5. Les noms de branches sont écrits en minuscules, sans accents, avec des tirets si nécessaire.
