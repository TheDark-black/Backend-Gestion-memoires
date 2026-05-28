from django.urls import path
from .views import (
    RegisterView, 
    CurrentUserView, 
    ChangePasswordView,
    LogoutView,
    RequestPasswordResetView,
    ResetPasswordView,
)




urlpatterns = [

    # Endpoint d'inscription des utilisateurs
    path('register/', RegisterView.as_view(), name='register'),

    # Endpoint permettant à l'utilisateur connecté
    # de consulter ou modifier son profil
    path('me/', CurrentUserView.as_view(), name='current-user'),

    # Endpoint permettant de modifier
    # le mot de passe utilisateur
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Endpoint de déconnexion utilisateur
    # avec blacklist du refresh token
    path('logout/',LogoutView.as_view(), name='logout'),

    # Endpoint permettant de demander un token de reinitialisation du mot de passe
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),

    # Endpoint permettant de definir un nouveau mot de passe apres validation du token de reinitialisation
    path('reset-password/',ResetPasswordView.as_view(), name= 'reset-password')
]
