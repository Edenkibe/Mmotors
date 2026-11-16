# Architecture technique du projet Mmotors

## 1. Présentation générale

Mmotors est une application web développée avec le framework Django et le langage Python.

L'application repose sur une architecture organisée en plusieurs composants permettant de séparer les responsabilités entre la gestion des données, le traitement des requêtes, la navigation et l'affichage des interfaces utilisateur.

Cette organisation facilite :
- La maintenance du code.
- L'évolution des fonctionnalités.
- La réutilisation des composants.
- Le travail collaboratif entre développeurs.
- La compréhension globale du fonctionnement de l'application.

## 2. Architecture globale du projet mmotors

le project a 8 application separés dans le different folder:
- account.
- contact.
- core
- dossiers.
- integration.
- location
- promotion
- voiture
dans chaques application vous trouvez de folder comme form[ dans le quel il y a tout le formulaire de l'application]

### 2.1 Model (Modèle)

Les modèles sont généralement définis dans le fichier `models.py`.

Ils représentent les différentes entités métier de l'application et permettent de structurer les données stockées dans la base de données.

Les modèles Django permettent notamment :
- De définir les champs des entités.
- De définir les relations entre les entités.
- D'effectuer des opérations de création, lecture, modification et suppression.
- De gérer les contraintes et les règles liées aux données.

### 2.2 View (Vue)

Les vues sont généralement définies dans le fichier `views.py`.

Elles assurent le traitement des requêtes envoyées par les utilisateurs.

Leur rôle consiste notamment à :
- Recevoir les requêtes HTTP.
- Récupérer et traiter les données.
- Appliquer les règles métier.
- Interagir avec les modèles.
- Retourner une réponse HTTP ou afficher un template.

### 2.3 Template (Interface utilisateur)

Les templates sont les fichiers HTML utilisés pour afficher les interfaces de l'application.

Ils permettent :
- D'afficher les informations récupérées depuis les vues.
- De présenter les formulaires.
- De gérer l'affichage conditionnel des éléments.
- D'utiliser les fonctionnalités du moteur de templates Django.

Les fichiers CSS, JavaScript et les images sont généralement stockés dans le dossier `static/`.

## 3. Organisation des dossiers et fichiers

Le projet Django est organisé autour d'un projet principal et de plusieurs applications.

Chaque application Django possède une responsabilité fonctionnelle précise.

Les principaux fichiers rencontrés dans une application Django sont :

| Fichier ou dossier | Description |
|---|---|
| `models.py` | Définition des modèles de données. |
| `views.py` | Traitement des requêtes et logique métier. |
| `urls.py` | Définition des routes de l'application. |
| `forms.py` | Définition et validation des formulaires. |
| `admin.py` | Configuration de l'administration Django. |
| `apps.py` | Configuration de l'application Django. |
| `tests.py` | Tests automatisés. |
| `migrations/` | Historique des évolutions de la base de données. |
| `templates/` | Fichiers HTML de l'application. |
| `static/` | Ressources CSS, JavaScript et images. |

## 4. Rôle du projet principal Django

Le projet principal est dans le folder Config qui constitue le point central de configuration de l'application.

Il contient généralement les éléments suivants :

### settings.py

Ce fichier regroupe les paramètres généraux de l'application :
- Les applications installées (`INSTALLED_APPS`).
- La configuration de la base de données (`DATABASES`).
- Les paramètres de sécurité.
- Les chemins des templates.
- La configuration des fichiers statiques.
- Les paramètres de langue et de fuseau horaire.

### urls.py

Ce fichier définit les routes principales du projet.

Il permet de connecter les URL aux différentes applications Django grâce à la fonction `include()`.

### wsgi.py et asgi.py

Ces fichiers permettent de configurer les interfaces utilisées pour déployer l'application avec des serveurs compatibles WSGI ou ASGI.

### manage.py

Ce fichier constitue le point d'entrée des commandes de gestion Django.

Il permet notamment de :
- Démarrer le serveur de développement.
- Créer les migrations.
- Appliquer les migrations.
- Créer un superutilisateur.
- Exécuter les tests.

## 5. Fonctionnement d'une requête utilisateur

Lorsqu'un utilisateur accède à une page de Mmotors, Django suit généralement le processus suivant :

1. L'utilisateur accède à une URL depuis son navigateur.
2. Django reçoit la requête HTTP.
3. Le système de routage recherche la vue correspondant à l'URL.
4. La vue exécute les traitements nécessaires.
5. La vue interagit avec les modèles si des données doivent être récupérées ou modifiées.
6. Les données sont transmises au template.
7. Le template génère le contenu HTML.
8. Django retourne la réponse au navigateur.

### Schéma simplifié du fonctionnement

```text
Utilisateur
     |
     v
Navigateur web
     |
     v
Requête HTTP
     |
     v
URLs Django
     |
     v
Views (logique métier)
     |
     v
Models
     |
     v
Base de données
     |
     v
Views
     |
     v
Templates HTML
     |
     v
Réponse HTTP
     |
     v
Navigateur web
```

## 6. Gestion de la base de données

Django utilise son ORM (Object Relational Mapper) pour communiquer avec la base de données.

L'ORM permet aux développeurs de manipuler les données à travers les modèles Python sans avoir à écrire directement des requêtes SQL pour les opérations courantes.

Les principales opérations sont :

- `objects.create()` : créer un enregistrement.
- `objects.get()` : récupérer un enregistrement.
- `objects.filter()` : filtrer des enregistrements.
- `objects.all()` : récupérer l'ensemble des enregistrements.
- `delete()` : supprimer un enregistrement.
- `save()` : enregistrer les modifications.

Les évolutions de la structure de la base de données sont gérées avec le système de migrations Django.

## 7. Gestion des formulaires

Les formulaires permettent de collecter les informations saisies par les utilisateurs.

Ils peuvent être définis dans un fichier `forms.py` ou directement dans les vues lorsque le projet utilise cette organisation.

Django permet notamment :
- De récupérer les données envoyées par les utilisateurs.
- De vérifier leur validité.
- De gérer les erreurs de saisie.
- De protéger les formulaires contre les attaques CSRF avec les mécanismes intégrés.

## 8. Gestion de l'authentification et des autorisations

Django fournit un système d'authentification intégré permettant de gérer les utilisateurs.

Il permet notamment :
- La connexion et la déconnexion.
- La gestion des comptes utilisateurs.
- La gestion des mots de passe.
- La restriction d'accès à certaines vues.
- La gestion des permissions.

Les vues nécessitant une authentification doivent utiliser les mécanismes de protection adaptés, par exemple `login_required`.

Les droits d'accès doivent également être vérifiés côté serveur.

## 9. Gestion des fichiers statiques

Les ressources statiques permettent de gérer la présentation et les interactions côté navigateur.

Elles peuvent comprendre :
- Les feuilles de style CSS.
- Les fichiers JavaScript.
- Les images.
- Les icônes.

Django utilise notamment les paramètres `STATIC_URL` et `STATICFILES_DIRS` pour gérer ces ressources.

En environnement de production, la collecte des fichiers statiques peut être réalisée avec :

```bash
python manage.py collectstatic
```

## 10. Bonnes pratiques de développement

Afin de conserver une architecture claire et facile à maintenir, les recommandations suivantes doivent être respectées :

- Respecter la séparation des responsabilités entre modèles, vues et templates.
- Éviter de placer toute la logique métier dans les templates.
- Utiliser des noms de fonctions et de variables explicites.
- Réutiliser les composants existants lorsque cela est possible.
- Utiliser les formulaires Django pour valider les données utilisateur.
- Protéger les vues selon les droits d'accès nécessaires.
- Créer les migrations après chaque modification des modèles.
- Ajouter des tests pour les nouvelles fonctionnalités.
- Éviter de stocker les informations sensibles directement dans le code source.

## 11. Évolution de l'architecture

Lorsqu'une nouvelle fonctionnalité est ajoutée, il est recommandé de suivre les étapes suivantes :

1. Identifier l'application Django concernée.
2. Déterminer si de nouveaux modèles sont nécessaires.
3. Ajouter ou modifier les vues.
4. Définir les nouvelles routes dans `urls.py`.
5. Créer ou modifier les templates.
6. Ajouter les éventuels fichiers CSS et JavaScript.
7. Effectuer les migrations si les modèles ont été modifiés.
8. Tester le fonctionnement de la fonctionnalité.
9. Mettre à jour la documentation technique.

## 12. Conclusion

L'architecture de Mmotors repose sur les principes d'organisation du framework Django et sur la séparation des responsabilités entre les données, la logique métier et l'interface utilisateur.

Cette organisation permet aux développeurs de comprendre plus facilement le fonctionnement de l'application, de maintenir le code existant et d'ajouter de nouvelles fonctionnalités de manière structurée.