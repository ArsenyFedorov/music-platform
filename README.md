# 🎵 Music Platform

REST API для музыкальной платформы

---

## 📌 Возможности

- Создание, получение и удаление артистов
- Подписка и отписка от артистов
- Подсчёт количества подписчиков
- Валидация данных через Pydantic
- Асинхронная работа с БД (asyncpg)
- Миграции через Alembic
- Запуск через Docker Compose

---

## 🛠 Стек

| Компонент | Технология |
|-----------|------------|
| Язык | Python 3.13 |
| Веб-фреймворк | FastAPI |
| ORM | SQLAlchemy 2.x (async) |
| Драйвер БД | asyncpg |
| БД | PostgreSQL |
| Миграции | Alembic |
| Настройки | pydantic-settings |
| Контейнеризация | Docker, Docker Compose |
| Менеджер зависимостей | uv |

---

## 📁 Структура проекта

```
music-platform/
├── app/
│   ├── main.py                 # точка входа FastAPI
│   ├── core/                   # настройки, общие утилиты
│   │   ├── config.py
│   │   └── database.py         # engine, SessionLocal, get_db_session
│   ├── modules/
│   │   ├── artist/
│   │   │   ├── models.py       # Artist, ArtistFollower
│   │   │   ├── schemas.py      # Pydantic-схемы
│   │   │   ├── repository.py   # работа с БД
│   │   │   ├── service.py      # бизнес-логика
│   │   │   ├── routers.py      # эндпоинты
│   │   │   ├── exceptions.py   # доменные исключения
│   │   │   └── dependencies.py # DI-провайдеры
│   │   └── user/
│   │       └── ...
│   └── shared/                 # общие исключения, хендлеры
├── alembic/                    # миграции
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
└── README.md
```

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ArsenyFedorov/music-platform.git
cd music-platform
```

### 2. Создать `.env`

Скопируйте пример и подставьте свои значения:

```bash
cp .env.example .env
```

Пример содержимого `.env`:

```dotenv
# --- PostgreSQL ---
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=music_platform
POSTGRES_HOST=db
POSTGRES_PORT=5432

# --- Приложение ---
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/music_platform
APP_ENV=local
DEBUG=true
```

> ⚠️ Не коммитьте `.env` в репозиторий — он должен быть в `.gitignore`.

### 3. Запустить через Docker Compose

```bash
docker compose up --build
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

### 4. Применить миграции

```bash
docker compose exec api alembic upgrade head
```

### 5. Открыть документацию

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 💻 Локальный запуск (без Docker)

Требуется Python 3.13 и запущенный PostgreSQL.

```bash
# Установить uv (если ещё нет)
pip install uv

# Установить зависимости
uv sync

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

---

## 🔌 API

Базовый префикс: `/` (проверьте у себя — возможно, `/api/v1`).

### Артисты

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| `POST` | `/artists` | Создать артиста |
| `GET` | `/artists` | Список артистов |
| `GET` | `/artists/{artist_id}` | Получить артиста по ID |
| `DELETE` | `/artists/{artist_id}` | Удалить артиста |
| `POST` | `/artists/{artist_id}/follow` | Подписаться на артиста |
| `DELETE` | `/artists/{artist_id}/follow` | Отписаться от артиста |

### Примеры запросов

**Создать артиста**

```bash
curl -X POST http://localhost:8000/artists \
  -H "Content-Type: application/json" \
  -d '{"name": "Radiohead", "description": "British rock band"}'
```

**Получить список артистов**

```bash
curl "http://localhost:8000/artists?limit=10&offset=0"
```

**Подписаться на артиста**

```bash
curl -X POST http://localhost:8000/artists/{artist_id}/follow \
  -H "user_id: <uuid>"
```

> Проверьте фактические имена параметров и заголовков в `routers.py`.

### Коды ответов

| Код | Значение |
|-----|----------|
| `200` | Успех |
| `201` | Ресурс создан |
| `400` | Неверные данные |
| `404` | Ресурс не найден |
| `409` | Конфликт (дубликат) |
| `500` | Внутренняя ошибка сервера |

---

## 🗄 Миграции

Создать новую миграцию:

```bash
alembic revision --autogenerate -m "add new table"
```

Применить миграции:

```bash
alembic upgrade head
```

Откатить последнюю:

```bash
alembic downgrade -1
```

---

## 🧪 Тесты

```bash
uv run pytest
```

С покрытием:

```bash
uv run pytest --cov=app
```

> Если тесты ещё не добавлены — этот раздел можно оставить как план развития.

---

## 🧹 Линтеры и форматтеры

```bash
uv run ruff check .
uv run ruff format .
```

---

## 🐳 Docker

Пересобрать образ:

```bash
docker compose build --no-cache
```

Посмотреть логи:

```bash
docker compose logs -f api
```

Остановить:

```bash
docker compose down
```

Удалить с томами:

```bash
docker compose down -v
```

---

## 🗺 Roadmap

- [ ] Аутентификация и авторизация (JWT)
- [ ] Роли пользователей (админ / слушатель)
- [ ] Треки и альбомы
- [ ] Поиск и фильтрация артистов
- [ ] Пагинация с курсором
- [ ] Кэширование (Redis)
- [ ] Тесты (pytest + httpx)
- [ ] CI/CD через GitHub Actions

---

## 🤝 Вклад

Pull requests приветствуются. Для крупных изменений сначала откройте issue.

1. Форкните репозиторий
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m "Add amazing feature"`)
4. Запушьте (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## 📄 Лицензия

MIT — см. файл `LICENSE` (добавьте, если ещё нет).

---

## 👤 Автор

**Арсений Фёдоров**
- GitHub: [@ArsenyFedorov](https://github.com/ArsenyFedorov)