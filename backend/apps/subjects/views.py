# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Subject
from django.db.models import Q
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



   # --- ARCHIVAGE (SUPPRESSION LOGIQUE) ---
    def delete(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        
        # Au lieu de subject.delete() (suppression physique), on archive
        subject.statut = 'archive'
        subject.save()
        
        return Response({
            "message": "Le sujet a été archivé avec succès (suppression logique)"
        }, status=status.HTTP_200_OK)
    

    
    def get(self, request, pk=None):
        # AFFICHAGE DES DÉTAILS D'UN SUJET (Si un ID est fourni dans l'URL) ---
        if pk:
            subject = get_object_or_404(Subject, pk=pk)
            serializer = SubjectSerializer(subject)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # LISTE FILTRÉE PAR SEMESTRE ENCADRANT ET STATUT(Si pas d'ID fourni) ---
        semester_id = request.query_params.get('semester_id')
        enseignant_id = request.query_params.get('enseignant_id')
        statut = request.query_params.get('statut')
        search_query = request.query_params.get('search')
        
        # affichage de toute les sujet enregistrer 
        subjects = Subject.objects.all()


        # [CONTRAINTE VISIBILITÉ] : Si l'utilisateur connecté est un étudiant, il ne voit QUE les sujets publiés
        # (À adapter selon votre système de rôles utilisateur)
        is_student = request.user.groups.filter(name='Students').exists() if request.user.is_authenticated else True 
        if is_student:
            subjects = subjects.filter(statut='publie')
        elif statut:
            # Si c'est un prof/admin, il peut filtrer par le statut de son choix (brouillon, complet, etc.)
            subjects = subjects.filter(statut=statut)

        # Recherche par mot-clé globale (titre, résumé, mots-clés)
        if search_query:
            subjects = subjects.filter(
                Q(titre__icontains=search_query) | 
                Q(resume__icontains=search_query) | 
                Q(mots_cles__icontains=search_query)
            )

        
        if semester_id:
            subjects = subjects.filter(semester_id=semester_id)
        if enseignant_id:
            subjects = subjects.filter(encadrant_id=enseignant_id)
        if statut:
            subjects = subjects.filter(statut=statut)
            
        subjects = subjects.order_by('-id')
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)