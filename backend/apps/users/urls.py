from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TeacherViewSet, StudentViewSet



router = DefaultRouter()

router.register(r'users',UserViewSet,basename='users')
router.register(r'teachers',TeacherViewSet,basename = 'teachers')
router.register(r'students',StudentViewSet,basename = 'students')


urlpatterns  = router.urls