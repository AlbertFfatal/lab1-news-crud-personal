# Lab2 News API (with Auth)

FastAPI приложение для новостного портала с авторизацией.

Реализован CRUD для пользователей, новостей и комментариев + JWT авторизация (local и GitHub OAuth).

## API Endpoints

### Auth
- **POST** `/auth/register` — регистрация локальная, пароль в хэш
- **POST** `/auth/login` — логин локал для токенов
- **GET** `/auth/github/login` — вход через GitHub (redirect)
- **GET** `/auth/github/callback` — callback от GitHub (также дает токены)
- **POST** `/auth/refresh` — обновление access токена по refresh
- **POST** `/auth/logout` — выход
- **GET** `/auth/sessions` — список активных сессий

### Users
- **POST** `/users/` — создать пользователя (только админ/владелец)
- **GET** `/users/` — список пользователей (открыто)
- **GET** `/users/{user_id}` — получить пользователя (открыто)
- **PUT** `/users/{user_id}` — обновить пользователя (protected, владелец или admin)
- **DELETE** `/users/{user_id}` — удалить пользователя (protected, владелец или admin)
- **PATCH** `/users/{user_id}/role` — изменить роль (verified/admin) (protected, только admin)

### News
- **POST** `/news/` — создать новость (protected, только verified или admin)
- **GET** `/news/` — список новостей (открыто)
- **GET** `/news/{news_id}` — получить новость (открыто)
- **PUT** `/news/{news_id}` — обновить новость (protected, владелец или admin)
- **DELETE** `/news/{news_id}` — удалить новость (protected, владелец или admin)

### Comments
- **POST** `/comments/` — создать комментарий (protected, любой авторизованный)
- **GET** `/comments/` — список комментариев (открыто)
- **GET** `/comments/{comment_id}` — получить комментарий (открыто)
- **PUT** `/comments/{comment_id}` — обновить комментарий (protected, владелец или admin)
- **DELETE** `/comments/{comment_id}` — удалить комментарий (protected, владелец или admin)

## Модели данных

### User
- id (PK)
- name (str)
- email (str, unique)
- registration_date (datetime, auto)
- is_author_verified (bool, default=False)
- is_admin (bool, default=False)
- avatar (str, nullable — URL)
- password_hash (str, nullable — хэш для local auth)

### News
- id (PK)
- title (str)
- content (JSON)
- publication_date (datetime, auto)
- author_id (FK → User.id)
- cover (str, nullable — URL)

### Comment
- id (PK)
- text (str)
- news_id (FK → News.id)
- author_id (FK → User.id)
- publication_date (datetime, auto)

### RefreshSession
- id (PK)
- user_id (FK → User.id)
- refresh_token (str, unique)
- user_agent (str)
- created_at (datetime, auto)
- expires_at (datetime)

**Связи**: каскадное удаление (удаление пользователя или новости удаляет связанные комментарии).

## Запуск проекта

```
# 1. Создать .env в корне:
GITHUB_CLIENT_ID=github_client_id
GITHUB_CLIENT_SECRET=github_client_secret
JWT_SECRET_KEY=super_secret_change_in_prod
JWT_ALGORITHM=HS256

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Запуск PostgreSQL
docker-compose up -d

# 4. Применение миграций 
alembic upgrade head

# 5. Запуск сервера
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Документация API доступна по адресу: http://127.0.0.1:8000/docs

## Примеры использования (curl)
#  Регистрация (local)
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d "{\"name\": \"Test\", \"email\": \"test@example.com\", \"password\": \"test123\", \"is_author_verified\": true}"

# Логин (local)
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\"email\": \"test@example.com\", \"password\": \"test123\"}"

# Refresh
curl -X POST http://127.0.0.1:8000/auth/refresh -H "Content-Type: application/json" -d "{\"refresh_token\": \"real_refresh_token\"}"

# Logout
curl -X POST http://127.0.0.1:8000/auth/logout -H "Content-Type: application/json" -d "{\"refresh_token\": \"real_refresh_token\"}"

# Создать новость (verified)
curl -X POST http://127.0.0.1:8000/news/ -H "Content-Type: application/json" -H "Authorization: Bearer real_refresh_token" -d "{\"title\": \"Test\", \"content\": {\"text\": \"Hello\"}}"

# Попытка от не verified (403)
curl -X POST http://127.0.0.1:8000/news/ -H "Content-Type: application/json" -H "Authorization: Bearer токен_не verified" -d "{\"title\": \"No\"}"


# Результаты тестов и UI находятся в папке images 