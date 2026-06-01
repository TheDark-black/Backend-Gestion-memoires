from django.shortcuts import render
from rest_framework import generics, status
from .serializers import (
    RegisterSerializer, 
    CurrentUserSerializer, 
    UpdateProfileSerializer, 
    ChangePasswordSerializer,
    LogoutSerializer,
    RequestPasswordResetSerializer,
    ResetPasswordSerializer,
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import  RetrieveAPIView
from rest_framework.views import APIView
from apps.users.views import UserListView
from apps.users.views import EncadrantListView
from drf_spectacular.utils import extend_schema
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from apps.users.models import User


# Vue permettant l'inscription d'un nouvel utilisateur
class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer


# Vue permettant à l'utilisateur connecté
# de consulter et modifier son profil
class CurrentUserView(RetrieveAPIView):

    serializer_class = CurrentUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateProfileSerializer
        
        return CurrentUserSerializer

    def patch(self,request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue permettant à l'utilisateur connecté
# de modifier son mot de passe
@extend_schema(request=ChangePasswordSerializer)
class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
        
            if not user.check_password(old_password):

                return Response({'error':'Ancien mot de passe incorrect'},status=status.HTTP_400_BAD_REQUEST)
        
            user.set_password(new_password)
            user.save()
            return Response({'message':'Mot de passe modifié avec succès'})
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue permettant de déconnecter un utilisateur
# en blacklistant son refresh token JWT
@extend_schema(request=LogoutSerializer)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Déconnexion réussie"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vue permettant de générer un token de réinitialisation
# lorsqu'un utilisateur oublie son mot de passe
class RequestPasswordResetView(APIView):

    serializer_class = RequestPasswordResetSerializer

    permission_classes = []

    def post(self, request):

        serializer = RequestPasswordResetSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']

            try:

                user = User.objects.get(email=email)

                token_generator = PasswordResetTokenGenerator()

                token = token_generator.make_token(user)

                return Response(
                    {
                        'message': 'Token généré avec succès',
                        'token': token,
                        'user_id': str(user.id)
                    },
                    status=status.HTTP_200_OK
                )

            except User.DoesNotExist:

                return Response(
                    {
                        'error': 'Utilisateur introuvable'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# Vue permettant de réinitialiser le mot de passe
# à l'aide du token généré précédemment
class ResetPasswordView(APIView):

    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request):

        serializer = ResetPasswordSerializer(data = request.data)
        if serializer.is_valid():

            user_id = serializer.validated_data['user_id']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(id =user_id)
                token_generator = PasswordResetTokenGenerator()
                if token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({'message':'Mot de passe réinitialisé avec succès'}, status=status.HTTP_200_OK)
                
                return Response({'error':'Token invalide'}, status=status.HTTP_400_BAD_REQUEST)
            
            except User.DoesNotExist:
                return Response({'error':'Utilisateur introuvable'}, status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  