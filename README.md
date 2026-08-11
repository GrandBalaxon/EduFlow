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

---

## Запуск проекта через Docker

### Настройка окружения

Создайте файл `.env.docker` по примеру `.env.sample`.

Заполните переменные:
- Django;
- PostgreSQL;
- Stripe;
- Celery/Redis;
- SMTP.

---

# Запуск контейнеров

```bash
docker compose up --build
```

Docker Compose автоматически поднимет:

- PostgreSQL;
- Redis;
- Django приложение;
- миграции базы данных;
- Celery worker;
- Celery Beat.

---

## Сервисы Docker Compose

### db

PostgreSQL 16.

Использует Docker volume `postgres_data`.

### migrate

Выполняет миграции:

```bash
python manage.py migrate
```

### redis

Используется как брокер сообщений и backend результатов Celery.

### web

Django приложение:

```bash
python manage.py runserver 0.0.0.0:8000
```

Доступно:

```text
http://localhost:8000/
```

### celery_worker

Запуск:

```bash
celery -A config worker --loglevel=info -P eventlet
```

### celery_beat

Запуск:

```bash
celery -A config beat -l info
```

---

# Dockerfile

Проект использует multi-stage сборку.

Builder stage:
- Python 3.14 slim;
- установка зависимостей через Poetry;
- исключение dev и lint зависимостей.

Final stage:
- копирование зависимостей;
- копирование исходного кода;
- запуск Django приложения.

---

# API документация

Swagger:

```text
http://localhost:8000/api/docs/
```

OpenAPI схема:

```text
http://localhost:8000/api/schema/
```

---

## Основные API разделы

### Пользователи

```text
/user/
```

Включает:
- регистрацию;
- профиль пользователя;
- обновление данных;
- удаление аккаунта;
- платежи.

### Курсы

```text
/course/
```

Включает:
- управление курсами;
- уроки;
- подписки;
- оплату.

---

## Локальный запуск без Docker

Установка зависимостей:

```bash
poetry install
```

Миграции:

```bash
python manage.py migrate
```

Создание администратора:

```bash
python manage.py createsuperuser
```

Запуск сервера:

```bash
python manage.py runserver
```

Celery worker:

```bash
celery -A config worker -l info -P eventlet
```

Celery Beat:

```bash
celery -A config beat -l info
```

---

## 📜 Лицензия

Этот проект распространяется под лицензией MIT.