import uuid

from backend.apps.academic import models
from backend.apps.users.models import Student


class Application(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='applications')
    motivation = models.TextField(null=True, blank=True)
    date_candidature = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        db_table = 'applications'
        unique_together = ('student', 'subject') 
        ordering = ['date_candidature'] # Permet le classement par ordre d'arrivée