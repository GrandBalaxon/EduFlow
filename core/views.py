from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from core.mixins import LessonOwnerOrModeratorFilterMixin
from core.models import Course, Lesson
from core.paginators import MyPageNumberPagination
from core.permissions import IsModerator, IsNotModerator, IsOwner
from core.serializers import CourseSerializer, LessonSerializer
from core.tasks import send_course_update_notification


@extend_schema(tags=["Курсы"])
@extend_schema_view(
    list=extend_schema(summary='Список курсов', description='Модератор видит все курсы, пользователь — только свои.'),
    create=extend_schema(summary='Создание курса', description='Создать курс может любой авторизованный, кроме модератора.'),
    retrieve=extend_schema(summary='Детали курса', description='Модератор или владелец получает информацию о курсе.'),
    update=extend_schema(summary='Обновление курса', description='Модератор или владелец полностью обновляет данные курса.'),
    partial_update=extend_schema(summary='Частичное обновление курса', description='Модератор или владелец частично обновляет данные курса.'),
    destroy=extend_schema(summary='Удаление курса', description='Только владелец (не модератор) может удалить курс.'),
)
class CourseViewSet(LessonOwnerOrModeratorFilterMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        send_course_update_notification.delay(course.id)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return [permission() for permission in self.permission_classes]


@extend_schema(tags=["Уроки"], summary="Список уроков курса")
class LessonListApiView(LessonOwnerOrModeratorFilterMixin, generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MyPageNumberPagination

@extend_schema(tags=["Уроки"], summary="Детали урока")
class LessonRetrieveApiView(LessonOwnerOrModeratorFilterMixin, generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

@extend_schema(tags=["Уроки"], summary="Создание урока")
class LessonCreateApiView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        course_pk = self.kwargs.get('course_pk')
        course = get_object_or_404(Course, pk=course_pk)

        # Только владелец курса может добавлять в него уроки
        if course.owner != self.request.user:
            raise PermissionDenied('Только владелец курса может добавлять уроки')

        serializer.save(owner=self.request.user, course=course)

@extend_schema(tags=["Уроки"], summary="Обновление урока")
class LessonUpdateApiView(LessonOwnerOrModeratorFilterMixin, generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

@extend_schema(tags=["Уроки"], summary="Удаление урока")
class LessonDestroyApiView(LessonOwnerOrModeratorFilterMixin, generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]
