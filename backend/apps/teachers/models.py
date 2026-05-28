import uuid
from django.db import models
from django.conf import settings # Pour lier à l'utilisateur par défaut

class Teacher(models.Model):
    GRADE_CHOICES = [
        ('Assistant', 'Assistant'),
        ('Maitre_Assistant', 'Maître Assistant'),
        ('Maitre_Conferences', 'Maître de Conférences'),
        ('Professeur', 'Professeur'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES)
    specialite = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.user.nom} - {self.grade}"