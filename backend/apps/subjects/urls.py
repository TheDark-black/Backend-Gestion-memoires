from django.urls import path
from .views import SubjectAPIView

urlpatterns = [
    # Route pour l'enregistrement (Store)
    # Appelé par Angular avec : http.post('.../subjects/store/')
    path('subjects/', SubjectAPIView.as_view(), name='subject-store'),

    # Route pour la modification (Update) 
    # Appelé par Angular avec : http.put('.../subjects/update/<uuid>/')
    path('subjects/update/<uuid:pk>/', SubjectAPIView.as_view(), name='subject-update'),

    # Route pour la suppression (Delete)
    # Appelé par Angular avec : http.delete('.../subjects/delete/<uuid>/')
    path('subjects/<uuid:pk>/', SubjectAPIView.as_view(), name='subject-delete'),
    
    # Route pour lister toutes les sujet enregistrer
    path('subjects/obtenir', SubjectAPIView.as_view(), name='subject-list-get'),

    # Route pour avoir les DÉTAILS d'un sujet (nécessite l'ID)
    path('subjects/<uuid:pk>/', SubjectAPIView.as_view(), name='subject-detail'),
]