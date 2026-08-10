from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from core.models import Course
from users.models import Subscription


@shared_task
def send_course_update_notification(course_id: int) -> None:
    """Отправляет уведомление об обновлении курса всем его подписчикам."""
    course = Course.objects.get(id=course_id)
    now = timezone.now()
    four_hours_ago = now - timedelta(hours=4)
    if course.last_update_notification_date and course.last_update_notification_date > four_hours_ago:
        return

    subscribers = Subscription.objects.filter(course=course, is_active=True)
    recipient_list = [sub.user.email for sub in subscribers]

    if recipient_list:
        send_mail(
            subject=f"Курс {course.title} обновился!",
            message=f"Курс {course.title} был дополнен. Скорее спешите изучить все изменения и успехов в учёбе!"
                    f"Ссылка на курс: http://127.0.0.1:8000/course/{course.id}/",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
        )

    course.last_update_notification_date = now
    course.save(update_fields=['last_update_notification_date'])
