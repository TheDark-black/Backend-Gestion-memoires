-- ============================================
-- SEEDS - Données de test
-- Université Joseph Ki-Zerbo | Master ILSI
-- ============================================

-- ATTENTION : exécuter après schema.sql

-- ============================================
-- 1. USERS (mot de passe = "password123" hashé)
-- ============================================
INSERT INTO users (id, nom, prenom, email, mot_de_passe, role) VALUES
('a0000001-0000-0000-0000-000000000001', 'ADMIN', 'Système', 'admin@ujkz.bf', '$2b$10$YourHashedPasswordHere', 'admin'),
('a0000001-0000-0000-0000-000000000002', 'SOMDA', 'Flavien', 'flavien.somda@ujkz.bf', '$2b$10$YourHashedPasswordHere', 'enseignant'),
('a0000001-0000-0000-0000-000000000003', 'OUEDRAOGO', 'Issouf', 'issouf.ouedraogo@ujkz.bf', '$2b$10$YourHashedPasswordHere', 'superviseur'),
('a0000001-0000-0000-0000-000000000004', 'KABORE', 'Adama', 'adama.kabore@ujkz.bf', '$2b$10$YourHashedPasswordHere', 'responsable'),
('a0000001-0000-0000-0000-000000000005', 'TRAORE', 'Fatima', 'fatima.traore@ujkz.bf', '$2b$10$YourHashedPasswordHere', 'etudiant'),
('a0000001-0000-0000-0000-000000000006', 'ZONGO', 'Bila', 'bila.zongo@ujkz.bf', '$2b$10$YourHashedPasswordHere', 'etudiant'),
('a0000001-0000-0000-0000-000000000007', 'SAWADOGO', 'Marc', 'marc.sawadogo@ujkz.bf', '$2b$10$YourHashedPasswordHere', 'etudiant');

-- ============================================
-- 2. TEACHERS
-- ============================================
INSERT INTO teachers (id, user_id, grade, specialite) VALUES
('b0000001-0000-0000-0000-000000000001', 'a0000001-0000-0000-0000-000000000002', 'Maitre_Assistant', 'Génie Logiciel'),
('b0000001-0000-0000-0000-000000000002', 'a0000001-0000-0000-0000-000000000003', 'Maitre_Conferences', 'Base de Données'),
('b0000001-0000-0000-0000-000000000003', 'a0000001-0000-0000-0000-000000000004', 'Professeur', 'Réseaux');

-- ============================================
-- 3. STUDENTS
-- ============================================
INSERT INTO students (id, user_id, matricule, promotion, master) VALUES
('c0000001-0000-0000-0000-000000000001', 'a0000001-0000-0000-0000-000000000005', 'UJKZ2025001', 'M1 2025-2026', 'ILSI'),
('c0000001-0000-0000-0000-000000000002', 'a0000001-0000-0000-0000-000000000006', 'UJKZ2025002', 'M1 2025-2026', 'ILSI'),
('c0000001-0000-0000-0000-000000000003', 'a0000001-0000-0000-0000-000000000007', 'UJKZ2025003', 'M1 2025-2026', 'ILSI');

-- ============================================
-- 4. ACADEMIC YEAR
-- ============================================
INSERT INTO academic_years (id, libelle, date_debut, date_fin, statut) VALUES
('d0000001-0000-0000-0000-000000000001', '2025-2026', '2025-10-01', '2026-07-31', 'en_cours');

-- ============================================
-- 5. SEMESTER
-- ============================================
INSERT INTO semesters (id, academic_year_id, libelle, date_limite_sujets, date_limite_candidatures, date_limite_documents, statut) VALUES
('e0000001-0000-0000-0000-000000000001', 'd0000001-0000-0000-0000-000000000001', 'Semestre 2 - 2025/2026', '2026-01-15', '2026-02-01', '2026-04-30', 'ouvert');

-- ============================================
-- 6. SUBJECTS
-- ============================================
INSERT INTO subjects (id, titre, resume, objectifs, mots_cles, encadrant_id, superviseur_id, semester_id, capacite, statut) VALUES
('f0000001-0000-0000-0000-000000000001',
 'Plateforme de gestion des mémoires de Master',
 'Conception et développement d une application web REST pour gérer le cycle de vie des mémoires.',
 'Mettre en oeuvre une architecture REST complète avec gestion des rôles.',
 'REST,API,PostgreSQL,Node.js',
 'b0000001-0000-0000-0000-000000000001',
 'b0000001-0000-0000-0000-000000000002',
 'e0000001-0000-0000-0000-000000000001',
 1, 'publie'),

('f0000001-0000-0000-0000-000000000002',
 'Système de détection d intrusion par Machine Learning',
 'Application de techniques ML pour détecter les intrusions réseau en temps réel.',
 'Implémenter et évaluer des modèles de classification pour la cybersécurité.',
 'Machine Learning,Sécurité,Python,Réseau',
 'b0000001-0000-0000-0000-000000000001',
 'b0000001-0000-0000-0000-000000000002',
 'e0000001-0000-0000-0000-000000000001',
 1, 'publie'),

('f0000001-0000-0000-0000-000000000003',
 'Application mobile de suivi agricole au Burkina Faso',
 'Développement d une app mobile pour aider les agriculteurs à suivre leurs cultures.',
 'Concevoir une solution mobile adaptée au contexte local avec fonctionnement hors ligne.',
 'Mobile,React Native,Agriculture,Offline',
 'b0000001-0000-0000-0000-000000000001',
 'b0000001-0000-0000-0000-000000000002',
 'e0000001-0000-0000-0000-000000000001',
 1, 'publie');
-- ============================================
-- 7. APPLICATIONS
-- ============================================
INSERT INTO applications (id, student_id, subject_id, motivation, statut) VALUES
('a1000001-0000-0000-0000-000000000001',
 'c0000001-0000-0000-0000-000000000001',
 'f0000001-0000-0000-0000-000000000001',
 'Je suis passionné par le développement web et les architectures REST.',
 'acceptee'),

('a1000001-0000-0000-0000-000000000002',
 'c0000001-0000-0000-0000-000000000002',
 'f0000001-0000-0000-0000-000000000002',
 'La cybersécurité est mon domaine de prédilection.',
 'acceptee'),

('a1000001-0000-0000-0000-000000000003',
 'c0000001-0000-0000-0000-000000000003',
 'f0000001-0000-0000-0000-000000000003',
 'Je veux contribuer au développement numérique agricole.',
 'en_attente');

-- ============================================
-- 8. MEMOIRES
-- ============================================
INSERT INTO memoires (id, student_id, subject_id, statut_avancement, soutenable) VALUES
('b1000001-0000-0000-0000-000000000001',
 'c0000001-0000-0000-0000-000000000001',
 'f0000001-0000-0000-0000-000000000001',
 'en_cours', false),

('b1000001-0000-0000-0000-000000000002',
 'c0000001-0000-0000-0000-000000000002',
 'f0000001-0000-0000-0000-000000000002',
 'en_cours', false);

-- ============================================
-- 9. MILESTONES
-- ============================================
INSERT INTO milestones (memoire_id, libelle, echeance, statut) VALUES
('b1000001-0000-0000-0000-000000000001', 'Validation du plan', '2026-02-15', 'valide'),
('b1000001-0000-0000-0000-000000000001', 'Remise version intermédiaire', '2026-03-15', 'en_cours'),
('b1000001-0000-0000-0000-000000000001', 'Dépôt mémoire final', '2026-04-30', 'a_faire'),
('b1000001-0000-0000-0000-000000000002', 'Validation du plan', '2026-02-15', 'en_cours'),
('b1000001-0000-0000-0000-000000000002', 'Remise version intermédiaire', '2026-03-15', 'a_faire');