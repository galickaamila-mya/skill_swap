# Skill Swap

**Skill Swap** — веб-платформа для бартерного обмена навыками между пользователями. Вы учите партнёра одному навыку — он учит вас другому. Без денег, через взаимный интерес и договорённости.

## Целевая аудитория

Студенты, фрилансеры и специалисты, которые хотят прокачать новые компетенции, обмениваясь знаниями с людьми с похожими интересами.

## Проблема

Курсы стоят дорого, а найти ментора по конкретному навыку сложно. Skill Swap решает это через систему взаимного матчинга, чат для переговоров, рейтинг исполнителей и историю завершённых сделок.

## Стек

- Django 6 + PostgreSQL
- Django REST Framework + Swagger (drf-spectacular)
- OAuth2 (Google) через django-allauth
- Redis (кэш + channel layer)
- Django Channels + WebSockets (чат переговоров)
- Docker + docker-compose
- pytest + GitHub Actions CI

## Локальный запуск

### 1. Подготовка окружения

```bash
cd skill_swap
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. PostgreSQL и Redis

Убедитесь, что PostgreSQL и Redis запущены локально (порты 5432 и 6379).
Создайте базу `skill_swap_db` или используйте значения по умолчанию из `settings.py`.

### 3. Миграции и данные

```bash
python manage.py migrate
python manage.py fill_db
```

Команда `fill_db` создаёт суперюзера `admin` / `Adminpass123!` и тестовые данные.

### 4. Запуск сервера

```bash
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

### 5. Docker

```bash
docker-compose up --build
```

### 6. Тесты

```bash
pytest
```

## OAuth2 (Google)

1. Откройте [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
2. Создайте **OAuth 2.0 Client ID** (тип: Web application)
3. В **Authorized redirect URIs** добавьте **оба** адреса (Google считает `localhost` и `127.0.0.1` разными):
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
   URI должен совпадать **символ в символ** (включая `http://`, порт `:8000` и слэш в конце).
4. Скопируйте **Client ID** и **Client Secret**
5. В Django Admin → **Social applications** → Add:
   - Provider: **Google**
   - Client id и Secret key — из Google Cloud
   - Sites: выберите сайт с ID=1

## API

- Swagger: http://127.0.0.1:8000/api/swagger/
- ReDoc: http://127.0.0.1:8000/api/redoc/

## Учётные записи (после fill_db)

| Роль | Логин | Пароль |
|------|-------|--------|
| Тестовый пользователь | `alice` | `Testpass123!` |
| Тестовый пользователь | `bob` | `Testpass123!` |

Суперюзер создаётся автоматически командой `fill_db` (и при `docker-compose up`).
