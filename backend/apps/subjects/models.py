import uuid
from django.db import models

class Subject(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
        ('complet', 'Complet'),
        ('archive', 'Archivé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre = models.CharField(max_length=255)
    resume = models.TextField(null=True, blank=True)
    objectifs = models.TextField(null=True, blank=True)
    competences_requises = models.TextField(null=True, blank=True)
    mots_cles = models.CharField(max_length=255, null=True, blank=True)
    
    enseignant = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='sujets_encadres')
    superviseur = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='sujets_supervises')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='subjects')
    
    capacite = models.IntegerField(default=1) # correspond au nombre maximal d'étudiants
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')

    @property
    def academic_year(self):
        """Permet de récupérer l'année académique directement depuis le sujet"""
        return self.semester.academic_year

    def __str__(self):
        return self.titre