# apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, 
    TeacherViewSet, 
    StudentViewSet,
    
)

# 1. On configure le routeur pour les ViewSets (CRUD automatique)
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'teachers', TeacherViewSet, basename='teachers')
router.register(r'students', StudentViewSet, basename='students')

urlpatterns = router.urls