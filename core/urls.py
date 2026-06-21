from core.apps import CoreConfig
from rest_framework.routers import DefaultRouter

from core.views import CourseViewSet

app_name = CoreConfig.name

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')

urlpatterns = []

urlpatterns += router.urls
