from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import User, Teacher, Student
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer, TeacherSerializer, StudentSerializer 
from rest_framework.permissions import IsAuthenticated
from .permissions import CanManageUsers, CanCreatSubject, CanUploadDocument
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, CanManageUsers]

    @action(
    detail=True,
    methods=['patch'],
    url_path='toggle-active')
    
    def toggle_active(self, request, pk=None):

        user = self.get_object()

        user.is_active = not user.is_active

        user.save()

        return Response(
            {
                'message': 'Statut utilisateur modifié',
                'is_active': user.is_active
            }
        )

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class StudentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class UserListView(ListAPIView):
    queryset = User.objects.all().order_by('-created_at')  # Trie du plus récent au plus ancien
    serializer_class = UserSerializer

    
class EncadrantListView(ListAPIView):
    queryset = Teacher.objects.all().order_by('grade')  # Trie du plus récent au plus ancien
    serializer_class = TeacherSerializer

    
