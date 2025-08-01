# Git Cleanup Script для Telegram Userbot
# Очищает текущее состояние Git и добавляет новые файлы

Write-Host "🧹 Очистка Git состояния..." -ForegroundColor Green

# 1. Удаляем venv из отслеживания (если отслеживается)
Write-Host "📦 Удаляем venv из отслеживания..." -ForegroundColor Yellow
git rm -r --cached venv/ 2>$null

# 2. Добавляем новые файлы
Write-Host "📁 Добавляем новые файлы..." -ForegroundColor Yellow

# Основные файлы
git add main_pipeline.py
git add config.py
git add requirements.txt
git add Dockerfile
git add docker-compose.yml
git add docker-compose.dev.yml
git add docker-compose.prod.yml
git add .dockerignore

# Модули
git add modules/
git add config/

# Документация
git add documentation/

# Скрипты
git add scripts/

# Примеры
git add combined_config_example.env
git add config_example.py
git add parser_example.py

# Архитектурные документы
git add MULTI_USER_ARCHITECTURE.md

# 3. Удаляем старые файлы
Write-Host "🗑️ Удаляем старые файлы..." -ForegroundColor Yellow
git rm main.py 2>$null
git rm README.md 2>$null
git rm env_example.txt 2>$null
git rm parsing_config_example.env 2>$null

# 4. Показываем статус
Write-Host "📊 Статус Git:" -ForegroundColor Green
git status

Write-Host "`n✅ Очистка завершена!" -ForegroundColor Green
Write-Host "Теперь можете сделать коммит:" -ForegroundColor Cyan
Write-Host "git commit -m 'feat: миграция на новую архитектуру пайплайнов'" -ForegroundColor White 