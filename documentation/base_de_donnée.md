# Documentation de la base de données – Mmotors

## 1. Présentation générale

La base de données de Mmotors permet de stocker, organiser et gérer les informations nécessaires au fonctionnement de l'application.

Elle centralise les données relatives aux Utilisateur, voiture_photo, voiture, payement_location, promotion, dossier_location, dossier_achat et contact

L'application utilise le système ORM (Object Relational Mapper) de Django pour communiquer avec la base de données.

L'ORM permet aux développeurs de manipuler les données à travers des modèles Python sans avoir à écrire directement des requêtes SQL pour les opérations courantes.

## 2. Organisation de la base de données

La structure de la base de données repose sur les modèles Django définis dans les fichiers `models.py` des différentes applications.

Chaque modèle représente généralement une table dans la base de données.

Les modèles définissent :
- Les champs et les types de données.
- Les relations entre les différentes entités.
- Les contraintes d'intégrité.
- Les règles de validation.
- Les comportements associés aux données.

Les principales entités métier de Mmotors peuvent être organisées autour des éléments suivants :

- Utilisateur, 
- voiture_photo, 
- voiture, 
- payement_location,
- promotion, 
- dossier_location, 
- dossier_achat
- contact

La liste définitive doit correspondre aux modèles réellement présents dans le projet.

## 3. Gestion des utilisateurs

### 3.1 Présentation

La gestion des utilisateurs repose sur le système d'authentification Django ou sur un modèle utilisateur personnalisé, selon la configuration du projet.

Les informations des utilisateurs permettent de gérer leur identité et leurs interactions avec l'application.

### 3.2 Informations possibles pour cree la table  user

  CREATE TABLE accounts_user (
  id bigint NOT NULL AUTO_INCREMENT,
  password varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  last_login datetime(6) DEFAULT NULL,
  is_superuser tinyint(1) NOT NULL,
  first_name varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  last_name varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  date_joined datetime(6) NOT NULL,
  email varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  username varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  is_active tinyint(1) NOT NULL,
  is_staff tinyint(1) NOT NULL,
  role varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email),
  UNIQUE KEY username (username)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


Les champs exacts dépendent du modèle utilisateur configuré dans Django.

## 4. Gestion des véhicules

### 4.1 Présentation

Les véhicules constituent une entité centrale de Mmotors.

Ils représentent les voitures proposées aux utilisateurs pour la location ou l'achat.

### 4.2 Informations possibles pour la creation du table 

CREATE TABLE voiture_voiture (
  id bigint NOT NULL AUTO_INCREMENT,
  marque varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  modele varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  annee int NOT NULL,
  prix decimal(10,2) NOT NULL,
  description longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  type varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  date_added datetime(6) NOT NULL,
  boite varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  carburant varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  etat varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  kilometre int unsigned NOT NULL,
  disponibilite varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT voiture_voiture_chk_1 CHECK ((kilometre >= 0))
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

## 5. Gestion des voiture_photo

### 5.1 Présentation

Ici on peut creer la photo de chaque voiture enregistrer dans la base de donnée

### 5.2 Informations possibles

CREATE TABLE voiture_photo (
  id bigint NOT NULL AUTO_INCREMENT,
  image varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  date_added datetime(6) NOT NULL,
  voiture_id bigint NOT NULL,
  is_main tinyint(1) NOT NULL,
  PRIMARY KEY (id),
  KEY voiture_photo_voiture_id_70b07a34 (voiture_id)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


La disponibilité du véhicule doit être vérifiée pour la période demandée afin d'éviter les conflits de réservation.

## 6. Gestion des promotions ads

### 6.1 Présentation

cette table nous permet a la creation des ads ou publicité
Elles facilitent le suivi des demandes et leur traitement par les personnes autorisées.

### 6.2 Informations possibles pour creer cette table de promotion

CREATE TABLE promotion_promotion (
  id bigint NOT NULL AUTO_INCREMENT,
  titre varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  description longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  disponibilite varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  created_at datetime(6) NOT NULL,
  promotion_done_at datetime(6) DEFAULT NULL,
  start_date datetime(6) DEFAULT NULL,
  end_date datetime(6) DEFAULT NULL,
  creator_id bigint DEFAULT NULL,
  voiture_id bigint NOT NULL,
  PRIMARY KEY (id),
  KEY promotion_promotion_creator_id_aa53f7b1 (creator_id),
  KEY promotion_promotion_voiture_id_d397dbb3 (voiture_id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

## 7. Gestion des payement de location

### 7.1 Présentation

permet de creer ou d'enregistrer le payement pour la location du voiture 

### 7.2 Informations possibles pour la creation du table de payement location

CREATE TABLE location_payementlocation (
  id bigint NOT NULL AUTO_INCREMENT,
  stripe_session_id varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  stripe_customer_id varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  paid tinyint(1) NOT NULL,
  created_at datetime(6) NOT NULL,
  location_id bigint NOT NULL,
  paid_amount decimal(10,2) DEFAULT NULL,
  paid_currency varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  stripe_payment_intent varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (id),
  KEY location_payementlocation_location_id_f46a03ff (location_id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


## 8. gestion sur le depot de demande de location

Permet de sauvegarder les demandes sur la location du vehicule
## 8.1 la creation de la table du demande de location

CREATE TABLE location_dossierlocation (
  id bigint NOT NULL AUTO_INCREMENT,
  nom_complet varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  telephone varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  email varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  adresse varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  numero_permis varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  pays_delivrance_permis varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  date_creation datetime(6) NOT NULL,
  date_depart datetime(6) NOT NULL,
  date_retour datetime(6) NOT NULL,
  lieu_depart varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  lieu_retour varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  code_location varchar(12) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  status varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  yousign_request_id varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  yousign_document_id varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  signed_contract_pdf varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  contrat_pdf varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  client_id bigint NOT NULL,
  vehicule_id bigint NOT NULL,
  deal varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  facture_pdf varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  message longtext COLLATE utf8mb4_unicode_ci,
  mysignature varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY code_location (code_location),
  KEY location_dossierlocation_client_id_63e71e70 (client_id),
  KEY location_dossierlocation_vehicule_id_c30a9968 (vehicule_id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

## 9. gestion sur le depot de demande sur l achat de vehicule

Permet de sauvegarder les demandes sur les achats du vehicule
## 9.1 la creation de la table du demande de vente du vehicule

CREATE TABLE dossiers_dossierachat (
  id bigint NOT NULL AUTO_INCREMENT,
  nom_complet varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  telephone varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  email varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  adresse longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  piece_identite varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  date_creation datetime(6) NOT NULL,
  client_id bigint NOT NULL,
  vehicule_id bigint NOT NULL,
  verification varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  mysignature varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  contrat_pdf varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  yousign_request_id varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  signed_contract_pdf varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  yousign_document_id varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  deal varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  paid_amount decimal(10,2) DEFAULT NULL,
  paid_at datetime(6) DEFAULT NULL,
  paid_currency varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  stripe_customer_id varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  stripe_payment_intent varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  stripe_session_id varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  facture_pdf varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  code_dossier varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  message longtext COLLATE utf8mb4_unicode_ci,
  read varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY code_dossier (code_dossier),
  KEY dossiers_dossierachat_client_id_a369ab8a (client_id),
  KEY dossiers_dossierachat_vehicule_id_5fd492c3 (vehicule_id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


## 10. gestion sur le contact ou message ou courier du site 

Permet de sauvegarder les demandes sur les achats du vehicule
## 10.1 la creation de la table du contact

CREATE TABLE contact_contactdossier (
  id bigint NOT NULL AUTO_INCREMENT,
  nom varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  email varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  code_dossier varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  message longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  created_at datetime(6) NOT NULL,
  type varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


## 10. Gestion des migrations

Django utilise un système de migrations pour suivre les évolutions de la structure de la base de données.

Lorsqu'un développeur modifie un modèle, il doit générer une migration.

### Créer les migrations

```bash
python manage.py makemigrations
```

### Appliquer les migrations

```bash
python manage.py migrate
```

### Consulter l'état des migrations

```bash
python manage.py showmigrations
```

### Afficher le SQL d'une migration

```bash
python manage.py sqlmigrate nom_application numero_migration
```

Les migrations doivent être versionnées avec Git afin que les autres développeurs puissent appliquer les mêmes évolutions de base de données.

## 11. Manipulation des données avec l'ORM Django

Django fournit plusieurs méthodes pour manipuler les données.

### Créer un enregistrement

```python
objet = MonModele.objects.create(champ="valeur")
```

### Récupérer tous les enregistrements

```python
objets = MonModele.objects.all()
```

### Rechercher un enregistrement

```python
objet = MonModele.objects.get(id=1)
```

### Filtrer les enregistrements

```python
objets = MonModele.objects.filter(statut="en_attente")
```

### Modifier un enregistrement

```python
objet.champ = "nouvelle valeur"
objet.save()
```

### Supprimer un enregistrement

```python
objet.delete()
```

Ces exemples sont génériques et doivent être adaptés aux modèles réels du projet.

## 12. Contraintes et intégrité des données

La cohérence des informations stockées doit être assurée par plusieurs mécanismes.

Les bonnes pratiques à respecter sont :

- Utiliser des clés primaires pour identifier chaque enregistrement.
- Définir correctement les relations entre les modèles.
- Utiliser les champs obligatoires lorsque cela est nécessaire.
- Vérifier les données avant leur enregistrement.
- Éviter les doublons lorsque les règles métier l'interdisent.
- Définir les comportements de suppression avec `on_delete`.
- Utiliser des contraintes de base de données lorsque cela est pertinent.

## 13. Sécurité et protection des données

La base de données peut contenir des informations personnelles et confidentielles.

Il est donc nécessaire de respecter les principes suivants :

- Ne jamais enregistrer les mots de passe en clair.
- Ne pas publier les identifiants de connexion à la base de données.
- Protéger les informations personnelles des utilisateurs.
- Limiter les accès aux données selon les permissions.
- Ne pas exposer les données sensibles dans les réponses HTTP.
- Utiliser des sauvegardes régulières.
- Ne pas versionner les fichiers contenant des secrets.

## 14. Sauvegarde et restauration

La sauvegarde de la base de données est importante pour prévenir les pertes de données.

Les procédures de sauvegarde et de restauration doivent être adaptées au moteur de base de données utilisé par le projet.

Pour une base SQLite, il est possible de sauvegarder le fichier de base de données après avoir pris les précautions nécessaires pour garantir la cohérence de la copie.

Pour PostgreSQL ou MySQL, il est préférable d'utiliser les outils de sauvegarde propres au moteur concerné.

Les sauvegardes doivent être conservées dans un emplacement sécurisé et ne doivent pas être publiées dans le dépôt Git.

## 15. Bonnes pratiques pour les développeurs

Lorsqu'un développeur intervient sur la base de données, il doit :

1. Consulter les modèles existants avant de créer de nouvelles entités.
2. Vérifier les relations entre les modèles.
3. Éviter de dupliquer des informations inutilement.
4. Générer les migrations après les modifications.
5. Tester les migrations avant de les intégrer.
6. Ne pas supprimer une colonne ou une table sans vérifier ses dépendances.
7. Mettre à jour cette documentation après toute évolution importante.

## 16. Conclusion

La base de données constitue un élément essentiel de l'application Mmotors.

Elle permet de centraliser les informations nécessaires à la gestion des utilisateurs, des véhicules, des demandes de location, des demandes d'achat et des autres fonctionnalités de la plateforme.

La compréhension de sa structure et de ses relations est indispensable pour maintenir l'application et développer de nouvelles fonctionnalités de manière cohérente.