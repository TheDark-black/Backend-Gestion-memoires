from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# Serializer utilisé pour enregistrer un nouvel utilisateur
# avec hash sécurisé du mot de passe
class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'nom', 'prenom', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
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


