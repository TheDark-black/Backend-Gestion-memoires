from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Semester
from .serializers import SemesterSerializer

class SemesterAPIView(APIView):

    # --- ENREGISTRER UN SEMESTRE (Store) ---
    def post(self, request):
        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Semestre créé avec succès",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- MODIFIER UN SEMESTRE (Update) ---
    def put(self, request, pk):
        semester = get_object_or_404(Semester, pk=pk)
        # partial=True permet de ne modifier que certains champs si besoin
        serializer = SemesterSerializer(semester, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Semestre mis à jour avec succès",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- SUPPRIMER UN SEMESTRE (Delete) ---
    def delete(self, request, pk):
        semester = get_object_or_404(Semester, pk=pk)
        semester.delete()
        return Response({
            "message": "Semestre supprimé avec succès"
        }, status=status.HTTP_204_NO_CONTENT)
    
    # --- LIRE TOUS LES SEMESTRES (List) ---
    def get(self, request):
        semesters = Semester.objects.all()
        serializer = SemesterSerializer(semesters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)