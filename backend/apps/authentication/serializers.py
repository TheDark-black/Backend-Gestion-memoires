from rest_framework import serializers
from apps.users.models import Student, Teacher, User
from rest_framework_simplejwt.tokens import RefreshToken


# Serializer utilisé pour enregistrer un nouvel utilisateur
# avec hash sécurisé du mot de passe
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=8)

    # Étape 1 : On déclare les champs spécifiques en "write_only" pour qu'ils soient acceptés dans le JSON
    matricule = serializers.CharField(required=False, write_only=True)
    promotion = serializers.CharField(required=False, write_only=True)
    master = serializers.CharField(required=False, write_only=True)
    semestre = serializers.CharField(required=False, write_only=True)
    
    grade = serializers.CharField(required=False, write_only=True)
    specialite = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'password', 'role', 
                  'matricule', 'promotion', 'master', 'semestre', 'grade', 'specialite']

    def create(self, validated_data):
            # Étape 2 : On extrait les données spécifiques avant de créer l'utilisateur de base
            matricule = validated_data.pop('matricule', None)
            promotion = validated_data.pop('promotion', None)
            master = validated_data.pop('master', None)
            semestre = validated_data.pop('semestre', None)
            
            grade = validated_data.pop('grade', None)
            specialite = validated_data.pop('specialite', None)
            
            password = validated_data.pop('password')

            # Étape 3 : Création de l'utilisateur de base (via votre manager qui gère les rôles)
            user = User.objects.create_user(password=password, **validated_data)

            # Étape 4 : Création du profil lié selon le rôle
            if user.role == 'etudiant':
                if not matricule:
                    raise serializers.ValidationError({"matricule": "Le matricule est obligatoire pour un étudiant."})
                Student.objects.create(
                    user=user,
                    matricule=matricule,
                    promotion=promotion,
                    master=master,
                    semestre=semestre
                )
            elif user.role in ['enseignant', 'superviseur']:
                if not grade:
                    raise serializers.ValidationError({"grade": "Le grade est obligatoire pour un enseignant."})
                Teacher.objects.create(
                    user=user,
                    grade=grade,
                    specialite=specialite
                )

            return user

# Serializer utilisé pour récupérer le refresh token
# lors de la déconnexion de l'utilisateur
class LogoutSerializer(serializers.Serializer):
    
    refresh = serializers.CharField()

    def save(self):
        refresh_token = self.validated_data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()


# Serializer utilisé pour afficher les informations
# du profil de l'utilisateur connecté
class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'nom' ,'prenom', 'email', 'role', 'created_at']


# Serializer utilisé pour modifier les informations
# du profil utilisateur connecté
class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['nom','prenom','email']


# Serializer utilisé pour valider l'ancien et
# le nouveau mot de passe de l'utilisateur
class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)


# Serializer utilisé pour vérifier l'email de l'utilisateur
# avant de générer un token de réinitialisation du mot de passe
class RequestPasswordResetSerializer(serializers.Serializer):

    email = serializers.EmailField()

# Serializer utilisé pour recevoir le token de réinitialisation
# ainsi que le nouveau mot de passe choisi par l'utilisateur
class ResetPasswordSerializer(serializers.Serializer):

    user_id = serializers.UUIDField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)



