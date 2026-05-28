import uuid
from django.db import models

class Memoire(models.Model):
    STATUT_AVANCEMENT = [
        ('en_cours', 'En cours'),
        ('suspendu', 'Suspendu'),
        ('abandonne', 'Abandonné'),
        ('finalise', 'Finalisé'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # OneToOneField garantit qu'un étudiant n'a qu'un mémoire 
    # ET qu'un sujet n'est lié qu'à un seul mémoire.
    student = models.OneToOneField('Student', on_delete=models.CASCADE, related_name='memoire')
    subject = models.OneToOneField('Subject', on_delete=models.CASCADE, related_name='memoire')
    
    date_affectation = models.DateTimeField(auto_now_add=True)
    statut_avancement = models.CharField(
        max_length=20, 
        choices=STATUT_AVANCEMENT, 
        default='en_cours'
    )
    soutenable = models.BooleanField(default=False)
    date_validation_soutenabilite = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'memoires'