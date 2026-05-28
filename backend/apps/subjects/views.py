# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Subject
from .serializers import SubjectSerializer

class SubjectAPIView(APIView):

    # --- FONCTION STORE (Création) ---
    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Enregistre en base de données
            return Response({
                "message": "Sujet enregistré avec succès",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # --- FONCTION UPDATE (Modification) ---
    def put(self, request, pk):
        # On récupère le sujet existant via son UUID (pk)
        subject = get_object_or_404(Subject, pk=pk)
        
        # On passe l'instance existante et les nouvelles données au serializer
        serializer = SubjectSerializer(subject, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Sujet mis à jour avec succès",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # --- FONCTION DELETE (Suppression) ---
    def delete(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()
        return Response({
            "message": "Sujet supprimé définitivement"
        }, status=status.HTTP_204_NO_CONTENT)
    

    
    def get(self, request, pk=None):
        # AFFICHAGE DES DÉTAILS D'UN SUJET (Si un ID est fourni dans l'URL) ---
        if pk:
            subject = get_object_or_404(Subject, pk=pk)
            serializer = SubjectSerializer(subject)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # LISTE FILTRÉE PAR SEMESTRE ENCADRANT ET STATUT(Si pas d'ID fourni) ---
        semester_id = request.query_params.get('semester_id')
        encadrant_id = request.query_params.get('encadrant_id')
        statut = request.query_params.get('statut')
        
        # affichage de toute les sujet enregistrer 
        subjects = Subject.objects.all()
        
        if semester_id:
            subjects = subjects.filter(semester_id=semester_id)
        if encadrant_id:
            subjects = subjects.filter(encadrant_id=encadrant_id)
        if statut:
            subjects = subjects.filter(statut=statut)
            
        subjects = subjects.order_by('-id')
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)