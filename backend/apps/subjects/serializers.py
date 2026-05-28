from rest_framework import serializers

from backend.apps.academic import models
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    # Détails lisibles pour Angular
    encadrant_nom = serializers.ReadOnlyField(source='encadrant.user.nom')
    superviseur_nom = serializers.ReadOnlyField(source='superviseur.user.nom')
    semester_libelle = serializers.ReadOnlyField(source='semester.libelle')

    class Meta:
        model = Subject
        fields = '__all__'

    def validate(self, data):
        """
        Validation globale du sujet.
        """
        encadrant = data.get('encadrant')
        superviseur = data.get('superviseur')

        # L'encadrant et le superviseur doivent être différents
        if encadrant == superviseur:
            raise serializers.ValidationError({
                "superviseur": "L'encadrant ne peut pas être son propre superviseur."
            })

        # Le superviseur doit avoir le grade requis
        grades_superieurs = ['Maitre_Conferences', 'Professeur']
        if superviseur and superviseur.grade not in grades_superieurs:
            raise serializers.ValidationError({
                "superviseur": "Le superviseur doit être au minimum Maître de Conférences ou Professeur."
            })

        return data