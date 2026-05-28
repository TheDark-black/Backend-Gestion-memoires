from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Subject, Memoire
from .serializers import MemoireSerializer

class AssignSubjectView(APIView):
    def post(self, request):
        serializer = MemoireSerializer(data=request.data)
        
        if serializer.is_valid():
            # On enregistre l'attribution
            memoire = serializer.save()
            
            # MISE À JOUR DU STATUT DU SUJET
            # Une fois attribué, le sujet doit passer en statut 'complet'
            # pour ne plus apparaître dans la liste des sujets disponibles.
            subject = memoire.subject
            subject.statut = 'complet'
            subject.save()

            return Response({
                "message": "Le sujet a été officiellement attribué.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)