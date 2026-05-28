from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AcademicYear
from .serializers import AcademicYearSerializer

class AcademicYearAPIView(APIView):

    # --- ENREGISTRER UNE ANNÉE (Store) ---
    def post(self, request):
        serializer = AcademicYearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Année académique enregistrée",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- MODIFIER UNE ANNÉE (Update) ---
    def put(self, request, pk):
        year = get_object_or_404(AcademicYear, pk=pk)
        serializer = AcademicYearSerializer(year, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Année académique mise à jour",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- SUPPRIMER UNE ANNÉE (Delete) ---
    def delete(self, request, pk):
        year = get_object_or_404(AcademicYear, pk=pk)
        # Attention : Supprimer une année supprimera les semestres liés (CASCADE)
        year.delete()
        return Response({
            "message": "Année académique supprimée avec succès"
        }, status=status.HTTP_204_NO_CONTENT)
    
    # --- LIRE TOUTES LES ANNÉES (List) ---
    def get(self, request):
        years = AcademicYear.objects.all().order_by('-date_debut')
        serializer = AcademicYearSerializer(years, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)