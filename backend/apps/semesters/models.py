import uuid
from django.db import models
from academic.models import AcademicYear

class Semester(models.Model):
    STATUT_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('ferme', 'Fermé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="semesters")
    libelle = models.CharField(max_length=50) # Ex: "Semestre 1"
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ferme')
    
    # --- Paramétrage des dates importantes ---
    date_limite_sujets = models.DateField(null=True, blank=True)         # Proposition des sujets
    date_limite_candidatures = models.DateField(null=True, blank=True)   # Positionnement des étudiants
    date_limite_documents = models.DateField(null=True, blank=True)      # Dépôt des documents (mémoires)
    
    # Période de soutenance (Début et Fin)
    date_debut_soutenances = models.DateField(null=True, blank=True)
    date_fin_soutenances = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'semesters'

    def __str__(self):
        return f"{self.libelle} ({self.academic_year.libelle})"