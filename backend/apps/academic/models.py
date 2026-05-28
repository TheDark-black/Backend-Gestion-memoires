import uuid
from django.db import models


class AcademicYear(models.Model):
    """
    Représente une année académique (ex: 2025-2026).
    Toutes les activités (sujets, soutenances) sont rattachées à une année.
    """

    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('archivee', 'Archivée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    libelle = models.CharField(max_length=20)           # ex: "2025-2026"
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')

    class Meta:
        db_table = 'academic_years'
        ordering = ['-date_debut']

    def __str__(self):
        return self.libelle