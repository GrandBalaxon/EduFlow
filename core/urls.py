from core.apps import CoreConfig
from rest_framework.routers import DefaultRouter

from core.views import CourseViewSet

name = CoreConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = []

urlpatterns += router.urls
