import uuid
from django.db import models
from teachers.models import Teacher
from semesters.models import Semester

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
    
    # Relations (Assurez-vous que les modèles Teacher et Semester existent)
    encadrant = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='sujets_encadres')
    superviseur = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE, related_name='sujets_supervises')
    semester = models.ForeignKey('semesters.Semester', on_delete=models.CASCADE, related_name='subjects')
    
    capacite = models.IntegerField(default=1)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')

    def __str__(self):
        return self.titre