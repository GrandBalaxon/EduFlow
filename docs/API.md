<div align="center">

# 🔌 Справочник API EduFlow

**Все эндпоинты, права доступа и примеры запросов в одном месте**

[← На главную](../README.md) · [Установка](SETUP.md) · [Swagger UI](http://localhost/api/docs/)

</div>

---

## 🌐 Базовые сведения

| Параметр | Значение |
|:--|:--|
| Базовый адрес (Docker) | `http://localhost/` |
| Базовый адрес (локально) | `http://localhost:8000/` |
| Формат | JSON (`application/json`) |
| Авторизация | `Authorization: Bearer <access_token>` |
| Пагинация | `?page=2&page_size=20` (по умолчанию 10, максимум 100) |

Интерактивная документация с возможностью отправлять запросы — **Swagger UI** на `/api/docs/`.
Машиночитаемая схема — `/api/schema/`.

---

## 🔑 Авторизация

Токены выдаёт SimpleJWT. Access-токен живёт **15 минут**, refresh — **1 день**.

| Метод | Эндпоинт | Доступ | Описание |
|:--|:--|:--|:--|
| `POST` | `/token/` | все | получить пару access + refresh |
| `POST` | `/token/refresh/` | все | обновить access-токен |

```bash
curl -X POST http://localhost/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secret"}'
```

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

Обновление access-токена:

```bash
curl -X POST http://localhost/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

---

## 👤 Пользователи — `/user/`

| Метод | Эндпоинт | Доступ | Описание |
|:--|:--|:--|:--|
| `POST` | `/user/create/` | все | регистрация нового пользователя |
| `GET` | `/user/{id}/` | авторизованные | профиль (свой — полностью, чужой — публично) |
| `PATCH` | `/user/{id}/update/` | только владелец | изменить профиль |
| `DELETE` | `/user/{id}/delete/` | только владелец | удалить аккаунт |
| `GET` | `/user/payments/` | авторизованные | свои платежи |
| `GET` | `/user/payments/{id}/status/` | авторизованные | проверить статус платежа в Stripe |

### Регистрация

```bash
curl -X POST http://localhost/user/create/ \
  -H "Content-Type: application/json" \
  -d '{
        "email": "student@example.com",
        "password": "StrongPass123",
        "phone_number": "+79001234567",
        "city": "Москва"
      }'
```

Обязательные поля — `email` и `password`. Логин выполняется по email, отдельного username нет.

### Профиль

Свой профиль возвращается с историей платежей:

```json
{
  "email": "student@example.com",
  "phone_number": "+79001234567",
  "city": "Москва",
  "avatar": null,
  "payments": [
    { "id": 1, "amount": "1990.00", "method": "stripe", "is_paid": true }
  ]
}
```

Чужой профиль — только `id`, `email`, `phone_number`, `city`, `avatar`.

### Список платежей с фильтрами

```bash
# фильтр по методу оплаты и сортировка по дате
curl "http://localhost/user/payments/?method=stripe&ordering=-date" \
  -H "Authorization: Bearer <access_token>"
```

Поддерживаемые фильтры: `method`, `course`, `lesson`. Сортировка: `ordering=date` / `-date`.

---

## 📖 Курсы — `/course/`

Полный CRUD на `ModelViewSet`. По умолчанию доступны `list`, `create`, `retrieve`,
`update`, `partial_update`, `destroy`.

| Метод | Эндпоинт | Доступ | Описание |
|:--|:--|:--|:--|
| `GET` | `/course/` | авторизованные | список курсов (с пагинацией) |
| `POST` | `/course/` | пользователь | создать курс |
| `GET` | `/course/{id}/` | владелец или модератор | детали курса |
| `PUT` / `PATCH` | `/course/{id}/` | владелец или модератор | обновить курс |
| `DELETE` | `/course/{id}/` | только владелец | удалить курс |

> 👀 Пользователь видит **только свои** курсы, модератор — **все** курсы платформы.

### Создание курса

```bash
curl -X POST http://localhost/course/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Django для начинающих",
        "description": "Базовый курс по Django REST Framework",
        "price": 4990
      }'
```

Владелец проставляется автоматически из токена — передавать `owner` не нужно.

### Структура ответа

```json
{
  "id": 1,
  "title": "Django для начинающих",
  "description": "Базовый курс по Django REST Framework",
  "preview_image": null,
  "price": 4990,
  "owner": 1,
  "lessons_count": 3,
  "is_subscribed": false,
  "lessons": []
}
```

Поля `lessons_count`, `lessons` и `is_subscribed` вычисляются автоматически.

---

## 📝 Уроки — `/course/{course_id}/lesson/`

| Метод | Эндпоинт | Доступ | Описание |
|:--|:--|:--|:--|
| `GET` | `/course/{course_id}/lesson/` | владелец курса или модератор | список уроков курса |
| `POST` | `/course/{course_id}/lesson/create/` | только владелец курса | добавить урок |
| `GET` | `/course/{course_id}/lesson/{id}/` | владелец урока или модератор | детали урока |
| `PUT` / `PATCH` | `/course/{course_id}/lesson/{id}/update/` | владелец урока или модератор | обновить урок |
| `DELETE` | `/course/{course_id}/lesson/{id}/delete/` | только владелец урока | удалить урок |

### Создание урока

```bash
curl -X POST http://localhost/course/1/lesson/create/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Первый эндпоинт",
        "description": "Пишем простой APIView",
        "video_link": "https://www.youtube.com/watch?v=example",
        "price": 990
      }'
```

> ⚠️ `video_link` принимает ссылки **только с YouTube** — остальные домены отклоняются
> валидатором с ошибкой `400`.

Добавлять уроки в курс может только его владелец (модератор — нет).

---

## 🔔 Подписки — `/course/{course_id}/subscription/`

| Метод | Эндпоинт | Доступ | Описание |
|:--|:--|:--|:--|
| `POST` | `/course/{course_id}/subscription/` | авторизованные | переключить подписку |

Тело запроса не требуется. Логика одного эндпоинта:

| Было | Стало |
|:--|:--|
| подписки нет | создаётся активная подписка |
| подписка активна | деактивируется (отписка) |
| подписка отключена | снова активируется |

```bash
curl -X POST http://localhost/course/1/subscription/ \
  -H "Authorization: Bearer <access_token>"
```

```json
{ "message": "Подписка отключена", "is_active": false }
```

Подписчики получают письмо, когда владелец обновляет курс или его уроки.
Не чаще одного письма на курс в 4 часа.

---

## 💳 Платежи — `/course/{course_id}/payment/`

| Метод | Эндпоинт | Доступ | Описание |
|:--|:--|:--|:--|
| `POST` | `/course/{course_id}/payment/` | авторизованные | оплатить курс |
| `POST` | `/course/{course_id}/lesson/{id}/payment/` | авторизованные | оплатить отдельный урок |

Оплата идёт через Stripe Checkout — в ответе возвращается ссылка на страницу оплаты.
Сумма берётся из `price` курса или урока, передавать её в запросе не нужно.

```bash
curl -X POST http://localhost/course/1/payment/ \
  -H "Authorization: Bearer <access_token>"
```

```json
{
  "id": 1,
  "user": 1,
  "date": "2026-11-12",
  "course": 1,
  "lesson": null,
  "amount": "4990.00",
  "method": "stripe",
  "stripe_session_id": "cs_test_a1...",
  "stripe_payment_url": "https://checkout.stripe.com/c/pay/cs_test_a1...",
  "is_paid": false
}
```

### Проверка оплаты

После возврата со страницы Stripe статус обновляется запросом:

```bash
curl http://localhost/user/payments/1/status/ \
  -H "Authorization: Bearer <access_token>"
```

Сервис сам спросит Stripe о статусе сессии и обновит поле `is_paid`.

---

## 🚦 Коды ответов

| Код | Когда возвращается |
|:--|:--|
| `200 OK` | успешный GET / PUT / PATCH |
| `201 Created` | объект создан |
| `204 No Content` | объект удалён |
| `400 Bad Request` | ошибка валидации или нет сессии Stripe |
| `401 Unauthorized` | нет токена или он просрочен |
| `403 Forbidden` | недостаточно прав (например, модератор пытается создать курс) |
| `404 Not Found` | объект не найден |
| `502 Bad Gateway` | ошибка на стороне Stripe |

Пример ошибки валидации:

```json
{
  "video_link": ["video_link должен содержать ссылку только на youtube.com"]
}
```

---

## 🧭 Сводная карта маршрутов

```text
/                                   → API
├── token/                          → JWT: получить пару токенов
├── token/refresh/                  → JWT: обновить access
├── admin/                          → Django Admin
├── api/docs/                       → Swagger UI
├── api/schema/                     → OpenAPI-схема
├── user/
│   ├── create/                     → регистрация
│   ├── {id}/                       → профиль
│   ├── {id}/update/                → изменить профиль
│   ├── {id}/delete/                → удалить аккаунт
│   ├── payments/                   → свои платежи
│   └── payments/{id}/status/       → статус платежа
└── course/
    ├── /                           → список / создание курсов
    ├── {id}/                       → детали / обновление / удаление
    ├── {id}/lesson/                → уроки курса
    ├── {id}/lesson/create/         → создать урок
    ├── {id}/lesson/{lid}/          → детали урока
    ├── {id}/lesson/{lid}/update/   → обновить урок
    ├── {id}/lesson/{lid}/delete/   → удалить урок
    ├── {id}/subscription/          → подписка / отписка
    ├── {id}/payment/               → оплата курса
    └── {id}/lesson/{lid}/payment/  → оплата урока
```

---

<div align="center">

[← На главную](../README.md) · [Установка →](SETUP.md)

</div>
