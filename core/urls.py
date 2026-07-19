from django.urls import path
from rest_framework.routers import DefaultRouter

from core.apps import CoreConfig
from core.views import CourseViewSet, LessonListApiView, LessonCreateApiView, LessonRetrieveApiView, \
    LessonUpdateApiView, LessonDestroyApiView
from users.views import SubscriptionApiView

app_name = CoreConfig.name

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')


urlpatterns = [
    path('<int:course_pk>/lesson/', LessonListApiView.as_view(), name='lesson_list'),
    path('<int:course_pk>/lesson/create/', LessonCreateApiView.as_view(), name='lesson_create'),
    path('<int:course_pk>/lesson/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson_details'),
    path('<int:course_pk>/lesson/<int:pk>/update/', LessonUpdateApiView.as_view(), name='lesson_update'),
    path('<int:course_pk>/lesson/<int:pk>/delete/', LessonDestroyApiView.as_view(), name='lesson_delete'),

    path('<int:course_pk>/subscription/', SubscriptionApiView.as_view(), name='subscription'),
]

urlpatterns += router.urls
