## API Endpoints

###  Users
- **POST** `/users/` — создать пользователя
- **GET** `/users/` — список пользователей
- **GET** `/users/{user_id}` — получить пользователя
- **PUT** `/users/{user_id}` — обновить пользователя
- **DELETE** `/users/{user_id}` — удалить пользователя

### News
- **POST** `/news/` — создать новость (только для авторов)
- **GET** `/news/` — список новостей
- **GET** `/news/{news_id}` — получить новость
- **PUT** `/news/{news_id}` — обновить новость
- **DELETE** `/news/{news_id}` — удалить новость (с каскадным удалением комментариев)

### Comments
- **POST** `/comments/` — создать комментарий
- **GET** `/comments/` — список комментариев
- **GET** `/comments/{comment_id}` — получить комментарий
- **PUT** `/comments/{comment_id}` — обновить комментарий
- **DELETE** `/comments/{comment_id}` — удалить комментарий

## Модели данных

### User
- id (PK)
- name (str)
- email (str, unique)
- registration_date (datetime, auto)
- is_author_verified (bool, default=False)
- avatar (str, nullable — URL)

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

**Связи**: каскадное удаление (удаление пользователя или новости удаляет связанные комментарии).

## Запуск проекта

```bash
# 1. Запуск PostgreSQL
docker-compose up -d

# 2. Применение миграций (таблицы + мок-данные)
alembic upgrade head

# 3. Запуск сервера
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Документация API доступна по адресу: http://127.0.0.1:8000/docs

## Примеры использования (curl)
Результаты тестов, также как и UI находятся в папке с изображениями
```cmd
# Список пользователей (мок-данные)
curl http://127.0.0.1:8000/users/

# Создать пользователя
curl -X POST http://127.0.0.1:8000/users/ -H "Content-Type: application/json" -d "{\"name\": \"Test User\", \"email\": \"test@example.com\"}"

# Создать новость (от verified author_id=1)
curl -X POST http://127.0.0.1:8000/news/ -H "Content-Type: application/json" -d "{\"title\": \"Test News\", \"content\": {\"text\": \"Hello\"}, \"author_id\": 1}"

# Попытка создания новости от неverified (403)
curl -X POST http://127.0.0.1:8000/news/ -H "Content-Type: application/json" -d "{\"title\": \"Forbidden\", \"content\": {\"text\": \"No\"}, \"author_id\": 2}"

