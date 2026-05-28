from django.urls import path
from .views import AcademicYearAPIView

urlpatterns = [
    # Store : POST /api/academic-years/store/
    path('academic-years/store/', AcademicYearAPIView.as_view(), name='year-store'),
    
    # Update : PUT /api/academic-years/update/<uuid>/
    path('academic-years/update/<uuid:pk>/', AcademicYearAPIView.as_view(), name='year-update'),
    
    # Delete : DELETE /api/academic-years/delete/<uuid>/
    path('academic-years/delete/<uuid:pk>/', AcademicYearAPIView.as_view(), name='year-delete'),

    # Route pour lister toutes les années academique enregister :
    path('academic-years/', AcademicYearAPIView.as_view(), name='year-list-get'),
]