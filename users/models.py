from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Введите почту")
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона"
    )
    city = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите город проживания"
    )
    avatar = models.ImageField(upload_to="users/avatar", blank=True, null=True, verbose_name="Аватар профиля")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        """Проверка прав, для суперпользователя всегда True"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Проверка прав на модули, для суперпользователя всегда True"""
        return self.is_superuser

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments", verbose_name="Пользователь"
    )
    date = models.DateField(auto_now_add=True, verbose_name="Дата платежа")
    course = models.ForeignKey(
        'core.Course', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Оплаченный курс"
    )
    lesson = models.ForeignKey(
        'core.Lesson', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Оплаченный отдельный урок"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")
    method = models.CharField(
        choices=[
            ('cash', 'Наличные'),
            ('transfer', 'Перевод')
        ],
        verbose_name="Метод оплаты"
    )

    def __str__(self):
        num = self.pk
        user = self.user.__str__()
        purchase = self.course.__str__() if self.course else self.lesson.__str__()
        amount = self.amount
        return f"{num} - {user} - {purchase} - {amount} - {self.date}"

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        'core.Course', on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Курс"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.email} → {self.course.title}'
