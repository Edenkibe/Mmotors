# Documentation fonctionnelle – Mmotors

## 1. Présentation

Ce document présente les principales fonctionnalités de l'application Mmotors.

Il a pour objectif de décrire le fonctionnement de chaque fonctionnalité, les utilisateurs concernés ainsi que les principales interactions entre les différentes parties de l'application.

Cette documentation s'adresse :
- Aux développeurs souhaitant comprendre le fonctionnement de l'application.
- Aux nouveaux membres de l'équipe.
- Aux personnes chargées de maintenir ou de faire évoluer le projet.

## 2. Gestion des utilisateurs

### 2.1 Présentation

La gestion des utilisateurs permet aux personnes d'accéder à l'application à travers un compte personnel.

Cette fonctionnalité repose sur le système d'authentification de Django, éventuellement complété par des fonctionnalités spécifiques au projet.

### 2.2 Fonctionnalités disponibles

Les fonctionnalités liées aux utilisateurs peuvent comprendre :

- La création d'un compte.
- La connexion à l'application.
- La déconnexion.
- La gestion des informations personnelles.
- La consultation des informations du compte.
- La gestion des accès selon le profil de l'utilisateur.

### 2.3 Fonctionnement

1. L'utilisateur accède à la page de connexion ou d'inscription 
2. Il renseigne les informations demandées.
3. Les données sont envoyées au serveur.
4. Django vérifie les informations.
5. Si les informations sont valides, l'utilisateur accède à son espace personnel,l'email sera envoyé sur l'adresse mail du user pour cliquer sur un lien d'activation pour que son compte soit activé

### 2.4 Éléments techniques

Les éléments techniques concernés peuvent inclure :

- Les modèles utilisateurs.
- Les vues d'authentification.
- Les formulaires.
- Les templates de connexion et d'inscription.
- Les mécanismes de gestion des sessions.

Les chemins exacts doivent être renseignés selon l'organisation du projet.

---

## 3.Location de voiture

## 3.1. Présentation

La fonctionnalité de location de voiture permet aux utilisateurs de Mmotors de consulter les véhicules proposés à la location et d'effectuer une demande de réservation.

Elle a pour objectif de faciliter la recherche d'un véhicule adapté aux besoins de l'utilisateur, en lui permettant de consulter les caractéristiques du véhicule et les informations relatives à sa location.

Cette fonctionnalité constitue l'un des services principaux de la plateforme Mmotors.

## 3.2. Objectifs de la fonctionnalité

La fonctionnalité de location de voiture vise à :

- Permettre aux utilisateurs de découvrir les véhicules disponibles à la location.

- Présenter les caractéristiques des véhicules.

- Permettre la consultation des tarifs de location.

- Faciliter le choix d'un véhicule.

- Permettre aux utilisateurs d'effectuer une demande de location.

- de rechercher les vehicule sous des criteres

- Centraliser les informations relatives aux demandes de location.

- Faciliter le suivi des demandes.

## 3.3. Acteurs concernés

Plusieurs types d'acteurs peuvent intervenir dans le processus de location.

## 3.3.1 Utilisateur

L'utilisateur peut :

- Consulter les véhicules proposés.

- Visualiser les détails d'un véhicule.

- Consulter les tarifs.

- Choisir un véhicule.

- Effectuer une demande de location.

- Consulter ses demandes de location.

## 3.3.2 Administrateur

L'administrateur peut, selon les fonctionnalités implémentées :

- Ajouter de nouveaux véhicules.

- Modifier les informations des véhicules.

- Supprimer des véhicules.

- Gérer les véhicules disponibles.

- Consulter les demandes de location.

- Gérer le traitement des demandes.

## 4 Achat de voiture

## 4.1. Présentation

La fonctionnalité d'achat de voiture permet aux utilisateurs de Mmotors de consulter les véhicules proposés à la vente sur la plateforme.

Elle a pour objectif de faciliter la recherche et l'acquisition d'un véhicule en mettant à disposition des utilisateurs un catalogue de voitures avec leurs caractéristiques, leurs photos et leurs prix.

L'utilisateur peut consulter les différentes annonces, sélectionner un véhicule qui correspond à ses besoins et effectuer une demande d'achat selon le processus prévu par la plateforme.

Cette fonctionnalité constitue un service essentiel de Mmotors en mettant en relation les personnes intéressées par l'achat de véhicules et les responsables de leur commercialisation.

## 4.2. Objectifs de la fonctionnalité

La fonctionnalité d'achat de voiture vise à :

- Présenter les véhicules disponibles à la vente.

- Permettre aux utilisateurs de rechercher un véhicule.

- Faciliter la comparaison entre plusieurs voitures.

- Afficher les caractéristiques détaillées des véhicules.

- Présenter les prix de vente.

- Permettre aux utilisateurs de manifester leur intérêt pour un véhicule.

- Enregistrer et suivre les demandes d'achat.

- Faciliter la gestion des annonces par les administrateurs.

## 4.3. Acteurs concernés

## 4.3.1 Utilisateur / Acheteur

L'utilisateur peut :

- Consulter le catalogue des voitures.

- Rechercher un véhicule selon ses critères.

- Filtrer les véhicules selon les caractéristiques disponibles.

- Consulter les détails d'une voiture.

- Visualiser les photos du véhicule.

- Consulter le prix de vente.

- Effectuer une demande d'achat ou de contact.

- Consulter l'état de ses demandes, si cette fonctionnalité est disponible.

## 4.3.2 Administrateur

L'administrateur peut, selon les fonctionnalités implémentées :

- Ajouter une nouvelle voiture au catalogue.

- Modifier les informations d'un véhicule.

- Ajouter ou modifier les photos.

- Mettre à jour le prix de vente.

- Modifier le statut de disponibilité.

- upprimer une annonce.

- Consulter les demandes d'achat.

- Traiter les demandes des utilisateurs.


## 5. Gestion des espaces utilisateurs

### 5.1 Présentation

L'espace utilisateur permet à chaque utilisateur connecté d'accéder aux informations et fonctionnalités qui lui sont destinées.

### 5.2 Fonctionnalités

Selon les fonctionnalités disponibles dans le projet, cet espace peut permettre :

- De consulter ses informations personnelles.
- D'accéder à ses différentes demandes.
- De consulter l'état de ses dossiers.
- De gérer certaines informations liées à son compte.

### 5.3 Fonctionnement

L'utilisateur doit être authentifié pour accéder à son espace personnel.

Les informations affichées doivent correspondre à son compte et respecter les règles d'autorisation définies par l'application.

### 6 Creation de publicité ou ads
cette fonctionnalité est reservé que aux admins du site, elle permet:
- de creer une publicité pour une voiture, elle sera vu par tous les utilisateurs du sites
- sur la page d'accueil pour un admin: verra l option dashboard reservé que pour l admin ->manage car -> creer une publicité pour une voiture

## 7. Navigation dans l'application

### 7.1 Présentation

La navigation permet aux utilisateurs d'accéder aux différentes rubriques de Mmotors.

Elle repose sur le système de routage Django et sur les liens définis dans les templates HTML.

### 7.2 Fonctionnement

Lorsqu'un utilisateur sélectionne un élément de navigation :

1. Le navigateur envoie une requête vers l'URL correspondante.
2. Django identifie la route.
3. La vue associée traite la requête.
4. La réponse est affichée dans le navigateur.

Les différentes pages doivent proposer une navigation cohérente et adaptée au profil de l'utilisateur.

---

## 8. Gestion des formulaires

### 8.1 Présentation

Les formulaires permettent de collecter les informations saisies par les utilisateurs.

Ils constituent un moyen d'interaction entre l'interface utilisateur et les traitements réalisés côté serveur.

### 8.2 Fonctionnement

1. L'utilisateur accède à un formulaire.
2. Il renseigne les champs demandés.
3. Il soumet le formulaire.
4. Le serveur récupère les données.
5. Les données sont validées.
6. Si elles sont correctes, le traitement demandé est exécuté.
7. Un message de confirmation ou d'erreur est présenté à l'utilisateur.

### 8.3 Sécurité et validation

Les formulaires doivent notamment :
- Vérifier la validité des données.
- Empêcher les soumissions non autorisées.
- Utiliser la protection CSRF de Django.
- Contrôler les droits d'accès avant toute modification de données.

---

## 9. Gestion des droits d'accès

### 9.1 Présentation

L'application doit contrôler l'accès aux fonctionnalités selon le profil et les autorisations de chaque utilisateur.

### 9.2 Principes

- Les pages privées doivent être accessibles uniquement aux utilisateurs autorisés.
- Les données personnelles ne doivent pas être accessibles par d'autres utilisateurs sans autorisation.
- Les opérations de modification et de suppression doivent faire l'objet d'un contrôle côté serveur.
- Les utilisateurs ne doivent pas pouvoir effectuer des actions réservées à d'autres profils.

---

## 10. Gestion des erreurs et des notifications

L'application doit informer l'utilisateur lorsque certaines opérations sont effectuées ou lorsqu'une erreur survient.

Les situations possibles comprennent :

- La validation réussie d'un formulaire.
- L'échec de validation d'une information.
- Une tentative d'accès non autorisée.
- La consultation d'une ressource inexistante.
- La suppression d'une demande.
- Une erreur lors de l'enregistrement des données.

Les messages doivent être compréhensibles et permettre à l'utilisateur de savoir quelle action entreprendre.

---

## 11. Sécurité générale de l'application

La sécurité constitue un élément essentiel du fonctionnement de Mmotors.

Les principales mesures à respecter sont :

- Utiliser le système d'authentification Django.
- Protéger les formulaires avec les jetons CSRF.
- Vérifier les permissions avant les opérations sensibles.
- Valider les données reçues par le serveur.
- Ne pas exposer les informations sensibles.
- Utiliser les méthodes HTTP adaptées aux opérations réalisées.
- Éviter de transmettre des informations confidentielles dans les URL.

---

## 12. Ajouter une nouvelle fonctionnalité

Pour développer une nouvelle fonctionnalité dans Mmotors, il est recommandé de suivre les étapes suivantes :

1. Identifier l'application Django concernée.
2. Définir le besoin fonctionnel.
3. Identifier les données nécessaires.
4. Créer ou modifier les modèles si nécessaire.
5. Développer les vues.
6. Définir les routes dans `urls.py`.
7. Créer ou modifier les templates.
8. Ajouter les formulaires nécessaires.
9. Vérifier les droits d'accès.
10. Tester le fonctionnement.
11. Mettre à jour la documentation.

---

## 13. Maintenance et évolution

Chaque nouvelle fonctionnalité ou modification importante doit être accompagnée d'une mise à jour de cette documentation.

Il est recommandé de préciser :

- Le nom de la fonctionnalité.
- Son objectif.
- Les profils utilisateurs concernés.
- Son fonctionnement.
- Les fichiers techniques concernés.
- Les règles métier associées.
- Les éventuelles dépendances avec d'autres fonctionnalités.

---

## 12. Conclusion

Les fonctionnalités de Mmotors sont organisées autour des besoins des utilisateurs et des différents traitements réalisés par l'application.

Cette documentation constitue une référence pour comprendre les fonctionnalités existantes, faciliter la maintenance du projet et accompagner les futurs développements.