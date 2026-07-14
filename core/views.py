from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from core.models import Course, Lesson
from core.permissions import IsModerator, IsNotModerator
from core.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ['list', 'retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator]
        return [permission() for permission in self.permission_classes]


class LessonListApiView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class LessonRetrieveApiView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class LessonCreateApiView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]


class LessonUpdateApiView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]
