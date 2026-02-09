# Ролевая модель авторизации

### Роли пользователей
- **User**:
  - Может читать users, news, comments.
  - Может создавать комментарии.
  - Может редактировать/удалять свои комментарии.

- **Verified Author**:
  - Все права User.
  - Может создавать новости.
  - Может редактировать/удалять свои новости (и комментарии к ним каскадно).

- **Admin**:
  - Все права Verified Author.
  - Может редактировать/удалять любые новости и комментарии.
  - Может назначать роли (verified/author, admin) другим пользователям.

### Авторизация
- JWT Bearer токен в Authorization header для защищенных ручек.
- Access токен (короткий срок).
- Refresh токен (длинный срок, хранится в БД с user_agent).
- Local login/register (пароль хэшируется argon2).
- GitHub OAuth (SSO через fastapi_sso).

### Защищенные ручки
- Создание/обновление/удаление — требуют JWT.
- Чтение — открыто.
- Создание новости — verified or admin.
- Редактирование/удаление материала — владелец or admin.

### Ручки auth
- /auth/register — регистрация (local).
- /auth/login — логин (local).
- /auth/github/login — GitHub OAuth.
- /auth/refresh — новый access токен.
- /auth/logout — инвалидация refresh.
- /auth/sessions — список активных сессий.