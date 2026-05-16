# Dictionnaire de données
## Plateforme de gestion des mémoires de Master
### Université Joseph Ki-Zerbo | Master ILSI 2025-2026

---

## Table : `users`
> Table centrale de tous les utilisateurs de la plateforme

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique auto-généré |
| nom | VARCHAR(100) | NOT NULL | Nom de famille |
| prenom | VARCHAR(100) | NOT NULL | Prénom |
| email | VARCHAR(150) | NOT NULL, UNIQUE | Email de connexion — doit être unique |
| mot_de_passe | VARCHAR(255) | NOT NULL | Mot de passe hashé (bcrypt) — jamais en clair |
| role | VARCHAR(30) | NOT NULL | Rôle : etudiant, enseignant, superviseur, responsable, admin, jury |
| actif | BOOLEAN | DEFAULT true | Compte actif ou désactivé par l'admin |
| created_at | TIMESTAMP | DEFAULT now() | Date de création du compte |

---

## Table : `teachers`
> Profil enseignant — complète la table users pour les enseignants

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → users.id, UNIQUE | Lien vers le compte utilisateur |
| grade | VARCHAR(50) | NOT NULL | Grade académique : Assistant, Maitre_Assistant, Maitre_Conferences, Professeur |
| specialite | VARCHAR(150) | | Domaine de spécialité de l'enseignant |

> ⚠️ **Règle métier** : le superviseur d'un sujet doit avoir grade = Maitre_Conferences ou Professeur

---

## Table : `students`
> Profil étudiant — complète la table users pour les étudiants

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| user_id | UUID | FK → users.id, UNIQUE | Lien vers le compte utilisateur |
| matricule | VARCHAR(50) | NOT NULL, UNIQUE | Numéro matricule universitaire |
| promotion | VARCHAR(50) | | Promotion (ex: M1 2025-2026) |
| master | VARCHAR(100) | | Intitulé du Master (ex: ILSI) |

---

## Table : `academic_years`
> Années académiques — cadre institutionnel du système

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| libelle | VARCHAR(20) | NOT NULL | Libellé (ex: 2025-2026) |
| date_debut | DATE | NOT NULL | Date de début de l'année |
| date_fin | DATE | NOT NULL | Date de fin de l'année |
| statut | VARCHAR(20) | DEFAULT en_cours | en_cours, terminee, archivee |

---

## Table : `semesters`
> Semestres — subdivision d'une année académique

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| academic_year_id | UUID | FK → academic_years.id | Année académique parente |
| libelle | VARCHAR(50) | NOT NULL | Ex: Semestre 2 - 2025/2026 |
| date_limite_sujets | DATE | | Date limite de dépôt des sujets par les enseignants |
| date_limite_candidatures | DATE | | Date limite de candidature des étudiants |
| date_limite_documents | DATE | | Date limite de dépôt des documents finaux |
| statut | VARCHAR(20) | DEFAULT ferme | ouvert = campagne active, ferme = campagne inactive |

---

## Table : `subjects`
> Sujets de mémoire proposés par les enseignants

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| titre | VARCHAR(255) | NOT NULL | Titre du sujet |
| resume | TEXT | | Résumé et contexte du sujet |
| objectifs | TEXT | | Objectifs attendus du mémoire |
| competences_requises | TEXT | | Prérequis pour candidater |
| mots_cles | VARCHAR(255) | | Mots-clés séparés par virgule |
| encadrant_id | UUID | FK → teachers.id | Enseignant qui encadre le mémoire |
| superviseur_id | UUID | FK → teachers.id | Enseignant superviseur (grade >= Maitre_Conferences) |
| semester_id | UUID | FK → semesters.id | Semestre auquel est rattaché le sujet |
| capacite | INT | DEFAULT 1 | Nombre max d'étudiants (généralement 1) |
| statut | VARCHAR(20) | DEFAULT brouillon | brouillon, publie, complet, archive |

> ⚠️ **Règle métier** : un sujet n'est visible aux étudiants que si statut = publie

---

## Table : `applications`
> Candidatures des étudiants sur les sujets

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| student_id | UUID | FK → students.id | Étudiant candidat |
| subject_id | UUID | FK → subjects.id | Sujet visé |
| motivation | TEXT | | Lettre de motivation de l'étudiant |
| date_candidature | TIMESTAMP | DEFAULT now() | Date et heure de la candidature |
| statut | VARCHAR(20) | DEFAULT en_attente | en_attente, acceptee, refusee |

> ⚠️ **Règle métier** : UNIQUE(student_id, subject_id) — un étudiant ne candidate qu'une fois par sujet et ne peut avoir qu'une candidature acceptée par semestre

---

## Table : `memoires`
> Mémoire en cours de réalisation — créé après acceptation de la candidature

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| student_id | UUID | FK → students.id, UNIQUE | Étudiant auteur (1 seul mémoire par étudiant) |
| subject_id | UUID | FK → subjects.id, UNIQUE | Sujet du mémoire (1 sujet = 1 mémoire max) |
| date_affectation | TIMESTAMP | DEFAULT now() | Date d'affectation officielle |
| statut_avancement | VARCHAR(20) | DEFAULT en_cours | en_cours, suspendu, abandonne, finalise |
| soutenable | BOOLEAN | DEFAULT false | Mis à true par l'encadrant quand le travail est prêt |
| date_validation_soutenabilite | TIMESTAMP | NULL | Date à laquelle l'encadrant a validé la soutenabilité |

---

## Table : `milestones`
> Jalons de suivi du mémoire — étapes clés à atteindre

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| memoire_id | UUID | FK → memoires.id | Mémoire concerné |
| libelle | VARCHAR(150) | NOT NULL | Ex: Validation du plan, Dépôt final |
| echeance | DATE | | Date limite pour ce jalon |
| statut | VARCHAR(20) | DEFAULT a_faire | a_faire, en_cours, valide, depasse |

---

## Table : `documents`
> Fichiers déposés par l'étudiant au fil du mémoire

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| memoire_id | UUID | FK → memoires.id | Mémoire auquel appartient le document |
| type | VARCHAR(50) | | plan, version_intermediaire, version_finale, annexe, fiche_validation |
| nom_fichier | VARCHAR(255) | NOT NULL | Nom original du fichier uploadé |
| chemin_stockage | VARCHAR(500) | NOT NULL | Chemin du fichier sur le serveur |
| version | INT | DEFAULT 1 | Numéro de version du document |
| date_depot | TIMESTAMP | DEFAULT now() | Date et heure du dépôt |

---

## Table : `observations`
> Commentaires et retours de l'encadrant sur le mémoire

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| memoire_id | UUID | FK → memoires.id | Mémoire concerné |
| auteur_id | UUID | FK → users.id | Auteur du commentaire (encadrant) |
| contenu | TEXT | NOT NULL | Texte de l'observation |
| type_observation | VARCHAR(30) | | commentaire, recommandation, correction |
| date_observation | TIMESTAMP | DEFAULT now() | Date et heure de l'observation |

---

## Table : `defense_sessions`
> Sessions de soutenance organisées par le responsable de Master

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| libelle | VARCHAR(150) | | Ex: Session Mai 2026 |
| date_session | DATE | NOT NULL | Date de la session |
| heure_debut | TIME | NOT NULL | Heure de début |
| heure_fin | TIME | NOT NULL | Heure de fin |
| salle | VARCHAR(100) | | Salle où se tient la session |
| semester_id | UUID | FK → semesters.id | Semestre rattaché |
| statut | VARCHAR(20) | DEFAULT planifiee | planifiee, terminee, annulee |

---

## Table : `defenses`
> Soutenance individuelle d'un étudiant

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| memoire_id | UUID | FK → memoires.id, UNIQUE | Mémoire concerné (1 mémoire = 1 soutenance) |
| session_id | UUID | FK → defense_sessions.id | Session dans laquelle se tient la soutenance |
| tenue_effective | BOOLEAN | DEFAULT false | true = soutenance a bien eu lieu |
| statut | VARCHAR(20) | DEFAULT programmee | programmee, tenue, annulee |
| date_heure | TIMESTAMP | | Date et heure précise de la soutenance |

> ⚠️ **Règle métier** : une soutenance ne peut être créée que si memoires.soutenable = true

---

## Table : `juries`
> Jury associé à une soutenance

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| defense_id | UUID | FK → defenses.id, UNIQUE | Soutenance concernée (1 jury par soutenance) |

---

## Table : `jury_members`
> Membres composant un jury

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| jury_id | UUID | FK → juries.id | Jury auquel appartient le membre |
| teacher_id | UUID | FK → teachers.id | Enseignant membre du jury |
| role_dans_jury | VARCHAR(30) | NOT NULL | president, encadrant, superviseur, membre, rapporteur |

> ⚠️ **Règle métier** : UNIQUE(jury_id, teacher_id) — un enseignant ne peut pas siéger deux fois dans le même jury

---

## Table : `defense_observations`
> Observations saisies par le jury le jour de la soutenance

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| defense_id | UUID | FK → defenses.id | Soutenance concernée |
| auteur_id | UUID | FK → users.id | Membre du jury auteur |
| contenu | TEXT | NOT NULL | Texte de l'observation |
| critere | VARCHAR(50) | | qualite_scientifique, qualite_redactionnelle, presentation_orale, maitrise_sujet, recommandations |

---

## Table : `grades`
> Note finale du mémoire

| Colonne | Type | Contrainte | Description |
|---|---|---|---|
| id | UUID | PK | Identifiant unique |
| defense_id | UUID | FK → defenses.id, UNIQUE | Soutenance notée (1 note par soutenance) |
| note_document | DECIMAL(4,2) | | Note sur la qualité du document écrit |
| note_travail | DECIMAL(4,2) | | Note sur le travail réalisé |
| note_presentation | DECIMAL(4,2) | | Note sur la présentation orale |
| note_reponses | DECIMAL(4,2) | | Note sur les réponses aux questions |
| note_finale | DECIMAL(4,2) | NOT NULL, 0-20 | Note finale du mémoire |
| mention | VARCHAR(30) | | Passable, Assez_Bien, Bien, Tres_Bien, Excellent |
| commentaires | TEXT | | Commentaires généraux du jury |
| validee | BOOLEAN | DEFAULT false | true = note définitive non modifiable |
| date_saisie | TIMESTAMP | DEFAULT now() | Date de saisie de la note |

> ⚠️ **Règle métier** : la note ne peut être saisie que si defenses.tenue_effective = true

---

## Récapitulatif des relations clés

| Relation | Type | Description |
|---|---|---|
| users → teachers | 1-1 | Un user peut être un enseignant |
| users → students | 1-1 | Un user peut être un étudiant |
| academic_years → semesters | 1-N | Une année contient plusieurs semestres |
| teachers → subjects | 1-N | Un enseignant propose plusieurs sujets |
| students → applications | 1-N | Un étudiant peut candidater (1 seule acceptée) |
| subjects → applications | 1-N | Un sujet reçoit plusieurs candidatures |
| students → memoires | 1-1 | Un étudiant a au plus un mémoire |
| memoires → defenses | 1-1 | Un mémoire donne lieu à une soutenance |
| defenses → juries | 1-1 | Une soutenance a un jury |
| defenses → grades | 1-1 | Une soutenance aboutit à une note |