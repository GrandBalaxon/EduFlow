# 🛠️ Руководство по установке и запуску

В этом руководстве описаны настройка EduFlow, запуск через Docker или Poetry.

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
