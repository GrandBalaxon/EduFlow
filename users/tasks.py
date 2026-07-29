from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def users_last_activity_check() -> None:
    """
    Проходится по всем активным пользователям сайта, что логинились, меняет статус is_active на False у пользователей,
    что не заходили на сайт последний месяц.
    """
    month_ago = timezone.now() - timedelta(days=30)
    users = User.objects.filter(is_active=True, last_login__isnull=False)

    deactivated_count = 0

    for user in users:
        if user.last_login < month_ago:
            user.is_active = False
            user.save()
            deactivated_count += 1

    print(f"Деактивировано пользователей: {deactivated_count}")
