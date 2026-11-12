<div align="center">

# 🛠️ Установка и запуск EduFlow

**Пошаговое руководство: от клонирования репозитория до первого запроса к API**

[← На главную](../README.md) · [Справочник API](API.md)

</div>

---

## 📋 Что понадобится

| Инструмент | Версия | Зачем |
|:--|:--|:--|
| [Docker](https://docs.docker.com/get-docker/) + Docker Compose | любая актуальная | рекомендуемый способ запуска |
| [Python](https://www.python.org/downloads/) | 3.14 | если запускаете без Docker |
| [Poetry](https://python-poetry.org/docs/#installation) | 2.x | управление зависимостями |
| [Git](https://git-scm.com) | — | клонирование репозитория |
| Аккаунт [Stripe](https://stripe.com) | test-режим | для проверки оплаты |

> 💡 Достаточно Docker — остальное нужно только для локального запуска без контейнеров.

---

## 🐳 Способ 1. Docker Compose (рекомендуется)

### Шаг 1. Клонируйте репозиторий

```bash
git clone https://github.com/GrandBalaxon/EduFlow.git
cd EduFlow
```

### Шаг 2. Заполните переменные окружения

```bash
cp .env.sample .env.docker
```

Откройте `.env.docker` и заполните значения — для первого запуска обязательны:

| Переменная | Пример | Комментарий |
|:--|:--|:--|
| `DEBUG` | `True` | `True` для локальной разработки |
| `SECRET_KEY` | `django-insecure-...` | любой длинный набор символов |
| `POSTGRES_DB` | `eduflow` | имя базы |
| `POSTGRES_USER` | `eduflow` | пользователь базы |
| `POSTGRES_PASSWORD` | `eduflow` | пароль базы |

Те же значения продублируйте в блоке `DATABASE_*`, потому что Django читает их отдельно:

```env
DATABASE_NAME=eduflow
DATABASE_USER=eduflow
DATABASE_PASSWORD=eduflow
DATABASE_HOST=db
DATABASE_PORT=5432
```

Ключи Stripe и настройки почты можно добавить позже — без них приложение запустится,
не будут работать только оплата и письма:

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

<details>
<summary><b>📮 Куда вписать остальные переменные</b></summary>

<br>

| Переменная | Что это |
|:--|:--|
| `DATABASE_HOST` | внутри Docker — имя сервиса `db`, локально — `localhost` |
| `CELERY_BROKER_URL` / `CELERY_RESULT_BACKEND` | Redis; в Docker — `redis://redis:6379/0` |
| `EMAIL_HOST`, `EMAIL_PORT` | SMTP-сервер для уведомлений |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | логин и пароль приложения почты |

Полный список — в файле [`.env.sample`](../.env.sample).

</details>

### Шаг 3. Запустите контейнеры

```bash
docker compose up --build
```

Первый запуск занимает несколько минут: собираются образы и применяются миграции.
Когда в логах появится `Listening at: http://0.0.0.0:8000` — всё готово.

### Шаг 4. Проверьте, что всё работает

| Сервис | Адрес |
|:--|:--|
| 🌐 API (через Nginx) | http://localhost/ |
| 📘 Swagger UI | http://localhost/api/docs/ |
| 🧾 OpenAPI-схема | http://localhost/api/schema/ |
| 🛠️ Django Admin | http://localhost/admin/ |

### Шаг 5. Создайте администратора

```bash
docker compose exec web python manage.py createsuperuser
```

Учётная запись создаётся по email. После этого можно войти в Django Admin
и, например, создать группу `Moderator` для модераторов.

---

## 🍃 Способ 2. Локально без Docker

Понадобятся Python 3.14, Poetry и запущенный PostgreSQL.

### Шаг 1. Установите зависимости

```bash
git clone https://github.com/GrandBalaxon/EduFlow.git
cd EduFlow
poetry install
```

### Шаг 2. Подготовьте `.env`

```bash
cp .env.sample .env
```

Заполните те же переменные, что и для Docker, но с локальными адресами:

```env
DEBUG=True
DATABASE_HOST=localhost
DATABASE_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

> Не забудьте заранее создать базу в PostgreSQL — `createdb eduflow`.

### Шаг 3. Примените миграции и создайте админа

```bash
poetry run python manage.py migrate
poetry run python manage.py createsuperuser
```

### Шаг 4. Запустите сервер

```bash
poetry run python manage.py runserver
```

API будет доступен на http://localhost:8000/ (в этом режиме Nginx не используется).
Swagger — http://localhost:8000/api/docs/.

### Шаг 5. Запустите Celery (по желанию)

Фоновые задачи нужны для уведомлений и деактивации аккаунтов.
Redis должен быть запущен: `docker run -d -p 6379:6379 redis:7-alpine`.

```bash
# воркер — в одном терминале
poetry run celery -A config worker -l info -P eventlet

# планировщик периодических задач — в другом
poetry run celery -A config beat -l info
```

---

## 🧩 Из чего состоит Docker Compose

`docker compose up` поднимает семь сервисов:

| Сервис | Роль |
|:--|:--|
| `db` | PostgreSQL 16, данные в volume `postgres_data` |
| `redis` | брокер сообщений и хранилище результатов Celery |
| `migrate` | одноразовый контейнер: применяет миграции перед стартом |
| `web` | Django под Gunicorn, статика собирается в `static_volume` |
| `celery_worker` | выполняет фоновые задачи |
| `celery_beat` | расписание периодических задач |
| `nginx` | принимает запросы на порту 80 и раздаёт статику |

Полезные команды:

```bash
docker compose up -d          # запуск в фоне
docker compose logs -f web    # смотреть логи приложения
docker compose exec web python manage.py shell
docker compose down           # остановить
docker compose down -v        # остановить и удалить данные БД
```

---

## 🧪 Тесты

```bash
# через Docker
docker compose exec web python manage.py test

# локально
poetry run coverage run manage.py test
poetry run coverage report -m
```

Тесты используют отдельные настройки `config/settings_ci.py`: SQLite в памяти,
Celery в eager-режиме и заглушка Stripe — внешние сервисы не нужны.

---

## 🆘 Частые проблемы

<details>
<summary><b>Порт 80 уже занят</b></summary>

<br>

Остановите сервис, который слушает порт 80, или измените порт Nginx в `docker-compose.yml`:

```yaml
nginx:
  ports:
    - "8080:80"
```

Тогда API будет доступен на http://localhost:8080/.

</details>

<details>
<summary><b>Контейнер `web` падает с ошибкой подключения к базе</b></summary>

<br>

Проверьте, что `POSTGRES_*` и `DATABASE_*` в `.env.docker` совпадают,
а `DATABASE_HOST` равен `db` (именно имя сервиса, не `localhost`).

Если база уже была создана со старым паролем, пересоздайте volume: `docker compose down -v`.

</details>

<details>
<summary><b>Не приходят письма об обновлении курса</b></summary>

<br>

1. Проверьте блок `EMAIL_*` в `.env.docker` — используются SSL-соединения.
2. Убедитесь, что запущены `celery_worker` и `celery_beat`.
3. Уведомление отправляется не чаще одного раза в 4 часа на курс — это защита от спама.

</details>

<details>
<summary><b>Stripe возвращает ошибку при оплате</b></summary>

<br>

Убедитесь, что `STRIPE_SECRET_KEY` — это тестовый ключ из личного кабинета Stripe,
и что аккаунт не заблокирован. Ссылки `success_url` и `cancel_url` ведут на локальный адрес,
поэтому в продакшене их нужно заменить.

</details>

---

<div align="center">

[← На главную](../README.md) · [Справочник API →](API.md)

</div>
