from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from core.mixins import LessonOwnerOrModeratorFilterMixin
from core.models import Course, Lesson
from core.paginators import MyPageNumberPagination
from core.permissions import IsModerator, IsNotModerator, IsOwner
from core.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(LessonOwnerOrModeratorFilterMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MyPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonListApiView(LessonOwnerOrModeratorFilterMixin, generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MyPageNumberPagination


class LessonRetrieveApiView(LessonOwnerOrModeratorFilterMixin, generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonCreateApiView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateApiView(LessonOwnerOrModeratorFilterMixin, generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyApiView(LessonOwnerOrModeratorFilterMixin, generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]
