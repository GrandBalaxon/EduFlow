from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from core.mixins import OwnerOrModeratorFilterMixin
from core.models import Course, Lesson
from core.permissions import IsModerator, IsNotModerator, IsOwner
from core.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(OwnerOrModeratorFilterMixin, viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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


class LessonListApiView(OwnerOrModeratorFilterMixin, generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonRetrieveApiView(OwnerOrModeratorFilterMixin, generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonCreateApiView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonUpdateApiView(OwnerOrModeratorFilterMixin, generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyApiView(OwnerOrModeratorFilterMixin, generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]
