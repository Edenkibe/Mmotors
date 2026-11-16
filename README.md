
# Mon Repository

## Description
Repository Git public contenant le projet.

## Branches

- main : branche principale contenant les versions stables.
- develop : branche utilisée pour le développement et l'intégration des fonctionnalités.
- feature/demande-location: une nouvelle fonctionalité sur la demande
- feature/display-choix-lieu-template: ajout de la fonctionalité sur delete demande 

## Convention de nommage des branches

Les branches doivent respecter les conventions suivantes :

| Type | Convention | Exemple |
|---|---|---|
| Fonctionnalité | feature/nom | feature/login |
| Correction | bugfix/nom | bugfix/header |
| Correction urgente | hotfix/nom | hotfix/security |
| Release | release/version | release/1.0.0 |

## Workflow Git

1. Les développeurs créent leurs branches à partir de develop.
2. Les fonctionnalités sont développées dans les branches feature.
3. Les corrections sont développées dans les branches bugfix.
4. Les modifications sont fusionnées dans develop.
5. Les versions stables sont fusionnées dans main.
