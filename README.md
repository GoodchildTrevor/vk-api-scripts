# vk-api-scripts

Сборник скриптов для работы с API VK — FastAPI REST обёртка + MCP сервер.

## Структура проекта

```
vk-api-scripts/
├── app/
│   ├── main.py           # FastAPI приложение
│   ├── config.py         # pydantic-settings (VK_TOKEN, VK_API_VERSION, …)
│   ├── routers/
│   │   ├── wall.py       # GET /vk/wall/{domain}
│   │   ├── groups.py     # GET /vk/groups/{group_id}
│   │   └── files.py      # GET /vk/files/{domain}
│   ├── schemas/          # Pydantic-модели ответов
│   └── services/
│       └── vk.py         # Вся бизнес-логика (async httpx)
├── mcp_server.py         # MCP сервер для AI-агентов
├── pyproject.toml
├── consts.py             # (legacy) константы
├── group_info.py         # (legacy) скрипт получения ID группы
├── group_posts.py        # (legacy) скрипт получения постов
└── file_tags.py          # (legacy) скрипт получения файлов
```

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install .
```

### 2. Конфигурация

Создайте файл `.env` в корне проекта:

```env
VK_TOKEN=ваш_токен_vk
VK_API_VERSION=5.199
```

### 3. Запуск REST API

```bash
uvicorn app.main:app --reload
```

API будет доступен по адресу `http://localhost:8000`.
Документация Swagger: `http://localhost:8000/docs`.

### Эндпоинты

| Метод | Путь                    | Описание                          |
| ----- | ----------------------- | --------------------------------- |
| GET   | `/vk/wall/{domain}`     | Текстовые посты со стены группы   |
| GET   | `/vk/groups/{group_id}` | Информация о группе               |
| GET   | `/vk/files/{domain}`    | Документы (файлы) с тегами        |
| GET   | `/health`               | Проверка работоспособности        |

### 4. Запуск MCP сервера

Для использования с Claude Desktop или другими AI-агентами:

```bash
python mcp_server.py
```

Или добавьте в `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vk-api": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": { "VK_TOKEN": "ваш_токен" }
    }
  }
}
```

### MCP инструменты

| Инструмент            | Описание                                  |
| --------------------- | ----------------------------------------- |
| `vk_get_wall_posts`   | Получить посты со стены группы             |
| `vk_get_group_info`   | Получить информацию о группе               |
| `vk_get_files`        | Получить документы (файлы) с тегами        |

## Legacy-скрипты

Оригинальные скрипты (`group_posts.py`, `file_tags.py`, `group_info.py`)
по-прежнему доступны, но используют синхронный `requests`.
Для их запуска установите legacy-зависимости:

```bash
pip install ".[legacy]"
```
