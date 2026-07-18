class OwnerOrModeratorFilterMixin:
    """
    Примесь для фильтрации queryset по владельцу.
    Модератор видит все объекты, остальные пользователи — только свои.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderator').exists():
            return queryset
        return queryset.filter(owner=self.request.user)
