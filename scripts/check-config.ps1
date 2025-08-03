# Script для проверки конфигурации Telegram Userbot
# Проверяет .env файл и зависимости

Write-Host "Проверка конфигурации Telegram Userbot..." -ForegroundColor Green

# 1. Проверяем наличие .env файла
Write-Host "`nПроверка файлов конфигурации:" -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "OK .env файл найден" -ForegroundColor Green
} elseif (Test-Path "my.env") {
    Write-Host "WARNING Найден my.env, но нужен .env" -ForegroundColor Yellow
    Write-Host "   Скопируйте my.env в .env: copy my.env .env" -ForegroundColor Cyan
} else {
    Write-Host "ERROR .env файл не найден!" -ForegroundColor Red
    Write-Host "   Создайте .env файл на основе my.env" -ForegroundColor Cyan
}

# 2. Проверяем основные файлы
Write-Host "`nПроверка основных файлов:" -ForegroundColor Yellow
$required_files = @("config.py", "main_pipeline.py", "requirements.txt")
foreach ($file in $required_files) {
    if (Test-Path $file) {
        Write-Host "OK $file найден" -ForegroundColor Green
    } else {
        Write-Host "ERROR $file не найден!" -ForegroundColor Red
    }
}

# 3. Проверяем зависимости
Write-Host "`nПроверка зависимостей:" -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "OK Виртуальное окружение найдено" -ForegroundColor Green
    
    # Активируем venv и проверяем зависимости
    & "venv\Scripts\python.exe" -c "
import sys
import importlib

required_packages = [
    'telethon', 'python-dotenv', 'pandas', 'matplotlib', 
    'aiofiles', 'sqlalchemy', 'requests'
]

missing_packages = []
for package in required_packages:
    try:
        importlib.import_module(package)
        print(f'OK {package}')
    except ImportError:
        missing_packages.append(package)
        print(f'ERROR {package}')

if missing_packages:
    print(f'Missing packages: {', '.join(missing_packages)}')
    print('Install them: pip install -r requirements.txt')
else:
    print('All main dependencies installed')
"
} else {
    Write-Host "ERROR Виртуальное окружение не найдено!" -ForegroundColor Red
    Write-Host "   Создайте venv: python -m venv venv" -ForegroundColor Cyan
    Write-Host "   Активируйте: venv\Scripts\activate" -ForegroundColor Cyan
    Write-Host "   Установите зависимости: pip install -r requirements.txt" -ForegroundColor Cyan
}

# 4. Проверяем конфигурацию
Write-Host "`nПроверка конфигурации:" -ForegroundColor Yellow
if (Test-Path ".env") {
    & "venv\Scripts\python.exe" -c "
import os
from dotenv import load_dotenv

load_dotenv()

# Проверяем обязательные параметры
required_vars = ['API_ID', 'API_HASH']
missing_vars = []

for var in required_vars:
    value = os.getenv(var)
    if value and value != 'your_api_hash_here':
        print(f'OK {var}')
    else:
        missing_vars.append(var)
        print(f'ERROR {var}')

if missing_vars:
    print(f'Not configured: {', '.join(missing_vars)}')
    print('Configure them in .env file')
else:
    print('Main parameters configured')

# Проверяем группы
source_group = os.getenv('SOURCE_GROUP_ID')
target_group = os.getenv('TARGET_GROUP_ID')
parsing_group = os.getenv('PARSING_GROUP_ID')

if source_group and target_group:
    print('OK Forwarding groups configured')
else:
    print('WARNING Forwarding groups not configured')

if parsing_group:
    print('OK Parsing group configured')
else:
    print('WARNING Parsing group not configured')
"
}

Write-Host "`nРекомендации:" -ForegroundColor Green
Write-Host "1. Убедитесь, что .env файл содержит правильные API_ID и API_HASH" -ForegroundColor Cyan
Write-Host "2. Настройте ID групп для пересылки и парсинга" -ForegroundColor Cyan
Write-Host "3. Выберите нужные функции (пересылка/парсинг)" -ForegroundColor Cyan
Write-Host "4. Запустите бота: python main_pipeline.py" -ForegroundColor Cyan

Write-Host "`nПроверка завершена!" -ForegroundColor Green 