# 🏗️ Мультипользовательская архитектура Telegram Userbot

## 📋 Обзор системы

Система для поддержки до **10,000 пользователей** с веб-интерфейсом, API и Telegram Bot для управления настройками переадресации.

### 🎯 Цели
- **Масштабируемость**: До 10,000 активных пользователей
- **Изоляция**: Каждый пользователь видит только свои настройки
- **Гибкость**: Веб-интерфейс + Telegram Bot + API
- **Безопасность**: Многоуровневая система авторизации
- **Производительность**: Оптимизация для высоких нагрузок

---

## 🏛️ Архитектура системы

### **Схема развертывания**
```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer (Nginx)                   │
└─────────────────┬─────────────────┬─────────────────────────┘
                  │                 │
        ┌─────────▼─────────┐ ┌─────▼─────┐
        │   Web Interface   │ │ Telegram  │
        │   (React/Vue.js)  │ │ Bot API   │
        └─────────┬─────────┘ └─────┬─────┘
                  │                 │
        ┌─────────▼─────────┐ ┌─────▼─────┐
        │   API Gateway     │ │  Message  │
        │   (FastAPI)       │ │ Processor │
        └─────────┬─────────┘ └─────┬─────┘
                  │                 │
        ┌─────────▼─────────────────▼─────────┐
        │         Database Layer              │
        │  PostgreSQL + Redis + Elasticsearch │
        └─────────────────────────────────────┘
```

### **Компоненты системы**

#### **1. Frontend (Веб-интерфейс)**
- **Технологии**: React.js + TypeScript
- **UI Framework**: Ant Design / Material-UI
- **Состояние**: Redux Toolkit / Zustand
- **Аутентификация**: Telegram Login Widget

#### **2. Backend API**
- **Framework**: FastAPI (Python)
- **Аутентификация**: JWT + Telegram OAuth
- **Документация**: Swagger/OpenAPI
- **Валидация**: Pydantic

#### **3. Telegram Bot**
- **Библиотека**: python-telegram-bot
- **Команды**: Управление настройками
- **Inline кнопки**: Быстрое управление

#### **4. База данных**
- **Основная**: PostgreSQL
- **Кэш**: Redis
- **Поиск**: Elasticsearch
- **Миграции**: Alembic

#### **5. Message Processor**
- **Telethon**: Обработка сообщений
- **Асинхронность**: asyncio
- **Очереди**: Redis + Celery

---

## 🗄️ Структура базы данных

### **Основные таблицы**

#### **Пользователи**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'user',
    status VARCHAR(20) DEFAULT 'active',
    subscription_tier VARCHAR(20) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_activity TIMESTAMP,
    settings JSONB DEFAULT '{}',
    limits JSONB DEFAULT '{}'
);

-- Индексы
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_status ON users(status);
```

#### **Конфигурации пользователей**
```sql
CREATE TABLE user_configs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    config_type VARCHAR(50) NOT NULL, -- 'sources', 'destinations', 'pipelines'
    config_name VARCHAR(100) NOT NULL,
    config_data JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, config_type, config_name)
);

-- Индексы
CREATE INDEX idx_user_configs_user_id ON user_configs(user_id);
CREATE INDEX idx_user_configs_type ON user_configs(config_type);
CREATE INDEX idx_user_configs_active ON user_configs(is_active);
```

#### **Статистика и метрики**
```sql
CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    messages_processed INTEGER DEFAULT 0,
    pipelines_active INTEGER DEFAULT 0,
    errors_count INTEGER DEFAULT 0,
    api_calls INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы
CREATE INDEX idx_user_stats_user_date ON user_stats(user_id, date);
CREATE INDEX idx_user_stats_date ON user_stats(date);
```

#### **API ключи и токены**
```sql
CREATE TABLE api_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100),
    permissions JSONB DEFAULT '[]',
    expires_at TIMESTAMP,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы
CREATE INDEX idx_api_tokens_user_id ON api_tokens(user_id);
CREATE INDEX idx_api_tokens_expires ON api_tokens(expires_at);
```

#### **Логи и аудит**
```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Индексы
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
```

---

## 🔐 Система безопасности

### **Аутентификация**

#### **1. Telegram OAuth**
```python
# Telegram Login Widget
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_API_ID = "your_api_id"
TELEGRAM_API_HASH = "your_api_hash"

# Валидация данных от Telegram
def verify_telegram_auth(auth_data: dict) -> bool:
    # Проверка подписи от Telegram
    pass
```

#### **2. JWT токены**
```python
# JWT настройки
JWT_SECRET_KEY = "your-secret-key"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 24 * 60 * 60  # 24 часа

# Создание токена
def create_access_token(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
```

### **Авторизация**

#### **Роли пользователей**
```python
ROLES = {
    "super_admin": {
        "permissions": ["*"],
        "description": "Полный доступ ко всем функциям"
    },
    "admin": {
        "permissions": ["manage_users", "view_stats", "manage_system"],
        "description": "Администратор системы"
    },
    "premium_user": {
        "permissions": ["unlimited_pipelines", "api_access", "priority_support"],
        "description": "Премиум пользователь"
    },
    "user": {
        "permissions": ["basic_pipelines", "web_interface"],
        "description": "Обычный пользователь"
    },
    "trial": {
        "permissions": ["limited_pipelines", "web_interface"],
        "description": "Пробный период"
    }
}
```

#### **Middleware для проверки прав**
```python
def require_permission(permission: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Проверка прав доступа
            pass
        return wrapper
    return decorator
```

---

## 🚀 API Endpoints

### **Аутентификация**
```python
# POST /api/v1/auth/telegram
async def telegram_auth(auth_data: TelegramAuth):
    """Аутентификация через Telegram"""
    pass

# POST /api/v1/auth/refresh
async def refresh_token(refresh_token: str):
    """Обновление JWT токена"""
    pass

# POST /api/v1/auth/logout
async def logout():
    """Выход из системы"""
    pass
```

### **Пользователи**
```python
# GET /api/v1/users/profile
async def get_user_profile():
    """Получение профиля пользователя"""
    pass

# PUT /api/v1/users/profile
async def update_user_profile(profile: UserProfile):
    """Обновление профиля"""
    pass

# GET /api/v1/users/stats
async def get_user_stats(period: str = "30d"):
    """Статистика пользователя"""
    pass
```

### **Конфигурации**
```python
# GET /api/v1/configs/sources
async def get_user_sources():
    """Получение источников пользователя"""
    pass

# POST /api/v1/configs/sources
async def create_user_source(source: SourceConfig):
    """Создание источника"""
    pass

# PUT /api/v1/configs/sources/{source_id}
async def update_user_source(source_id: int, source: SourceConfig):
    """Обновление источника"""
    pass

# DELETE /api/v1/configs/sources/{source_id}
async def delete_user_source(source_id: int):
    """Удаление источника"""
    pass

# Аналогично для destinations и pipelines
```

### **Пайплайны**
```python
# GET /api/v1/pipelines
async def get_user_pipelines():
    """Получение пайплайнов пользователя"""
    pass

# POST /api/v1/pipelines
async def create_pipeline(pipeline: PipelineConfig):
    """Создание пайплайна"""
    pass

# PUT /api/v1/pipelines/{pipeline_id}/start
async def start_pipeline(pipeline_id: int):
    """Запуск пайплайна"""
    pass

# PUT /api/v1/pipelines/{pipeline_id}/stop
async def stop_pipeline(pipeline_id: int):
    """Остановка пайплайна"""
    pass
```

### **API ключи**
```python
# GET /api/v1/tokens
async def get_api_tokens():
    """Получение API ключей"""
    pass

# POST /api/v1/tokens
async def create_api_token(token: TokenConfig):
    """Создание API ключа"""
    pass

# DELETE /api/v1/tokens/{token_id}
async def delete_api_token(token_id: int):
    """Удаление API ключа"""
    pass
```

---

## 🎨 Веб-интерфейс

### **Структура React приложения**
```
src/
├── components/
│   ├── auth/
│   │   ├── TelegramLogin.tsx
│   │   └── ProtectedRoute.tsx
│   ├── dashboard/
│   │   ├── Dashboard.tsx
│   │   ├── Stats.tsx
│   │   └── QuickActions.tsx
│   ├── configs/
│   │   ├── Sources.tsx
│   │   ├── Destinations.tsx
│   │   └── Pipelines.tsx
│   ├── pipeline/
│   │   ├── PipelineList.tsx
│   │   ├── PipelineEditor.tsx
│   │   └── PipelineStats.tsx
│   └── common/
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── Loading.tsx
├── pages/
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── Sources.tsx
│   ├── Destinations.tsx
│   ├── Pipelines.tsx
│   ├── Settings.tsx
│   └── API.tsx
├── services/
│   ├── api.ts
│   ├── auth.ts
│   └── websocket.ts
├── store/
│   ├── authSlice.ts
│   ├── configSlice.ts
│   └── pipelineSlice.ts
└── utils/
    ├── constants.ts
    ├── helpers.ts
    └── types.ts
```

### **Основные страницы**

#### **1. Dashboard (Главная)**
- Общая статистика
- Активные пайплайны
- Быстрые действия
- Уведомления

#### **2. Sources (Источники)**
- Список источников
- Добавление/редактирование
- Тестирование подключения
- Статистика по источникам

#### **3. Destinations (Назначения)**
- Список назначений
- Настройка типов (Telegram, Webhook, Database)
- Тестирование отправки
- Логи отправки

#### **4. Pipelines (Пайплайны)**
- Создание пайплайнов
- Визуальный редактор
- Мониторинг статуса
- Детальная статистика

#### **5. Settings (Настройки)**
- Профиль пользователя
- API ключи
- Уведомления
- Подписка

---

## 🤖 Telegram Bot

### **Команды для пользователей**
```python
# Основные команды
/start - Начало работы
/help - Справка
/profile - Профиль пользователя
/stats - Статистика

# Управление источниками
/sources - Список источников
/source_add <name> <id> - Добавить источник
/source_remove <name> - Удалить источник
/source_test <name> - Тест источника

# Управление назначениями
/destinations - Список назначений
/dest_add <name> <type> <config> - Добавить назначение
/dest_remove <name> - Удалить назначение

# Управление пайплайнами
/pipelines - Список пайплайнов
/pipeline_create <name> <source> <dest> - Создать пайплайн
/pipeline_start <name> - Запустить пайплайн
/pipeline_stop <name> - Остановить пайплайн
/pipeline_remove <name> - Удалить пайплайн

# Статистика
/stats_daily - Статистика за день
/stats_weekly - Статистика за неделю
/stats_monthly - Статистика за месяц
```

### **Inline кнопки**
```python
# Быстрые действия
[
    [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
    [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
    [InlineKeyboardButton("🔗 Источники", callback_data="sources")],
    [InlineKeyboardButton("📤 Назначения", callback_data="destinations")]
]

# Управление пайплайнами
[
    [InlineKeyboardButton("▶️ Запустить", callback_data="pipeline_start_123")],
    [InlineKeyboardButton("⏹️ Остановить", callback_data="pipeline_stop_123")],
    [InlineKeyboardButton("📊 Детали", callback_data="pipeline_details_123")]
]
```

---

## 📊 Система мониторинга

### **Метрики для отслеживания**
```python
# Пользовательские метрики
USER_METRICS = [
    "active_users_daily",
    "new_registrations",
    "pipeline_creations",
    "api_calls_per_user",
    "error_rate_per_user"
]

# Системные метрики
SYSTEM_METRICS = [
    "database_connections",
    "redis_memory_usage",
    "api_response_time",
    "telegram_api_calls",
    "queue_size"
]

# Бизнес метрики
BUSINESS_METRICS = [
    "conversion_rate",
    "premium_subscriptions",
    "user_retention",
    "support_tickets"
]
```

### **Алерты и уведомления**
```python
# Критические алерты
CRITICAL_ALERTS = [
    "database_connection_failed",
    "redis_memory_exceeded",
    "api_rate_limit_exceeded",
    "telegram_api_error"
]

# Предупреждения
WARNING_ALERTS = [
    "high_cpu_usage",
    "slow_database_queries",
    "user_limit_approaching"
]
```

---

## 🚀 Развертывание

### **Docker Compose для продакшена**
```yaml
version: '3.8'

services:
  # База данных
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: userbot_multi
      POSTGRES_USER: userbot
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - userbot_network

  # Redis для кэша
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - userbot_network

  # Elasticsearch для поиска
  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - userbot_network

  # API сервер
  api:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://userbot:${DB_PASSWORD}@postgres/userbot_multi
      - REDIS_URL=redis://redis:6379
      - ELASTICSEARCH_URL=http://elasticsearch:9200
    depends_on:
      - postgres
      - redis
      - elasticsearch
    networks:
      - userbot_network

  # Веб-интерфейс
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - api
    networks:
      - userbot_network

  # Telegram Bot
  telegram_bot:
    build: ./telegram_bot
    environment:
      - BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - API_URL=http://api:8000
    depends_on:
      - api
    networks:
      - userbot_network

  # Message Processor
  message_processor:
    build: ./message_processor
    environment:
      - DATABASE_URL=postgresql://userbot:${DB_PASSWORD}@postgres/userbot_multi
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    networks:
      - userbot_network

  # Мониторинг
  prometheus:
    image: prom/prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
    networks:
      - userbot_network

  grafana:
    image: grafana/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - userbot_network

volumes:
  postgres_data:
  redis_data:
  elasticsearch_data:
  grafana_data:

networks:
  userbot_network:
    driver: bridge
```

---

## 📈 Масштабирование

### **Горизонтальное масштабирование**
```bash
# Масштабирование API серверов
docker-compose up --scale api=3

# Масштабирование Message Processors
docker-compose up --scale message_processor=5

# Балансировка нагрузки
docker-compose up --scale frontend=2
```

### **Вертикальное масштабирование**
```yaml
# Увеличение ресурсов
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

---

## 🔧 Оптимизация производительности

### **Кэширование**
```python
# Redis кэш для частых запросов
CACHE_CONFIG = {
    "user_configs": 300,  # 5 минут
    "user_stats": 600,     # 10 минут
    "pipeline_status": 30,  # 30 секунд
    "api_tokens": 1800     # 30 минут
}
```

### **Индексы базы данных**
```sql
-- Составные индексы для быстрых запросов
CREATE INDEX idx_user_configs_user_type_active 
ON user_configs(user_id, config_type, is_active);

CREATE INDEX idx_user_stats_user_date_processed 
ON user_stats(user_id, date, messages_processed);

-- Частичные индексы
CREATE INDEX idx_active_users 
ON users(telegram_id) WHERE status = 'active';
```

### **Асинхронная обработка**
```python
# Celery для фоновых задач
CELERY_TASKS = [
    "process_messages",
    "update_statistics",
    "send_notifications",
    "backup_user_data"
]
```

---

## 🛡️ Безопасность

### **Защита от атак**
```python
# Rate limiting
RATE_LIMITS = {
    "api_calls": "100/minute",
    "login_attempts": "5/minute",
    "pipeline_creations": "10/hour"
}

# Валидация входных данных
def validate_user_input(data: dict) -> bool:
    # Проверка типов данных
    # Санитизация строк
    # Проверка размеров
    pass
```

### **Шифрование данных**
```python
# Шифрование чувствительных данных
from cryptography.fernet import Fernet

def encrypt_sensitive_data(data: str) -> str:
    f = Fernet(ENCRYPTION_KEY)
    return f.encrypt(data.encode()).decode()

def decrypt_sensitive_data(encrypted_data: str) -> str:
    f = Fernet(ENCRYPTION_KEY)
    return f.decrypt(encrypted_data.encode()).decode()
```

---

## 📋 План реализации

### **Этап 1: Базовая инфраструктура (2-3 недели)**
1. Настройка базы данных
2. Создание API сервера
3. Базовая аутентификация
4. Простой веб-интерфейс

### **Этап 2: Основной функционал (3-4 недели)**
1. Управление конфигурациями
2. Telegram Bot
3. Система ролей
4. Базовый мониторинг

### **Этап 3: Масштабирование (2-3 недели)**
1. Оптимизация производительности
2. Кэширование
3. Асинхронная обработка
4. Расширенный мониторинг

### **Этап 4: Продакшн готовность (1-2 недели)**
1. Тестирование нагрузки
2. Безопасность
3. Документация
4. Развертывание

---

## 💰 Монетизация

### **Тарифные планы**
```python
SUBSCRIPTION_TIERS = {
    "free": {
        "pipelines_limit": 3,
        "api_calls_limit": 1000,
        "storage_limit": "100MB",
        "support": "community"
    },
    "basic": {
        "pipelines_limit": 10,
        "api_calls_limit": 10000,
        "storage_limit": "1GB",
        "support": "email",
        "price": "$9.99/month"
    },
    "premium": {
        "pipelines_limit": 50,
        "api_calls_limit": 100000,
        "storage_limit": "10GB",
        "support": "priority",
        "price": "$29.99/month"
    },
    "enterprise": {
        "pipelines_limit": "unlimited",
        "api_calls_limit": "unlimited",
        "storage_limit": "unlimited",
        "support": "dedicated",
        "price": "custom"
    }
}
```

---

## 📞 Поддержка

### **Система тикетов**
```python
SUPPORT_TICKETS = {
    "priority": ["critical", "high", "medium", "low"],
    "categories": ["technical", "billing", "feature_request", "bug_report"],
    "response_times": {
        "critical": "1 hour",
        "high": "4 hours",
        "medium": "24 hours",
        "low": "72 hours"
    }
}
```

### **Документация**
- API документация (Swagger)
- Руководство пользователя
- Видео-туториалы
- FAQ

---

## 🎯 Заключение

Данная архитектура обеспечивает:

✅ **Масштабируемость** до 10,000 пользователей  
✅ **Безопасность** и изоляцию данных  
✅ **Гибкость** в управлении  
✅ **Производительность** и оптимизацию  
✅ **Мониторинг** и аналитику  
✅ **Монетизацию** через тарифные планы  

Система готова к поэтапной реализации с возможностью масштабирования по мере роста пользовательской базы. 