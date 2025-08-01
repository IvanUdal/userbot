# PowerShell скрипт для автоматической настройки Docker окружения
# для Telegram Userbot на Windows

param(
    [switch]$Force
)

# Функция для вывода сообщений с цветом
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    $Colors = @{
        "Red" = "Red"
        "Green" = "Green" 
        "Yellow" = "Yellow"
        "Blue" = "Cyan"
        "White" = "White"
    }
    
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "[INFO] $Message" "Blue"
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "[SUCCESS] $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "[WARNING] $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "[ERROR] $Message" "Red"
}

# Проверка наличия Docker
function Test-Docker {
    Write-Info "Проверка Docker..."
    
    try {
        $dockerVersion = docker --version
        Write-Success "Docker найден: $dockerVersion"
    }
    catch {
        Write-Error "Docker не установлен. Установите Docker Desktop и попробуйте снова."
        exit 1
    }
    
    try {
        $composeVersion = docker-compose --version
        Write-Success "Docker Compose найден: $composeVersion"
    }
    catch {
        Write-Error "Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
        exit 1
    }
}

# Создание необходимых директорий
function New-Directories {
    Write-Info "Создание директорий..."
    
    $directories = @(
        "data",
        "logs", 
        "sessions",
        "backups",
        "monitoring",
        "notebooks",
        "grafana",
        "prometheus"
    )
    
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Success "Создана директория: $dir"
        }
        else {
            Write-Info "Директория уже существует: $dir"
        }
    }
}

# Настройка .env файла
function Set-EnvFile {
    Write-Info "Настройка .env файла..."
    
    if (!(Test-Path ".env")) {
        if (Test-Path "combined_config_example.env") {
            Copy-Item "combined_config_example.env" ".env"
            Write-Success ".env файл создан из примера"
        }
        else {
            Write-Warning "Файл combined_config_example.env не найден. Создайте .env вручную."
        }
    }
    else {
        Write-Info ".env файл уже существует"
    }
    
    # Проверка обязательных переменных
    if (Test-Path ".env") {
        $envContent = Get-Content ".env"
        if ($envContent -notmatch "API_ID=" -or $envContent -notmatch "API_HASH=") {
            Write-Warning "В .env файле отсутствуют API_ID или API_HASH. Настройте их вручную."
        }
    }
}

# Сборка Docker образа
function Build-DockerImage {
    Write-Info "Сборка Docker образа..."
    
    try {
        docker-compose build
        Write-Success "Docker образ собран"
    }
    catch {
        Write-Error "Ошибка при сборке Docker образа"
        exit 1
    }
}

# Проверка конфигурации
function Test-Config {
    Write-Info "Проверка конфигурации Docker Compose..."
    
    try {
        docker-compose config | Out-Null
        Write-Success "Конфигурация корректна"
    }
    catch {
        Write-Error "Ошибка в конфигурации Docker Compose"
        exit 1
    }
}

# Создание скриптов управления
function New-ManagementScripts {
    Write-Info "Создание скриптов управления..."
    
    # Создаем директорию scripts если её нет
    if (!(Test-Path "scripts")) {
        New-Item -ItemType Directory -Path "scripts" -Force | Out-Null
    }
    
    # Скрипт запуска
    $startScript = @"
# PowerShell скрипт для запуска Telegram Userbot
Write-Host "🚀 Запуск Telegram Userbot..." -ForegroundColor Green
docker-compose up -d
Write-Host "✅ Бот запущен. Логи: docker-compose logs -f" -ForegroundColor Green
"@
    Set-Content "scripts/start.ps1" $startScript
    
    # Скрипт остановки
    $stopScript = @"
# PowerShell скрипт для остановки Telegram Userbot
Write-Host "🛑 Остановка Telegram Userbot..." -ForegroundColor Yellow
docker-compose down
Write-Host "✅ Бот остановлен" -ForegroundColor Green
"@
    Set-Content "scripts/stop.ps1" $stopScript
    
    # Скрипт перезапуска
    $restartScript = @"
# PowerShell скрипт для перезапуска Telegram Userbot
Write-Host "🔄 Перезапуск Telegram Userbot..." -ForegroundColor Blue
docker-compose restart
Write-Host "✅ Бот перезапущен" -ForegroundColor Green
"@
    Set-Content "scripts/restart.ps1" $restartScript
    
    # Скрипт просмотра логов
    $logsScript = @"
# PowerShell скрипт для просмотра логов Telegram Userbot
Write-Host "📋 Логи Telegram Userbot..." -ForegroundColor Cyan
docker-compose logs -f
"@
    Set-Content "scripts/logs.ps1" $logsScript
    
    # Скрипт бэкапа
    $backupScript = @"
# PowerShell скрипт для создания бэкапа
Write-Host "💾 Создание бэкапа..." -ForegroundColor Magenta
docker-compose -f docker-compose.prod.yml run backup
Write-Host "✅ Бэкап создан в папке backups/" -ForegroundColor Green
"@
    Set-Content "scripts/backup.ps1" $backupScript
    
    Write-Success "Скрипты управления созданы в папке scripts/"
}

# Создание README для Docker
function New-DockerReadme {
    Write-Info "Создание документации..."
    
    $readmeContent = @"
# 🐳 Docker - Быстрый старт

## 🚀 Запуск

```powershell
# Запуск в фоне
.\scripts\start.ps1

# Просмотр логов
.\scripts\logs.ps1

# Остановка
.\scripts\stop.ps1

# Перезапуск
.\scripts\restart.ps1

# Бэкап данных
.\scripts\backup.ps1
```

## 📋 Команды Docker

```powershell
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

```powershell
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
"@
    
    Set-Content "DOCKER_README.md" $readmeContent
    Write-Success "Документация создана"
}

# Основная функция
function Main {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "🐳 Настройка Docker для Telegram Userbot" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    
    Test-Docker
    New-Directories
    Set-EnvFile
    Build-DockerImage
    Test-Config
    New-ManagementScripts
    New-DockerReadme
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Success "Настройка завершена!"
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Следующие шаги:" -ForegroundColor White
    Write-Host "1. Настройте .env файл (API_ID, API_HASH, ID групп)" -ForegroundColor White
    Write-Host "2. Запустите бота: .\scripts\start.ps1" -ForegroundColor White
    Write-Host "3. Проверьте логи: .\scripts\logs.ps1" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Документация: DOCKER_README.md" -ForegroundColor White
    Write-Host "🔧 Скрипты управления: scripts\" -ForegroundColor White
    Write-Host ""
}

# Запуск основной функции
Main 