from django.urls import path
from .views import SemesterAPIView

urlpatterns = [
    # Route pour créer : POST /api/semesters/store/
    path('semester/', SemesterAPIView.as_view(), name='semester-store'),
    
    # Route pour modifier : PUT /api/semesters/update/<uuid>/
    path('semester/update/<uuid:pk>/', SemesterAPIView.as_view(), name='semester-update'),
    
    # Route pour supprimer : DELETE /api/semesters/delete/<uuid>/
    path('semester/<uuid:pk>/', SemesterAPIView.as_view(), name='semester-delete'),

    # Route pour obtenir toutes les semestres enregistrer 
    path('semesters/obtenir', SemesterAPIView.as_view(), name='semester-list-create'),
]