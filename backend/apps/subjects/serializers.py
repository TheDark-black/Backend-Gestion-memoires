from rest_framework import serializers
from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    # On utilise des SerializerMethodField pour éviter que Django ne crashe 
    # si les relations transversales sont vides ou mal nommées au moment du POST
    enseignant_nom = serializers.SerializerMethodField()
    superviseur_nom = serializers.SerializerMethodField()
    semester_libelle = serializers.SerializerMethodField()
    annee_academique_libelle = serializers.SerializerMethodField()
    total_candidatures = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    def get_enseignant_nom(self, obj):
        try:
            return f"{obj.enseignant.user.nom} {obj.enseignant.user.prenom}"
        except AttributeError:
            return None

    def get_superviseur_nom(self, obj):
        try:
            return f"{obj.superviseur.user.nom} {obj.superviseur.user.prenom}"
        except AttributeError:
            return None

    def get_semester_libelle(self, obj):
        try:
            # Vérifiez si votre modèle Semester utilise 'libelle', 'nom' ou 'code'
            return getattr(obj.semester, 'libelle', str(obj.semester))
        except AttributeError:
            return None

    def get_annee_academique_libelle(self, obj):
        try:
            return getattr(obj.semester.academic_year, 'libelle', str(obj.semester.academic_year))
        except AttributeError:
            return None

    def get_total_candidatures(self, obj):
        try:
            return obj.applications.count()
        except AttributeError:
            return 0

    def validate(self, data):
        """
        Validation globale du sujet.
        """
        enseignant = data.get('enseignant')
        superviseur = data.get('superviseur')

        if enseignant == superviseur:
            raise serializers.ValidationError({
                "superviseur": "L'encadrant ne peut pas être son propre superviseur."
            })

        grades_superieurs = ['Maitre_Conferences', 'Professeur']
        if superviseur and superviseur.grade not in grades_superieurs:
            raise serializers.ValidationError({
                "superviseur": "Le superviseur doit être au minimum Maître de Conférences ou Professeur."
            })

        return data