# 🏗️ Руководство по масштабируемой архитектуре пайплайнов

## 📋 Обзор

Данная архитектура позволяет управлять парсингом из множества источников в множество назначений с централизованным управлением настройками. Это решение для тех, кто хочет масштабировать свой Telegram Userbot и управлять сложными сценариями парсинга.

## 🎯 Преимущества архитектуры

### ✅ **Модульность**
- Каждый компонент независим и может быть заменен
- Легко добавлять новые типы источников и назначений
- Гибкая система обработки данных

### ✅ **Масштабируемость**
- Поддержка множественных источников одновременно
- Параллельная обработка данных
- Горизонтальное и вертикальное масштабирование

### ✅ **Централизованное управление**
- Все настройки в JSON файлах
- Единая точка управления
- Простое добавление новых пайплайнов

### ✅ **Мониторинг и аналитика**
- Детальная статистика по каждому пайплайну
- Отслеживание производительности
- Система уведомлений и алертов

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации

Создайте файл `.env` с основными настройками:

```env
# Основные настройки
API_ID=your_api_id
API_HASH=your_api_hash
SESSION_NAME=userbot

# Уведомления
NOTIFY_START=true
NOTIFY_STATS=true
ADMIN_CHAT_ID=-1001234567890
```

### 3. Запуск бота

```bash
python main_pipeline.py
```

## 📁 Структура проекта

```
userbot/
├── 📁 config/                    # Конфигурационные файлы
│   ├── 📄 sources.json          # Источники парсинга
│   ├── 📄 destinations.json     # Назначения
│   └── 📄 pipelines.json        # Пайплайны обработки
├── 📁 modules/                   # Модули системы
│   ├── 📄 pipeline_manager.py   # Управление пайплайнами
│   └── 📄 pipeline_commands.py  # Команды управления
├── 📁 data/                      # Данные
│   └── 📁 exports/              # Экспортированные данные
├── 📁 logs/                      # Логи
├── 📄 main_pipeline.py          # Основной файл
└── 📄 config.py                 # Конфигурация
```

## 🔧 Настройка источников

### Добавление источника через команду

```bash
.source_add news_channel -1001234567890
```

### Ручное редактирование `config/sources.json`

```json
{
  "sources": {
    "news_channel": {
      "id": -1001234567890,
      "name": "Новостной канал",
      "type": "channel",
      "enabled": true,
      "parsing_rules": {
        "parse_text": true,
        "parse_media": true,
        "parse_buttons": true,
        "parse_bots": false
      },
      "filters": {
        "keywords": ["новости", "анонс"],
        "exclude_keywords": ["спам"],
        "min_length": 10
      }
    }
  }
}
```

### Типы источников

- **channel** - Публичные каналы
- **group** - Обычные группы
- **supergroup** - Супергруппы

## 🎯 Настройка назначений

### Добавление назначения через команду

```bash
.destination_add telegram_dest telegram {"chat_id": -100111222333}
```

### Ручное редактирование `config/destinations.json`

```json
{
  "destinations": {
    "telegram_dest": {
      "name": "Telegram назначение",
      "type": "telegram",
      "enabled": true,
      "config": {
        "chat_id": -100111222333,
        "format": "markdown"
      },
      "processing_rules": {
        "summarize": true,
        "highlight_keywords": true
      }
    }
  }
}
```

### Типы назначений

- **telegram** - Отправка в Telegram чат/канал
- **file** - Сохранение в файл (JSON, CSV)
- **database** - Сохранение в базу данных
- **webhook** - Отправка через webhook
- **elasticsearch** - Индексация в Elasticsearch

## 🔄 Создание пайплайнов

### Добавление пайплайна через команду

```bash
.pipeline_create news_analytics news_channel telegram_dest,export_file
```

### Ручное редактирование `config/pipelines.json`

```json
{
  "pipelines": {
    "news_analytics": {
      "name": "Аналитика новостей",
      "enabled": true,
      "source": "news_channel",
      "destinations": ["telegram_dest", "export_file"],
      "processing_steps": [
        {
          "name": "content_filtering",
          "type": "filter",
          "config": {
            "keywords": ["новости", "важно"],
            "exclude_keywords": ["спам"],
            "min_length": 10
          }
        },
        {
          "name": "formatting",
          "type": "formatter",
          "config": {
            "add_timestamps": true,
            "add_source_info": true
          }
        }
      ]
    }
  }
}
```

### Типы шагов обработки

- **filter** - Фильтрация сообщений
- **formatter** - Форматирование данных
- **classifier** - Классификация сообщений
- **analyzer** - Анализ контента
- **enricher** - Обогащение данных

## 📊 Команды управления

### Базовые команды

```bash
.ping                    # Проверка работоспособности
.info                    # Информация о конфигурации
.status                  # Статус системы
.help                    # Справка
```

### Управление пайплайнами

```bash
.pipelines_start_all     # Запуск всех пайплайнов
.pipelines_stop_all      # Остановка всех пайплайнов
.pipeline_status <name>  # Статус конкретного пайплайна
.pipelines_list          # Список всех пайплайнов
```

### Управление источниками

```bash
.source_add <name> <id>  # Добавить источник
.source_remove <name>     # Удалить источник
.sources_list            # Список источников
```

### Управление назначениями

```bash
.destination_add <name> <type> <config>  # Добавить назначение
.destination_remove <name>               # Удалить назначение
.destinations_list                       # Список назначений
```

### Статистика и экспорт

```bash
.stats_export all_pipelines  # Экспорт статистики
```

## 🔍 Примеры использования

### Сценарий 1: Мониторинг новостей

```bash
# 1. Добавляем источник новостей
.source_add news_channel -1001234567890

# 2. Добавляем назначение для уведомлений
.destination_add notifications telegram {"chat_id": -100111222333}

# 3. Создаем пайплайн
.pipeline_create news_monitoring news_channel notifications

# 4. Запускаем все пайплайны
.pipelines_start_all
```

### Сценарий 2: Анализ технического сообщества

```bash
# 1. Добавляем источник
.source_add tech_community -1009876543210

# 2. Добавляем назначения
.destination_add analytics_db database {"connection_string": "postgresql://..."}
.destination_add export_file file {"format": "json", "path": "./data/exports/"}

# 3. Создаем пайплайн с обработкой
.pipeline_create tech_analysis tech_community analytics_db,export_file

# 4. Запускаем
.pipelines_start_all
```

### Сценарий 3: Комплексный мониторинг

```bash
# 1. Добавляем несколько источников
.source_add news_channel -1001234567890
.source_add support_group -1009876543210
.source_add tech_community -100111222333

# 2. Добавляем назначения
.destination_add notifications telegram {"chat_id": -100111222333}
.destination_add analytics_db database {"connection_string": "..."}
.destination_add export_file file {"format": "json"}

# 3. Создаем пайплайны
.pipeline_create news_monitoring news_channel notifications
.pipeline_create support_tracking support_group analytics_db,export_file
.pipeline_create tech_analysis tech_community analytics_db,notifications

# 4. Запускаем
.pipelines_start_all
```

## 📈 Мониторинг и аналитика

### Просмотр статистики

```bash
.status                    # Общая статистика
.pipeline_status <name>    # Статистика пайплайна
.stats_export all_pipelines # Экспорт статистики
```

### Метрики для отслеживания

- **Производительность**: сообщений в секунду, время обработки
- **Качество данных**: процент успешных парсингов, количество ошибок
- **Бизнес-метрики**: популярные темы, активность источников

## 🔒 Безопасность

### Рекомендации

1. **Шифрование данных** - используйте AES для чувствительной информации
2. **Аутентификация** - проверяйте доступ к источникам
3. **Логирование** - ведите детальные логи всех операций
4. **Резервное копирование** - настройте автоматические бэкапы

### Настройка прав доступа

```json
{
  "sources": {
    "private_group": {
      "id": -1001234567890,
      "name": "Приватная группа",
      "type": "group",
      "enabled": true,
      "access_control": {
        "require_admin": false,
        "require_member": true,
        "allowed_users": [123456789, 987654321]
      }
    }
  }
}
```

## 🚀 Масштабирование

### Горизонтальное масштабирование

1. **Множественные инстансы** - запуск нескольких ботов
2. **Балансировка нагрузки** - распределение источников между инстансами
3. **Очереди сообщений** - Redis/RabbitMQ для обработки

### Вертикальное масштабирование

1. **Оптимизация памяти** - кэширование и пулы соединений
2. **Многопоточность** - асинхронная обработка
3. **База данных** - индексы и партиционирование

## 🛠️ Отладка и диагностика

### Просмотр логов

```bash
tail -f logs/userbot.log
```

### Проверка состояния пайплайнов

```bash
.pipeline_status news_analytics
```

### Диагностика ошибок

```bash
# Проверка подключения к источнику
.source_add test_source -1001234567890

# Проверка назначения
.destination_add test_dest telegram {"chat_id": -100111222333}
```

## 📊 Дашборд мониторинга

Для визуализации данных рекомендуется использовать:

- **Grafana** - для метрик и графиков
- **Kibana** - для логов и поиска
- **Prometheus** - для сбора метрик

## 🔧 Расширение функциональности

### Добавление новых типов назначений

1. Создайте новый класс в `modules/`
2. Добавьте обработку в `PipelineManager`
3. Обновите документацию

### Добавление новых шагов обработки

1. Реализуйте логику в `PipelineManager`
2. Добавьте конфигурацию
3. Протестируйте на примерах

## 📚 Дополнительные ресурсы

- [ARCHITECTURE_GUIDE.md](./ARCHITECTURE_GUIDE.md) - Подробная архитектурная документация
- [config_example.py](./config_example.py) - Примеры конфигураций
- [parser_example.py](./parser_example.py) - Примеры парсинга

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи в `logs/userbot.log`
2. Убедитесь в правильности конфигурации
3. Проверьте доступ к источникам
4. Обратитесь к документации

Эта архитектура обеспечивает гибкое и масштабируемое управление парсингом из множества источников в множество назначений с централизованным контролем и детальным мониторингом. 