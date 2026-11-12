import logging

from .settings import *  # noqa: F401,F403

logging.disable(logging.INFO)

SECRET_KEY = "dummy-secret-key-for-ci"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
STRIPE_SECRET_KEY = "sk_test_dummy"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Ускоряет тесты, заменяя медленный PBKDF2 на MD5
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
