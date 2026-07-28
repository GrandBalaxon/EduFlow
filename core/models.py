from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название",
        help_text="Введите название курса"
    )
    preview_image = models.ImageField(
        upload_to="previews/courses/",
        blank=True,
        null=True,
        verbose_name="Превью (картинка)"
    )
    description = models.TextField(verbose_name="Краткое описание")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="courses")
    price = models.PositiveIntegerField(verbose_name='Цена (в рублях)', default=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название",
        help_text="Введите название урока"
    )
    description = models.TextField(
        verbose_name="Краткое описание",
        help_text="Введите краткое описание урока"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        help_text="Укажите к какому курсу относится урок"
    )
    preview_image = models.ImageField(
        upload_to="previews/lessons/",
        blank=True,
        null=True,
        verbose_name="Превью (картинка)"
    )
    video_link = models.URLField(unique=True, blank=True, null=True, verbose_name="Ссылка на видео урока")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="lessons")
    price = models.PositiveIntegerField(verbose_name='Цена (в рублях)', default=100)

    def __str__(self):
        return f"{self.course.title}: Урок {self.id} - {self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
