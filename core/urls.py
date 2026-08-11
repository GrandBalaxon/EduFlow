from django.urls import path
from rest_framework.routers import DefaultRouter

from core.apps import CoreConfig
from core.views import CourseViewSet, LessonListApiView, LessonCreateApiView, LessonRetrieveApiView, \
    LessonUpdateApiView, LessonDestroyApiView
from users.views import SubscriptionApiView, PaymentCreateApiView

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

    # ссылки на платежи
    path('<int:course_pk>/payment/', PaymentCreateApiView.as_view(), name='course_payment'),
    path('<int:course_pk>/lesson/<int:pk>/payment/', PaymentCreateApiView.as_view(), name='lesson_payment'),
]

urlpatterns += router.urls
