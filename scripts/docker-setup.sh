#!/bin/bash

# Скрипт для автоматической настройки Docker окружения
# для Telegram Userbot

set -e  # Остановка при ошибке

echo "🐳 Настройка Docker окружения для Telegram Userbot"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия Docker
check_docker() {
    log_info "Проверка Docker..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker не установлен. Установите Docker и попробуйте снова."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
        exit 1
    fi
    
    log_success "Docker и Docker Compose установлены"
}

# Создание необходимых директорий
create_directories() {
    log_info "Создание директорий..."
    
    mkdir -p data logs sessions backups monitoring notebooks grafana prometheus
    
    log_success "Директории созданы"
}

# Настройка .env файла
setup_env() {
    log_info "Настройка .env файла..."
    
    if [ ! -f .env ]; then
        if [ -f combined_config_example.env ]; then
            cp combined_config_example.env .env
            log_success ".env файл создан из примера"
        else
            log_warning "Файл combined_config_example.env не найден. Создайте .env вручную."
        fi
    else
        log_info ".env файл уже существует"
    fi
    
    # Проверка обязательных переменных
    if [ -f .env ]; then
        if ! grep -q "API_ID=" .env || ! grep -q "API_HASH=" .env; then
            log_warning "В .env файле отсутствуют API_ID или API_HASH. Настройте их вручную."
        fi
    fi
}

# Настройка прав доступа
setup_permissions() {
    log_info "Настройка прав доступа..."
    
    # Устанавливаем права для текущего пользователя
    sudo chown -R $USER:$USER data logs sessions backups monitoring notebooks grafana prometheus 2>/dev/null || true
    chmod 755 data logs sessions backups monitoring notebooks grafana prometheus
    
    log_success "Права доступа настроены"
}

# Сборка Docker образа
build_image() {
    log_info "Сборка Docker образа..."
    
    docker-compose build
    
    log_success "Docker образ собран"
}

# Проверка конфигурации
check_config() {
    log_info "Проверка конфигурации Docker Compose..."
    
    docker-compose config > /dev/null
    
    log_success "Конфигурация корректна"
}

# Создание скриптов управления
create_scripts() {
    log_info "Создание скриптов управления..."
    
    # Скрипт запуска
    cat > scripts/start.sh << 'EOF'
#!/bin/bash
echo "🚀 Запуск Telegram Userbot..."
docker-compose up -d
echo "✅ Бот запущен. Логи: docker-compose logs -f"
EOF

    # Скрипт остановки
    cat > scripts/stop.sh << 'EOF'
#!/bin/bash
echo "🛑 Остановка Telegram Userbot..."
docker-compose down
echo "✅ Бот остановлен"
EOF

    # Скрипт перезапуска
    cat > scripts/restart.sh << 'EOF'
#!/bin/bash
echo "🔄 Перезапуск Telegram Userbot..."
docker-compose restart
echo "✅ Бот перезапущен"
EOF

    # Скрипт просмотра логов
    cat > scripts/logs.sh << 'EOF'
#!/bin/bash
echo "📋 Логи Telegram Userbot..."
docker-compose logs -f
EOF

    # Скрипт бэкапа
    cat > scripts/backup.sh << 'EOF'
#!/bin/bash
echo "💾 Создание бэкапа..."
docker-compose -f docker-compose.prod.yml run backup
echo "✅ Бэкап создан в папке backups/"
EOF

    # Делаем скрипты исполняемыми
    chmod +x scripts/*.sh
    
    log_success "Скрипты управления созданы"
}

# Создание README для Docker
create_docker_readme() {
    log_info "Создание документации..."
    
    cat > DOCKER_README.md << 'EOF'
# 🐳 Docker - Быстрый старт

## 🚀 Запуск

```bash
# Запуск в фоне
./scripts/start.sh

# Просмотр логов
./scripts/logs.sh

# Остановка
./scripts/stop.sh

# Перезапуск
./scripts/restart.sh

# Бэкап данных
./scripts/backup.sh
```

## 📋 Команды Docker

```bash
# Сборка образа
docker-compose build

# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Логи
docker-compose logs -f

# Вход в контейнер
docker-compose exec telegram-userbot bash
```

## 🔧 Разработка

```bash
# Запуск с отладкой
docker-compose -f docker-compose.dev.yml up

# Jupyter Notebook (анализ данных)
# Доступен по адресу: http://localhost:8888

# Grafana (мониторинг)
# Доступен по адресу: http://localhost:3000
# Логин: admin, Пароль: admin

# PostgreSQL (база данных)
# Хост: localhost, Порт: 5432
# База: userbot, Пользователь: userbot, Пароль: userbot_password
```

## 📊 Мониторинг

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000
- **Jupyter**: http://localhost:8888

## ⚠️ Важно

1. Настройте .env файл перед запуском
2. Укажите API_ID и API_HASH
3. Настройте ID групп
4. Проверьте права доступа к папкам
EOF

    log_success "Документация создана"
}

# Основная функция
main() {
    echo "=========================================="
    echo "🐳 Настройка Docker для Telegram Userbot"
    echo "=========================================="
    
    check_docker
    create_directories
    setup_env
    setup_permissions
    build_image
    check_config
    create_scripts
    create_docker_readme
    
    echo ""
    echo "=========================================="
    log_success "Настройка завершена!"
    echo "=========================================="
    echo ""
    echo "📋 Следующие шаги:"
    echo "1. Настройте .env файл (API_ID, API_HASH, ID групп)"
    echo "2. Запустите бота: ./scripts/start.sh"
    echo "3. Проверьте логи: ./scripts/logs.sh"
    echo ""
    echo "📚 Документация: DOCKER_README.md"
    echo "🔧 Скрипты управления: scripts/"
    echo ""
}

# Запуск основной функции
main "$@" 