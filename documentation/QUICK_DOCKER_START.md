# 🚀 Быстрый запуск Docker

## 📋 Требования

- Docker Desktop установлен
- PowerShell или Command Prompt
- Минимум 2GB свободного места

## ⚡ Быстрый старт (3 шага)

### Шаг 1: Настройка
```powershell
# Запусти скрипт настройки
.\scripts\docker-setup.ps1
```

### Шаг 2: Конфигурация
```powershell
# Открой .env файл и настрой:
notepad .env

# Обязательно укажи:
# API_ID=12345678
# API_HASH=your_api_hash_here
# SOURCE_GROUP_ID=-1001234567890
# TARGET_GROUP_ID=-1001234567891
```

### Шаг 3: Запуск
```powershell
# Запусти бота
.\scripts\start.ps1

# Проверь логи
.\scripts\logs.ps1
```

## 🔧 Основные команды

```powershell
# Запуск
.\scripts\start.ps1

# Остановка
.\scripts\stop.ps1

# Перезапуск
.\scripts\restart.ps1

# Логи
.\scripts\logs.ps1

# Бэкап
.\scripts\backup.ps1
```

## 📊 Мониторинг

- **Логи**: `.\scripts\logs.ps1`
- **Статус**: `docker-compose ps`
- **Ресурсы**: `docker stats`

## ⚠️ Решение проблем

### Проблема: "Docker не найден"
```powershell
# Установи Docker Desktop
# https://www.docker.com/products/docker-desktop
```

### Проблема: "Permission denied"
```powershell
# Запусти PowerShell от имени администратора
# Или настрой права доступа к папкам
```

### Проблема: "Container exits"
```powershell
# Проверь .env файл
# Проверь логи: .\scripts\logs.ps1
```

## 🎯 Проверка работы

1. **Бот запущен**: `docker-compose ps` показывает "Up"
2. **Логи показывают подключение**: "Connected to Telegram"
3. **Команды работают**: отправь `.ping` в группу
4. **Пересылка работает**: отправь сообщение в исходную группу

## 📚 Дополнительно

- **Полная документация**: `DOCKER_SETUP.md`
- **Разработка**: `docker-compose -f docker-compose.dev.yml up`
- **Продакшен**: `docker-compose -f docker-compose.prod.yml up -d` 