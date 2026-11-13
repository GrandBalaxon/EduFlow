<img src="docs/assets/banner.png" alt="EduFlow — образовательная платформа на Django REST Framework" width="100%">

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

---

## 📚 О проекте

**EduFlow** — бэкенд образовательной платформы, где авторы публикуют курсы и уроки, а студенты
покупают их и подписываются на обновления.

Сервис отдаёт JSON API поверх Django REST Framework: регистрация и JWT-авторизация, разграничение
доступа по ролям, оплата курсов и отдельных уроков через Stripe, фоновые задачи на Celery.
Всё упаковано в Docker Compose и поднимается одной командой.

---

## ✨ Возможности

<table>
<tr>
<td width="50%" valign="top">

### 👤 Пользователи
- Регистрация по email
- Авторизация по JWT (access + refresh)
- Свой профиль с полными данными
- Публичные профили других студентов
- Загрузка аватара, телефон, город
- История платежей

### 📖 Курсы и уроки
- Полный CRUD для курсов и уроков
- Превью-картинки и ссылки на видео
- Цена курса и цена отдельного урока
- Пагинация и фильтрация списков
- Уроки привязаны к курсу

</td>
<td width="50%" valign="top">

### 🔔 Подписки
- Подписка на курс в один запрос
- Повторный запрос переключает статус
- Уведомление подписчикам при обновлении курса
- Защита от спама: не чаще одного письма в 4 часа

### 💳 Платежи
- Оплата курса или одного урока
- Оплата через Stripe Checkout
- Ссылка на оплату в ответе API
- Проверка статуса платежа по сессии
- Хранение суммы, даты и метода оплаты

### ⚙️ Фоновые задачи
- Напоминания об обновлении курсов
- Автодеактивация «спящих» аккаунтов (30 дней)
- Планировщик на django-celery-beat

</td>
</tr>
</table>

---

## 🛡️ Роли и доступ

| Роль | Как получается | Что может |
|:--|:--|:--|
| **Гость** | без токена | зарегистрироваться, получить токен, открыть Swagger |
| **Пользователь** | регистрация | создавать свои курсы и уроки, покупать чужое, подписываться |
| **Владелец** | создал объект | редактировать и удалять только свои курсы и уроки |
| **Модератор** | группа `Moderator` | видеть и редактировать всё, но **не** создавать и **не** удалять контент |
| **Админ** | `createsuperuser` | доступ в Django Admin, полные права |

---

## 🧰 Технологии

| Слой | Технологии |
|:--|:--|
| **Язык и фреймворк** | Python 3.14, Django 6.0, Django REST Framework 3.17 |
| **База данных** | PostgreSQL 16 (`psycopg2-binary`) |
| **Авторизация** | SimpleJWT — access-токен 15 минут, refresh — 1 день |
| **Документация API** | drf-spectacular → OpenAPI 3 + Swagger UI |
| **Платежи** | Stripe Checkout |
| **Фоновые задачи** | Celery 5.6, Redis 7 (брокер и backend), django-celery-beat |
| **Инфраструктура** | Docker, Docker Compose, Gunicorn, Nginx |
| **Зависимости** | Poetry 2.x |
| **Качество кода** | flake8 (120 символов), coverage, GitHub Actions |

---

## 🚀 Быстрый старт

Нужны только [Docker](https://docs.docker.com/get-docker/) и Docker Compose.

```bash
# 1. Клонируем репозиторий
git clone https://github.com/GrandBalaxon/EduFlow.git
cd EduFlow

# 2. Готовим переменные окружения
cp .env.sample .env.docker   # и заполняем значения

# 3. Поднимаем всё одной командой
docker compose up --build
```

Готово — API доступен по адресам:

| Что | Адрес |
|:--|:--|
| 🌐 API через Nginx | http://localhost/ |
| 📘 Swagger UI | http://localhost/api/docs/ |
| 🧾 OpenAPI-схема | http://localhost/api/schema/ |
| 🛠️ Django Admin | http://localhost/admin/ |

<br>

<details>
<summary><b>🍃 Запуск без Docker (локально через Poetry)</b></summary>

<br>

```bash
poetry install
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
poetry run python manage.py runserver
```

Celery (в двух отдельных терминалах):

```bash
poetry run celery -A config worker -l info -P eventlet
poetry run celery -A config beat -l info
```

Подробнее — в [руководстве по установке](docs/SETUP.md).

</details>

> ⚠️ **Минимум для запуска:** `SECRET_KEY`, `DEBUG` и данные PostgreSQL.
> Ключи Stripe и настройки почты нужны только для оплаты и писем.
> Полный список переменных — в [`.env.sample`](.env.sample) и [руководстве по установке](docs/SETUP.md).

---

## 🔌 API за минуту

Все запросы к `/course/` и `/user/` требуют заголовок `Authorization: Bearer <access_token>`.

```bash
# Получаем токен
curl -X POST http://localhost/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'

# Список своих курсов
curl http://localhost/course/ -H "Authorization: Bearer <access_token>"

# Подписка на курс (повторный запрос — отписка)
curl -X POST http://localhost/course/1/subscription/ \
  -H "Authorization: Bearer <access_token>"

# Оплата курса — в ответ придёт ссылка на Stripe
curl -X POST http://localhost/course/1/payment/ \
  -H "Authorization: Bearer <access_token>"
```

| Группа | Префикс | Что внутри |
|:--|:--|:--|
| 👤 Пользователи | `/user/` | регистрация, профиль, удаление, платежи |
| 📖 Курсы | `/course/` | CRUD курсов, уроки, подписка, оплата |
| 🔑 Авторизация | `/token/` | получение и обновление JWT |
| 📘 Документация | `/api/docs/` | Swagger UI |

Полное описание эндпоинтов с примерами — в **[справочнике API](docs/API.md)**.

---

## 🧪 Тесты и CI

```bash
# запуск тестов локально
poetry run coverage run manage.py test
poetry run coverage report -m
```

Проверки в GitHub Actions (`.github/workflows/ci.yml`):

| Шаг | Что проверяет |
|:--|:--|
| 🧹 **lint** | стиль кода через flake8 |
| ✅ **checks** | `manage.py check` и отсутствие незакоммиченных миграций |
| 🧪 **test** | тесты API с отчётом покрытия |
| 🐳 **build** | сборка всех Docker-образов |
| 🚀 **deploy** | выкладка на сервер при пуше в `main` |

---

## 📜 Лицензия

Проект распространяется под [лицензией MIT](LICENSE)
