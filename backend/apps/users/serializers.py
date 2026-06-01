from rest_framework import serializers
from .models import User, Teacher, Student, Role


# Serializer utilisé pour afficher les informations publiques
# des utilisateurs sans exposer les données sensibles
class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all())
    
    class Meta:
        model = User

        fields = [
            'id',
            'nom',
            'prenom',
            'email',
            'roles',
            'is_active',
            'created_at'
        ]

        read_only_fields = [
            'id',
            'created_at'
        ]

        
        
    # Création d'utilisateur via le manager personnalisé
    # por synchroniser automatiquement les rôles 
    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)
        return user


# Serializer utilisé pour afficher les informations
# des enseignants
class TeacherSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    class Meta:
        model = Teacher
        fields = '__all__'


# Serializer utilisé pour afficher les informations
# des étudiants
class StudentSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    class Meta:
        model = Student
        fields = '__all__'
        