import uuid
from django.db import models
from academic.models import AcademicYear

class Semester(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=50)
    statut = models.CharField(max_length=20, default='ferme')