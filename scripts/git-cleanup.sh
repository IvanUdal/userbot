#!/bin/bash

# Git Cleanup Script для Telegram Userbot
# Очищает текущее состояние Git и добавляет новые файлы

echo "🧹 Очистка Git состояния..."

# 1. Удаляем venv из отслеживания (если отслеживается)
echo "📦 Удаляем venv из отслеживания..."
git rm -r --cached venv/ 2>/dev/null

# 2. Добавляем новые файлы
echo "📁 Добавляем новые файлы..."

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
echo "🗑️ Удаляем старые файлы..."
git rm main.py 2>/dev/null
git rm README.md 2>/dev/null
git rm env_example.txt 2>/dev/null
git rm parsing_config_example.env 2>/dev/null

# 4. Показываем статус
echo "📊 Статус Git:"
git status

echo ""
echo "✅ Очистка завершена!"
echo "Теперь можете сделать коммит:"
echo "git commit -m 'feat: миграция на новую архитектуру пайплайнов'" 