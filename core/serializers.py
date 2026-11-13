from rest_framework import serializers

from core.models import Course, Lesson
from core.validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели уроков."""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [YouTubeLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели курсов."""
    lessons_count = serializers.IntegerField(source='lessons_count_annotated', read_only=True)
    is_subscribed = serializers.BooleanField(source='is_subscribed_annotated', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
