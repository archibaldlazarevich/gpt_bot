# GPT_test_bel_bot

## Описание

**GPT_test_bel_bot** — это телеграм бот, с помощью которого вы сможете использовать возможности ИИ по генерации изображений, аудио и текста.Основной функционал работает с API /pollinations.ai

---

## Установка

1. **Клонируйте репозиторий:**

    git clone https://github.com/archibaldlazarevich/gpt_bot.git


2. **Установите зависимости:**
    
    pip install poetry

    poetry install --no-root

3. **Настройте переменные окружения:**
  Создайте файл `.env` используя .env.template и добавьте токен бота и конфигурацию базы данных:
  ```
  BOT_TOKEN = ...
  POLLINATIONS_TOKEN = токен, который вы можете получить на pollinations.ai
  DATABASE_URL = ...(пример - "sqlite+aiosqlite:///base.db")

4. **Запустите :**
    
    python -m src.main
    
5. **Запуск через Docker**
    Для удобства можно использовать Docker. 
    Запуск:
    docker compose up --build
    Остановка:
    docker compose down


---

## Использование

### GPT_test_bel_bot

- `/start` — Запустить бота
- `/help` — Справка
- `/picture` — Генерация изображений с предварительным выбором разрешения изображения и модели для генерации
- далее в см. в коде 
---

## Архитектура

- При работе бот взаимодействует с API pollinations.ai при генерации данных.
- Для работы с данными используется SQlite(указать вашу БД: PostgreSQL, SQLite и т.д.).
- Взаимодействие с Telegram реализовано через библиотеку [aiogram](https://docs.aiogram.dev/).

---

## Требования

- Python 3.10+
- aiogram 3.x
- (другие зависимости — см. pyproject.toml)

---

## Авторы

- Артур Лазаревич [archibaldlazarevich](https://github.com/archibaldlazarevich)

- почта [compact_00@mail.ru](mailto:compact_00@mail.ru)
---

