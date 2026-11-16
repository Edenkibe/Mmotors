# Guide d'installation du projet Mmotors

## 1. Présentation

Ce document décrit les étapes nécessaires pour installer, configurer et exécuter le projet **Mmotors** sur un nouvel environnement de développement.

Il s'adresse aux développeurs qui souhaitent récupérer le code source du projet, installer ses dépendances et commencer à travailler sur l'application.

## 2. Prérequis

Avant de commencer l'installation, assurez-vous de disposer des outils suivants :

- **Python** : langage utilisé pour le développement de l'application.
- **Git** : outil de gestion de versions.
- **Visual Studio Code** (recommandé) : éditeur de code.
- **pip** : gestionnaire de paquets Python.

Vérifier les installations :

```bash
python --version
git --version
pip --version
```

## 3. Récupération du projet

Ouvrir un terminal et exécuter la commande suivante pour récupérer le dépôt GitHub :

```bash
git clone https://github.com/Edenkibe/Mmotors.git
```

Accéder ensuite au dossier du projet :

```bash
cd Mmotors
```

## 4. Création de l'environnement virtuel

Il est recommandé d'utiliser un environnement virtuel afin d'isoler les dépendances du projet des autres installations Python présentes sur la machine.

Créer l'environnement virtuel :

```bash
python -m venv env 
```

### Activation sous Windows (PowerShell)

```powershell
.\env\Scripts\Activate
```

### Activation sous Linux ou macOS

```bash
source env/bin/activate
```

Une fois activé, le nom de l'environnement `(env)` apparaît généralement au début de la ligne de commande.

## 5. Installation des dépendances

Le fichier `requirements.txt` contient les bibliothèques Python nécessaires au fonctionnement du projet.

Installer les dépendances avec :

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 6. Configuration de l'application

Avant de démarrer l'application, vérifier les paramètres du projet dans le fichier `settings.py`. a l'interieur du fichier config

Les éléments à vérifier sont notamment :

- La configuration de la base de données.
- La variable `SECRET_KEY`.
- Le paramètre `DEBUG`.
- Les paramètres `ALLOWED_HOSTS`.
- Les éventuelles variables d'environnement nécessaires.

**Important :** les informations sensibles, notamment les clés secrètes et les identifiants de base de données, ne doivent pas être publiées sur GitHub.

Si le projet utilise un fichier `.env`, demander les valeurs de configuration nécessaires au responsable du projet. Ne jamais utiliser les identifiants de production dans un environnement local.

## 7. Initialisation de la base de données

Après avoir configuré la base de données, exécuter les migrations Django :

```bash
python manage.py migrate
```

Cette commande permet de créer ou de mettre à jour les tables de la base de données selon les migrations disponibles.

Si des fichiers de migration doivent être générés après une modification des modèles, utiliser :

```bash
python manage.py makemigrations
python manage.py migrate
```

## 8. Création d'un compte administrateur

Pour accéder à l'interface d'administration Django, créer un superutilisateur :

```bash
python manage.py createsuperuser
```

Suivre les instructions affichées dans le terminal pour renseigner le nom d'utilisateur, l'adresse e-mail et le mot de passe.

## 9. Lancement du serveur de développement

Une fois toutes les étapes précédentes terminées, démarrer le serveur Django :

```bash
python manage.py runserver
```

Par défaut, l'application est accessible à l'adresse suivante :

http://127.0.0.1:8000/

L'interface d'administration Django est accessible à :

http://127.0.0.1:8000/admin/

Pour arrêter le serveur, utiliser `CTRL + C` dans le terminal.

## 10. Récupération des dernières modifications

Pour récupérer les dernières modifications du projet depuis GitHub :

```bash
git switch develop
git pull origin develop
```

Avant de commencer une nouvelle fonctionnalité, créer une branche dédiée :

```bash
git switch -c feature/nom-de-la-fonctionnalite
```

## 11. Résolution des problèmes fréquents

### Problème : Python n'est pas reconnu

Vérifier que Python est correctement installé et ajouté à la variable d'environnement PATH.

### Problème : L'environnement virtuel ne s'active pas sous PowerShell

Si PowerShell bloque l'exécution des scripts, ouvrir une session PowerShell et exécuter :

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Puis réessayer :

```powershell
.\env\Scripts\Activate.ps1
```

### Problème : ModuleNotFoundError

Vérifier que l'environnement virtuel est activé, puis réinstaller les dépendances :

```bash
pip install -r requirements.txt
```

### Problème : Erreur de connexion à la base de données

Vérifier les paramètres de connexion dans la configuration Django et s'assurer que le serveur de base de données est démarré, si le projet utilise un serveur externe.

## 12. Fin de l'installation

L'installation est terminée lorsque :

- Les dépendances sont installées.
- La base de données est correctement initialisée.
- Le serveur Django démarre sans erreur.
- L'application est accessible depuis le navigateur.

Le développeur peut alors commencer à explorer le code source et à contribuer au projet Mmotors.

---

**Projet :** Mmotors  
**Dépôt GitHub :** https://github.com/Edenkibe/Mmotors  
**Documentation :** Dossier `docs/`