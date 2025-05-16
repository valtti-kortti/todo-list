# TODO FastAPI Приложение

## 🚀 Запуск проекта

### 1. Настрой `.env` файл

Пример `.env`:

```env
APP_HOST_PORT=8000
POSTGRES_DB=postgres
POSTGRES_DB_USER=postgres
POSTGRES_DB_PASSWORD=12345
POSTGRES_DB_HOST_PORT=5438

BaseData=postgresql+asyncpg://postgres:12345@db:5432/postgres
```

---

### 2. Собери и запусти контейнеры

```bash
docker-compose up -d
```

---

### 3. Войти в контейнер приложения

```bash
docker exec -it my_project_app bash
```

---

### 4. Создай таблицы в базе данных

Внутри контейнера:

```bash
PYTHONPATH=. python -m database.init_db
```

---

## 🛠 Возможности

- Создание задачи
- Получение задач по имени/фамилии
- Получение всех задач
- Получение задачи по ID
- Обновление и удаление задач
