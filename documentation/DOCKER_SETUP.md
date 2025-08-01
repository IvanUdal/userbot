# 🐳 Docker настройка для Telegram Userbot

## 🎯 Обзор

Docker позволяет легко развертывать и запускать Telegram userbot в любом окружении с полной изоляцией и воспроизводимостью.

## 📋 Требования

### Системные требования:
- Docker Engine 20.10+
- Docker Compose 2.0+
- Минимум 1GB RAM
- 2GB свободного места на диске

### Проверка установки:
```bash
# Проверка Docker
docker --version
docker-compose --version

# Проверка доступности
docker run hello-world
```

## 🚀 Быстрый старт

### Шаг 1: Подготовка файлов
```bash
# Создай необходимые директории
mkdir -p data logs sessions backups monitoring

# Скопируй конфигурацию
cp combined_config_example.env .env

# Настрой .env файл
nano .env
```

### Шаг 2: Настройка .env файла
```env
# Обязательные настройки
API_ID=12345678
API_HASH=your_api_hash_here
SESSION_NAME=userbot_docker

# Настройки групп
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1001234567891
PARSING_GROUP_ID=-1001234567890

# Включи нужные функции
FORWARDING_ENABLED=true
PARSING_ENABLED=true
```

### Шаг 3: Запуск в Docker
```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

## 🔧 Команды Docker

### Основные команды:
```bash
# Сборка образа
docker-compose build

# Запуск в фоне
docker-compose up -d

# Запуск с выводом логов
docker-compose up

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f telegram-userbot

# Вход в контейнер
docker-compose exec telegram-userbot bash

# Проверка статуса
docker-compose ps
```

### Команды для продакшена:
```bash
# Запуск production версии
docker-compose -f docker-compose.prod.yml up -d

# Создание бэкапа
docker-compose -f docker-compose.prod.yml run backup

# Мониторинг ресурсов
docker stats telegram-userbot-prod
```

## 📊 Мониторинг и логи

### Просмотр логов:
```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs telegram-userbot

# Следить за логами в реальном времени
docker-compose logs -f

# Последние 100 строк
docker-compose logs --tail=100
```

### Мониторинг ресурсов:
```bash
# Использование ресурсов
docker stats

# Информация о контейнере
docker inspect telegram-userbot

# Проверка здоровья
docker-compose ps
```

## 🔒 Безопасность

### Рекомендации по безопасности:
1. **Не включай .env в Git** - используй .gitignore
2. **Ограничивай доступ** - используй volumes только для чтения
3. **Регулярно обновляй** - обновляй базовые образы
4. **Мониторь логи** - следи за подозрительной активностью

### Проверка безопасности:
```bash
# Сканирование уязвимостей
docker scan telegram-userbot

# Проверка конфигурации
docker-compose config

# Аудит зависимостей
docker run --rm -v $(pwd):/app python:3.11-slim bash -c "cd /app && pip-audit"
```

## 💾 Управление данными

### Структура volumes:
```
./data/          # Парсинг данные
./logs/          # Логи приложения
./sessions/      # Telegram сессии
./backups/       # Бэкапы данных
./monitoring/    # Файлы мониторинга
```

### Бэкап данных:
```bash
# Создание бэкапа
docker-compose -f docker-compose.prod.yml run backup

# Восстановление из бэкапа
tar -xzf backups/userbot_data_20240115_143000.tar.gz -C data/

# Автоматический бэкап (cron)
0 2 * * * cd /path/to/userbot && docker-compose -f docker-compose.prod.yml run backup
```

## 🛠️ Разработка с Docker

### Отладка:
```bash
# Запуск в режиме отладки
docker-compose up --build

# Вход в контейнер для отладки
docker-compose exec telegram-userbot bash

# Просмотр файлов в контейнере
docker-compose exec telegram-userbot ls -la /app
```

### Тестирование:
```bash
# Запуск тестов в контейнере
docker-compose exec telegram-userbot python -m pytest

# Проверка конфигурации
docker-compose exec telegram-userbot python -c "from config import Config; print('Config OK')"
```

## 📈 Production развертывание

### Подготовка к продакшену:
```bash
# Создай production конфигурацию
cp docker-compose.prod.yml docker-compose.yml

# Настрой переменные окружения
export DOCKER_ENV=production

# Запуск production версии
docker-compose up -d
```

### Мониторинг продакшена:
```bash
# Проверка здоровья
docker-compose ps

# Мониторинг ресурсов
docker stats

# Просмотр логов
docker-compose logs -f --tail=100
```

## ⚠️ Устранение проблем

### Частые проблемы:

#### Проблема 1: "Permission denied"
```bash
# Решение: исправь права доступа
sudo chown -R $USER:$USER data logs sessions
chmod 755 data logs sessions
```

#### Проблема 2: "Container exits immediately"
```bash
# Проверь логи
docker-compose logs telegram-userbot

# Проверь .env файл
docker-compose exec telegram-userbot cat /app/.env
```

#### Проблема 3: "Out of memory"
```bash
# Увеличь лимиты в docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G
```

#### Проблема 4: "Session file not found"
```bash
# Создай сессию локально
python main.py

# Скопируй файл сессии
cp *.session sessions/
```

## 🔄 Обновление

### Обновление кода:
```bash
# Остановка контейнеров
docker-compose down

# Обновление кода
git pull

# Пересборка и запуск
docker-compose up -d --build
```

### Обновление зависимостей:
```bash
# Обновление requirements.txt
docker-compose exec telegram-userbot pip freeze > requirements.txt

# Пересборка с новыми зависимостями
docker-compose build --no-cache
docker-compose up -d
```

## 📋 Чек-лист развертывания

### Перед запуском:
- [ ] Docker и Docker Compose установлены
- [ ] .env файл настроен
- [ ] API_ID и API_HASH указаны
- [ ] ID групп настроены
- [ ] Директории созданы (data, logs, sessions)
- [ ] Права доступа настроены

### После запуска:
- [ ] Контейнер запущен без ошибок
- [ ] Логи показывают успешное подключение
- [ ] Бот отвечает на команды
- [ ] Пересылка работает
- [ ] Парсинг работает (если включен)
- [ ] Данные сохраняются в volumes

## 🎯 Полезные команды

### Управление:
```bash
# Быстрый перезапуск
docker-compose restart telegram-userbot

# Очистка неиспользуемых ресурсов
docker system prune -f

# Просмотр использования диска
docker system df

# Экспорт данных
docker-compose exec telegram-userbot python -c "from parser_example import MessageParser; print('Parser ready')"
```

### Отладка:
```bash
# Проверка конфигурации
docker-compose config

# Проверка сетевых подключений
docker network ls
docker network inspect userbot_userbot-network

# Проверка volumes
docker volume ls
docker volume inspect userbot_userbot_data
```

## 💡 Советы

### Оптимизация:
1. **Используй .dockerignore** - ускоряет сборку
2. **Многоэтапная сборка** - уменьшает размер образа
3. **Кэширование pip** - ускоряет установку зависимостей
4. **Ограничение ресурсов** - предотвращает перегрузку

### Безопасность:
1. **Не используй root** - создавай пользователя в контейнере
2. **Сканируй образы** - регулярно проверяй уязвимости
3. **Обновляй зависимости** - следи за security patches
4. **Логируй все** - сохраняй логи для аудита

### Производительность:
1. **Используй volumes** - для персистентных данных
2. **Ограничивай ресурсы** - предотвращай перегрузку
3. **Мониторь использование** - следи за потреблением ресурсов
4. **Оптимизируй образ** - уменьшай размер Dockerfile

## 🎯 Итог

Docker обеспечивает:
- ✅ **Изоляцию** - бот работает в отдельном окружении
- ✅ **Портативность** - работает на любой системе с Docker
- ✅ **Воспроизводимость** - одинаковое поведение везде
- ✅ **Масштабируемость** - легко развертывать и обновлять
- ✅ **Мониторинг** - встроенные инструменты для отслеживания 