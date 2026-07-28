from celery import shared_task
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL
from core.models import Course
from users.models import Subscription


@shared_task
def send_course_update_notification(course_id: int) -> None:
    """Отправляет уведомление об обновлении курса всем его подписчикам."""
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course, is_active=True)
    recipient_list = [sub.user.email for sub in subscribers]

    if recipient_list:
        send_mail(
            subject=f"Курс {course.title} обновился!",
            message=f"Курс {course.title} был дополнен. Скорее спешите изучить все изменения и успехов в учёбе!"
                    f"Ссылка на курс: http://127.0.0.1:8000/course/{course.id}/",
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
        )
