# 🎓 EduFlow Django REST API

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Django](https://img.shields.io/badge/django-6.0-green.svg)
![DRF](https://img.shields.io/badge/django%20rest%20framework-3.17-red.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-16-blue.svg)
![Poetry](https://img.shields.io/badge/dependency%20manager-poetry-blue.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)
![Celery](https://img.shields.io/badge/celery-5.6-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

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
