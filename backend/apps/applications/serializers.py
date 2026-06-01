from rest_framework import serializers

from backend.apps.users.models import Student
from .models import Application
from subjects.serializers import SubjectSerializer

class StudentSummarySerializer(serializers.ModelSerializer):
    nom = serializers.CharField(source='user.nom')
    prenom = serializers.CharField(source='user.prenom')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Student
        fields = ['id', 'matricule', 'nom', 'prenom', 'email', 'promotion', 'master']

class ApplicationSerializer(serializers.ModelSerializer):
    student_details = StudentSummarySerializer(source='student', read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'student', 'student_details', 'subject', 'subject_details', 
            'motivation', 'date_candidature', 'statut'
        ]