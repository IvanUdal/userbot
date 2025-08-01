# 🔄 Руководство по миграции на масштабируемую архитектуру

## 📋 Обзор

Данное руководство поможет вам перейти с простой архитектуры (один источник → одно назначение) на масштабируемую архитектуру пайплайнов.

## 🎯 Преимущества миграции

### ✅ **Что вы получите:**

- **Множественные источники** - парсинг из нескольких групп одновременно
- **Множественные назначения** - отправка в разные места
- **Гибкая обработка** - фильтрация, форматирование, классификация
- **Мониторинг** - детальная статистика и алерты
- **Масштабируемость** - легко добавлять новые источники и назначения

## 🚀 Пошаговая миграция

### Шаг 1: Подготовка

1. **Создайте резервную копию текущего проекта**
```bash
cp -r userbot userbot_backup
```

2. **Установите новые зависимости**
```bash
pip install -r requirements.txt
```

### Шаг 2: Миграция конфигурации

#### Из старого `.env` в новую архитектуру:

**Старый формат:**
```env
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1009876543210
FORWARDING_ENABLED=true
```

**Новый формат:**
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

### Шаг 3: Создание конфигурационных файлов

#### 1. Создайте `config/sources.json`:

```json
{
  "sources": {
    "main_source": {
      "id": -1001234567890,
      "name": "Основной источник",
      "type": "group",
      "enabled": true,
      "parsing_rules": {
        "parse_text": true,
        "parse_media": true,
        "parse_buttons": true,
        "parse_bots": false
      },
      "filters": {
        "keywords": [],
        "exclude_keywords": ["спам"],
        "min_length": 0
      }
    }
  }
}
```

#### 2. Создайте `config/destinations.json`:

```json
{
  "destinations": {
    "main_target": {
      "name": "Основное назначение",
      "type": "telegram",
      "enabled": true,
      "config": {
        "chat_id": -1009876543210,
        "format": "markdown"
      },
      "processing_rules": {
        "summarize": false,
        "highlight_keywords": false,
        "add_metadata": true
      }
    }
  }
}
```

#### 3. Создайте `config/pipelines.json`:

```json
{
  "pipelines": {
    "main_pipeline": {
      "name": "Основной пайплайн",
      "enabled": true,
      "source": "main_source",
      "destinations": ["main_target"],
      "processing_steps": [
        {
          "name": "basic_filtering",
          "type": "filter",
          "config": {
            "exclude_keywords": ["спам"],
            "min_length": 0
          }
        },
        {
          "name": "basic_formatting",
          "type": "formatter",
          "config": {
            "add_timestamps": true,
            "add_source_info": true
          }
        }
      ],
      "created_at": "2024-01-01T00:00:00",
      "last_run": null,
      "total_processed": 0,
      "total_errors": 0
    }
  }
}
```

### Шаг 4: Запуск новой архитектуры

1. **Остановите старый бот**
```bash
# Остановите текущий процесс
pkill -f "python main.py"
```

2. **Запустите новый бот**
```bash
python main_pipeline.py
```

3. **Проверьте работу**
```bash
# В Telegram отправьте команду
.ping
```

### Шаг 5: Настройка через команды

#### Добавление источников:
```bash
.source_add news_channel -1001234567890
.source_add support_group -1009876543210
```

#### Добавление назначений:
```bash
.destination_add notifications telegram {"chat_id": -100111222333}
.destination_add export_file file {"format": "json", "path": "./data/exports/"}
```

#### Создание пайплайнов:
```bash
.pipeline_create news_monitoring news_channel notifications
.pipeline_create support_tracking support_group export_file
```

#### Запуск всех пайплайнов:
```bash
.pipelines_start_all
```

## 🔧 Расширение функциональности

### Добавление фильтрации

Отредактируйте `config/pipelines.json`:

```json
{
  "processing_steps": [
    {
      "name": "keyword_filtering",
      "type": "filter",
      "config": {
        "keywords": ["важно", "срочно"],
        "exclude_keywords": ["спам", "реклама"],
        "min_length": 10
      }
    }
  ]
}
```

### Добавление классификации

```json
{
  "processing_steps": [
    {
      "name": "priority_classification",
      "type": "classifier",
      "config": {
        "urgency_keywords": ["срочно", "критично"],
        "priority_levels": ["low", "medium", "high", "critical"]
      }
    }
  ]
}
```

### Добавление новых назначений

#### База данных PostgreSQL:
```bash
.destination_add analytics_db database {"connection_string": "postgresql://user:pass@localhost/analytics"}
```

#### Elasticsearch:
```bash
.destination_add elasticsearch elasticsearch {"hosts": ["localhost:9200"], "index": "telegram_messages"}
```

#### Webhook:
```bash
.destination_add webhook webhook {"url": "https://api.example.com/webhook", "method": "POST"}
```

## 📊 Мониторинг миграции

### Проверка статуса:
```bash
.status                    # Общая статистика
.pipelines_list           # Список пайплайнов
.sources_list             # Список источников
.destinations_list        # Список назначений
```

### Просмотр статистики:
```bash
.pipeline_status main_pipeline  # Статистика конкретного пайплайна
.stats_export all_pipelines    # Экспорт статистики
```

## 🔍 Отладка проблем

### Проблема: "Источник не найден"
```bash
# Проверьте доступ к источнику
.source_add test_source -1001234567890
```

### Проблема: "Ошибка отправки в назначение"
```bash
# Проверьте конфигурацию назначения
.destination_add test_dest telegram {"chat_id": -100111222333}
```

### Проблема: "Пайплайн не запускается"
```bash
# Проверьте статус пайплайна
.pipeline_status <pipeline_name>

# Перезапустите пайплайн
.pipelines_stop_all
.pipelines_start_all
```

## 📈 Оптимизация производительности

### 1. Настройка параллельной обработки

Отредактируйте `config/pipelines.json`:

```json
{
  "pipelines": {
    "parallel_pipeline": {
      "name": "Параллельная обработка",
      "enabled": true,
      "source": "main_source",
      "destinations": ["dest1", "dest2", "dest3"],
      "processing_steps": [
        {
          "name": "parallel_processing",
          "type": "parallel",
          "config": {
            "max_workers": 4,
            "batch_size": 100
          }
        }
      ]
    }
  }
}
```

### 2. Настройка кэширования

```json
{
  "processing_steps": [
    {
      "name": "caching",
      "type": "cache",
      "config": {
        "cache_enabled": true,
        "cache_ttl": 3600,
        "cache_size": 1000
      }
    }
  ]
}
```

## 🔒 Безопасность

### 1. Шифрование конфигурации

```json
{
  "destinations": {
    "secure_db": {
      "name": "Защищенная БД",
      "type": "database",
      "enabled": true,
      "config": {
        "connection_string": "postgresql://user:pass@localhost/secure_db",
        "encryption": {
          "enabled": true,
          "algorithm": "AES-256",
          "key": "your_encryption_key"
        }
      }
    }
  }
}
```

### 2. Аутентификация источников

```json
{
  "sources": {
    "private_group": {
      "id": -1001234567890,
      "name": "Приватная группа",
      "type": "group",
      "enabled": true,
      "access_control": {
        "require_member": true,
        "allowed_users": [123456789, 987654321]
      }
    }
  }
}
```

## 📚 Дополнительные ресурсы

- [PIPELINE_ARCHITECTURE_GUIDE.md](./PIPELINE_ARCHITECTURE_GUIDE.md) - Подробное руководство по архитектуре
- [ARCHITECTURE_GUIDE.md](./ARCHITECTURE_GUIDE.md) - Архитектурная документация
- [config_example.py](./config_example.py) - Примеры конфигураций

## 🤝 Поддержка

При возникновении проблем:

1. **Проверьте логи**: `tail -f logs/userbot.log`
2. **Убедитесь в правильности конфигурации**
3. **Проверьте доступ к источникам**
4. **Обратитесь к документации**

Эта миграция откроет новые возможности для масштабирования вашего Telegram Userbot и управления сложными сценариями парсинга. 