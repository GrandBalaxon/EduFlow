from core.models import Lesson


class LessonOwnerOrModeratorFilterMixin:
    """
    Примесь для фильтрации queryset уроков по владельцу.
    Модератор видит все объекты, остальные пользователи — только свои.
    """
    queryset = Lesson.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderator').exists():
            return queryset
        return queryset.filter(owner=self.request.user)
