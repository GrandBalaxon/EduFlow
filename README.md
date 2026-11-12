# 🎓 EduFlow Django REST API

[![CI](https://github.com/GrandBalaxon/EduFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/GrandBalaxon/EduFlow/actions/workflows/ci.yml)
[![Coverage](https://raw.githubusercontent.com/GrandBalaxon/EduFlow/python-coverage-comment-action-data/badge.svg)](https://github.com/GrandBalaxon/EduFlow/tree/python-coverage-comment-action-data)
[![License](https://img.shields.io/badge/license-MIT-3DA639.svg?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14-3776AB.svg?logo=python&logoColor=white)](https://www.python.org)
[![Django](https://img.shields.io/badge/django-6.0-092E20.svg?logo=django&logoColor=white)](https://www.djangoproject.com)

[![DRF](https://img.shields.io/badge/DRF-3.17-A30000.svg?logo=django&logoColor=white)](https://www.django-rest-framework.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Celery](https://img.shields.io/badge/Celery-5.6-37814A.svg?logo=celery&logoColor=white)](https://docs.celeryq.dev)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg?logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Stripe](https://img.shields.io/badge/Stripe-Payments-635BFF.svg?logo=stripe&logoColor=white)](https://stripe.com)
[![Poetry](https://img.shields.io/badge/Poetry-2.x-60A5FA.svg?logo=poetry&logoColor=white)](https://python-poetry.org)

## 📚 О проекте

EduFlow — REST API образовательной платформы для управления курсами, уроками, пользователями, подписками и платежами.

Проект реализован на Django REST Framework и полностью контейнеризирован с использованием Docker и Docker Compose.

## Возможности проекта

### Пользователи
- Регистрация пользователей.
- Авторизация через JWT.
- Управление профилем.
- Просмотр публичных профилей.
- История платежей пользователя.

### Курсы и уроки
- Создание и управление курсами.
- Добавление уроков в курсы.
- Разграничение доступа:
  - пользователь;
  - владелец контента;
  - модератор.

### Подписки
- Подписка пользователей на курсы.
- Управление статусом подписки.

### Платежи
- Интеграция со Stripe.
- Оплата курсов и отдельных уроков.
- Проверка статуса платежа.

### Фоновые задачи
Используется Celery:
- отправка уведомлений подписчикам при обновлении курса;
- автоматическая деактивация пользователей, которые не заходили более 30 дней.

## 📖 Документация и запуск

👉 **[Перейти к руководству](docs/SETUP.md)**

## 📜 Лицензия

Проект распространяется под [лицензией MIT](LICENSE)
