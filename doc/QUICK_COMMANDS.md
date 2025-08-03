# ⚡ Быстрый справочник команд

## 🎯 Основные команды

| Команда | Описание |
|---------|----------|
| `.pipelines_list` | Список всех пайплайнов |
| `.pipelines_start_all` | Запустить все пайплайны |
| `.pipelines_stop_all` | Остановить все пайплайны |
| `.pipeline_status <имя>` | Статус конкретного пайплайна |
| `.sources_list` | Список источников |
| `.destinations_list` | Список назначений |
| `.config` | Показать конфигурацию |
| `.status` | Общий статус userbot |
| `.help` | Справка по командам |

## 📊 Управление источниками

| Команда | Пример |
|---------|--------|
| `.source_add <название> <chat_id>` | `.source_add my_channel -1001234567890` |
| `.source_remove <название>` | `.source_remove my_channel` |

## 🎯 Управление назначениями

| Команда | Пример |
|---------|--------|
| `.destination_add <название> <тип> <конфиг>` | `.destination_add my_db database {"host":"localhost"}` |
| `.destination_remove <название>` | `.destination_remove my_db` |

## 🔧 Управление пайплайнами

| Команда | Пример |
|---------|--------|
| `.pipeline_create <название> <источник> <назначения>` | `.pipeline_create my_pipeline news_channel analytics_db` |
| `.pipeline_remove <название>` | `.pipeline_remove my_pipeline` |

## 📈 Статистика и экспорт

| Команда | Пример |
|---------|--------|
| `.stats_export <формат>` | `.stats_export json` |

## 🔍 Отладка

| Команда | Описание |
|---------|----------|
| `.ping` | Проверка связи |
| `.info` | Информация о userbot |
| `.safety` | Настройки безопасности |
| `.test_access` | Тест доступа к каналам |
| `.test_media` | Тест обработки медиа |

## 🚨 Частые проблемы

### Пайплайн не работает:
1. `.pipeline_status <имя>` - проверить статус
2. `.sources_list` - проверить источники
3. `docker logs telegram-userbot` - посмотреть логи

### Добавить новый канал:
1. `.source_add <название> <chat_id>`
2. `.pipeline_create <название> <источник> <назначения>`

### Экспорт данных:
1. `.stats_export json` - экспорт статистики
2. Проверить папку `data/` для файлов

## 📝 Примеры использования

### Мониторинг новостного канала:
```
.source_add news -1001234567890
.pipeline_create news_monitor news notification_channel
```

### Анализ технической группы:
```
.source_add tech_group -1009876543210
.pipeline_create tech_analysis tech_group analytics_db,elasticsearch
```

### Экспорт статистики:
```
.stats_export json
```

## ⚙️ Настройка через файлы

- `config/sources.json` - источники
- `config/destinations.json` - назначения  
- `config/pipelines.json` - пайплайны
- `.env` - основные настройки

## 🔐 Безопасность

- Все команды требуют авторизации
- Логирование всех операций
- Защита от спама и флуда 