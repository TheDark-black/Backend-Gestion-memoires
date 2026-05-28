from rest_framework import serializers
from .models import Memoire

class MemoireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memoire
        fields = '__all__'

    def validate_subject(self, value):
        # Vérifie si le sujet est déjà présent dans la table memoires
        if Memoire.objects.filter(subject=value).exists():
            raise serializers.ValidationError("Ce sujet est déjà attribué à un autre étudiant.")
        return value

    def validate_student(self, value):
        # Vérifie si l'étudiant a déjà un mémoire
        if Memoire.objects.filter(student=value).exists():
            raise serializers.ValidationError("Cet étudiant possède déjà un sujet de mémoire.")
        return value