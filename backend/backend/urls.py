"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/', include('apps.users.urls')),

    # Schema OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    
    # JWT endpoints
    # Connnexion : POST /api/token/ avec email et password pour obtenir access et refresh token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Rafraichissement du token : POST /api/token/refresh/ avec le refresh token pour obtenir un nouveau access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoints d'authentification personnalisés (inscription, profil, changement de mot de passe, etc.)
    path('api/auth/', include('apps.authentication.urls')),
]
