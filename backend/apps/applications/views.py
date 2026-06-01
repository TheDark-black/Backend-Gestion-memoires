from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from backend.apps.applications.serializers import ApplicationSerializer
from .models import Application, Student
from subjects.models import Subject

class ApplicationAPIView(APIView):

    # --- 1. DÉPOT D'UNE CANDIDATURE (Postuler) ---
    def post(self, request):
        student_id = request.data.get('student')
        subject_id = request.data.get('subject')
        
        student = get_object_or_404(Student, pk=student_id)
        subject = get_object_or_404(Subject, pk=subject_id)

        # CONTRAINTES MÉTIER

        # C1 : Si le sujet est déjà complet
        if subject.statut in ['complet', 'archive']:
            return Response(
                {"error": "Ce sujet est complet ou archivé. Les candidatures y sont fermées."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # C2 : Si l'étudiant a déjà une candidature acceptée ailleurs
        has_accepted = Application.objects.filter(student=student, statut='acceptee').exists()
        if has_accepted:
            return Response(
                {"error": "Vous avez déjà une candidature acceptée. Vous ne pouvez plus postuler."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # C3 : Un étudiant ne peut candidater que sur un seul sujet à la fois (Pas de doublon en attente)
        has_pending = Application.objects.filter(student=student, statut='en_attente').exists()
        if has_pending:
            return Response(
                {"error": "Vous avez déjà une candidature en attente. Annulez-la pour changer de sujet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Enregistrement
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Positionnement enregistré avec succès.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # --- 2. ANNULATION DE LA CANDIDATURE ---
    def delete(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        
        # CONTRAINTE : Annulation possible TANT QU'aucune décision n'a été prise
        if application.statut != 'en_attente':
            return Response(
                {"error": f"Action impossible. La candidature a déjà été {application.statut}."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        application.delete()
        return Response({
            "message": "Candidature annulée avec succès."
        }, status=status.HTTP_204_NO_CONTENT)


    # --- 3. CONSULTATION, FILTRAGE ET HISTORIQUE ---
    def get(self, request, pk=None):
        if pk:
            application = get_object_or_404(Application, pk=pk)
            serializer = ApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Filtres applicables
        student_id = request.query_params.get('student_id')   # Pour l'historique de l'étudiant
        subject_id = request.query_params.get('subject_id')   # Pour voir les candidats d'un sujet
        statut = request.query_params.get('statut')           # Filtrer par 'en_attente', 'acceptee', etc.

        applications = Application.objects.all()

        if student_id:
            applications = applications.filter(student_id=student_id)
        if subject_id:
            applications = applications.filter(subject_id=subject_id)
        if statut:
            applications = applications.filter(statut=statut)

        # [FONCTIONNALITÉ AVANCÉE : Classement par ordre chronologique]
        # Les premières personnes à postuler apparaissent en haut de la liste
        applications = applications.order_by('date_candidature')

        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)