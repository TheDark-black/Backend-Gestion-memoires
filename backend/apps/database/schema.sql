-- ============================================
-- PLATEFORME GESTION MEMOIRES - schema.sql
-- Université Joseph Ki-Zerbo | Master ILSI
-- ============================================

-- Extensions utiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 1. USERS
-- ============================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL CHECK (role IN (
        'etudiant','enseignant','superviseur',
        'responsable','admin','jury'
    )),
    actif BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT now()
);

-- ============================================
-- 2. TEACHERS
-- ============================================
CREATE TABLE teachers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    grade VARCHAR(50) NOT NULL CHECK (grade IN (
        'Assistant',
        'Maitre_Assistant',
        'Maitre_Conferences',
        'Professeur'
    )),
    specialite VARCHAR(150)
);

-- ============================================
-- 3. STUDENTS
-- ============================================
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    matricule VARCHAR(50) NOT NULL UNIQUE,
    promotion VARCHAR(50),
    master VARCHAR(100)
);

-- ============================================
-- 4. ACADEMIC_YEARS
-- ============================================
CREATE TABLE academic_years (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    libelle VARCHAR(20) NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE NOT NULL,
    statut VARCHAR(20) DEFAULT 'en_cours' CHECK (statut IN (
        'en_cours','terminee','archivee'
    ))
);

-- ============================================
-- 5. SEMESTERS
-- ============================================
CREATE TABLE semesters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    academic_year_id UUID NOT NULL REFERENCES academic_years(id),
    libelle VARCHAR(50) NOT NULL,
    date_limite_sujets DATE,
    date_limite_candidatures DATE,
    date_limite_documents DATE,
    statut VARCHAR(20) DEFAULT 'ferme' CHECK (statut IN ('ouvert','ferme'))
);

-- ============================================
-- 6. SUBJECTS
-- ============================================
CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titre VARCHAR(255) NOT NULL,
    resume TEXT,
    objectifs TEXT,
    competences_requises TEXT,
    mots_cles VARCHAR(255),
    encadrant_id UUID NOT NULL REFERENCES teachers(id),
    superviseur_id UUID NOT NULL REFERENCES teachers(id),
    semester_id UUID NOT NULL REFERENCES semesters(id),
    capacite INT DEFAULT 1,
    statut VARCHAR(20) DEFAULT 'brouillon' CHECK (statut IN (
        'brouillon','publie','complet','archive'
    ))
);

-- ============================================
-- 7. APPLICATIONS
-- ============================================
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id),
    subject_id UUID NOT NULL REFERENCES subjects(id),
    motivation TEXT,
    date_candidature TIMESTAMP DEFAULT now(),
    statut VARCHAR(20) DEFAULT 'en_attente' CHECK (statut IN (
        'en_attente','acceptee','refusee'
    )),
    -- UN étudiant = UN seul sujet par semestre
    UNIQUE(student_id, subject_id)
);

-- ============================================
-- 8. MEMOIRES
-- ============================================
CREATE TABLE memoires (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL UNIQUE REFERENCES students(id),
    subject_id UUID NOT NULL UNIQUE REFERENCES subjects(id),
    date_affectation TIMESTAMP DEFAULT now(),
    statut_avancement VARCHAR(20) DEFAULT 'en_cours' CHECK (statut_avancement IN (
        'en_cours','suspendu','abandonne','finalise'
    )),
    soutenable BOOLEAN DEFAULT false,
    date_validation_soutenabilite TIMESTAMP
);

-- ============================================
-- 9. MILESTONES (jalons)
-- ============================================
CREATE TABLE milestones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memoire_id UUID NOT NULL REFERENCES memoires(id) ON DELETE CASCADE,
    libelle VARCHAR(150) NOT NULL,
    echeance DATE,
    statut VARCHAR(20) DEFAULT 'a_faire' CHECK (statut IN (
        'a_faire','en_cours','valide','depasse'
    ))
);

-- ============================================
-- 10. DOCUMENTS
-- ============================================
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memoire_id UUID NOT NULL REFERENCES memoires(id) ON DELETE CASCADE,
    type VARCHAR(50) CHECK (type IN (
        'plan','version_intermediaire',
        'version_finale','annexe','fiche_validation'
    )),
    nom_fichier VARCHAR(255) NOT NULL,
    chemin_stockage VARCHAR(500) NOT NULL,
    version INT DEFAULT 1,
    date_depot TIMESTAMP DEFAULT now()
);

-- ============================================
-- 11. OBSERVATIONS (encadrant → mémoire)
-- ============================================
CREATE TABLE observations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memoire_id UUID NOT NULL REFERENCES memoires(id) ON DELETE CASCADE,
    auteur_id UUID NOT NULL REFERENCES users(id),
    contenu TEXT NOT NULL,
    type_observation VARCHAR(30) CHECK (type_observation IN (
        'commentaire','recommandation','correction'
    )),
    date_observation TIMESTAMP DEFAULT now()
);

-- ============================================
-- 12. DEFENSE_SESSIONS
-- ============================================
CREATE TABLE defense_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    libelle VARCHAR(150),
    date_session DATE NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    salle VARCHAR(100),
    semester_id UUID NOT NULL REFERENCES semesters(id),
    statut VARCHAR(20) DEFAULT 'planifiee' CHECK (statut IN (
        'planifiee','terminee','annulee'
    ))
);

-- ============================================
-- 13. DEFENSES
-- ============================================
CREATE TABLE defenses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memoire_id UUID NOT NULL UNIQUE REFERENCES memoires(id),
    session_id UUID NOT NULL REFERENCES defense_sessions(id),
    tenue_effective BOOLEAN DEFAULT false,
    statut VARCHAR(20) DEFAULT 'programmee' CHECK (statut IN (
        'programmee','tenue','annulee'
    )),
    date_heure TIMESTAMP
);

-- ============================================
-- 14. JURIES
-- ============================================
CREATE TABLE juries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    defense_id UUID NOT NULL UNIQUE REFERENCES defenses(id)
);

-- ============================================
-- 15. JURY_MEMBERS
-- ============================================
CREATE TABLE jury_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    jury_id UUID NOT NULL REFERENCES juries(id) ON DELETE CASCADE,
    teacher_id UUID NOT NULL REFERENCES teachers(id),
    role_dans_jury VARCHAR(30) NOT NULL CHECK (role_dans_jury IN (
        'president','encadrant','superviseur','membre','rapporteur'
    )),
    UNIQUE(jury_id, teacher_id)
);

-- ============================================
-- 16. DEFENSE_OBSERVATIONS
-- ============================================
CREATE TABLE defense_observations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    defense_id UUID NOT NULL REFERENCES defenses(id) ON DELETE CASCADE,
    auteur_id UUID NOT NULL REFERENCES users(id),
    contenu TEXT NOT NULL,
    critere VARCHAR(50) CHECK (critere IN (
        'qualite_scientifique','qualite_redactionnelle',
        'presentation_orale','maitrise_sujet','recommandations'
    ))
);

-- ============================================
-- 17. GRADES
-- ============================================
CREATE TABLE grades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    defense_id UUID NOT NULL UNIQUE REFERENCES defenses(id),
    note_document DECIMAL(4,2),
    note_travail DECIMAL(4,2),
    note_presentation DECIMAL(4,2),
    note_reponses DECIMAL(4,2),
    note_finale DECIMAL(4,2) NOT NULL CHECK (note_finale >= 0 AND note_finale <= 20),
    mention VARCHAR(30) CHECK (mention IN (
        'Passable','Assez_Bien','Bien','Tres_Bien','Excellent'
    )),
    commentaires TEXT,
    validee BOOLEAN DEFAULT false,
    date_saisie TIMESTAMP DEFAULT now()
);


-- Indexes utiles
CREATE INDEX idx_subjects_semester ON subjects(semester_id);
CREATE INDEX idx_subjects_statut ON subjects(statut);
CREATE INDEX idx_applications_student ON applications(student_id);
CREATE INDEX idx_memoires_student ON memoires(student_id);
CREATE INDEX idx_documents_memoire ON documents(memoire_id);
CREATE INDEX idx_observations_memoire ON observations(memoire_id);