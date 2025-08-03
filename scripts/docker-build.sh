#!/bin/bash

# Скрипт для сборки Docker с автоматическим fallback
# Автор: Telegram Userbot Team

echo "🚀 Начинаем сборку Docker образа..."

# Пробуем основной Dockerfile
echo "📦 Пробуем основной Dockerfile..."
if docker-compose build --no-cache; then
    echo "✅ Сборка успешно завершена!"
    exit 0
else
    echo "❌ Ошибка при сборке основного Dockerfile"
fi

# Если основной не сработал, пробуем упрощенный
echo "🔄 Переключаемся на упрощенный Dockerfile..."

# Временно переименовываем файлы
if [ -f "Dockerfile" ]; then
    mv Dockerfile Dockerfile.main
fi
if [ -f "Dockerfile.simple" ]; then
    mv Dockerfile.simple Dockerfile
fi

if docker-compose build --no-cache; then
    echo "✅ Сборка упрощенного Dockerfile успешно завершена!"
    
    # Возвращаем оригинальные имена
    if [ -f "Dockerfile" ]; then
        mv Dockerfile Dockerfile.simple
    fi
    if [ -f "Dockerfile.main" ]; then
        mv Dockerfile.main Dockerfile
    fi
    
    exit 0
else
    echo "❌ Ошибка при сборке упрощенного Dockerfile"
fi

# Возвращаем оригинальные имена в случае ошибки
if [ -f "Dockerfile" ]; then
    mv Dockerfile Dockerfile.simple
fi
if [ -f "Dockerfile.main" ]; then
    mv Dockerfile.main Dockerfile
fi

echo "💥 Все попытки сборки завершились неудачей!"
echo "🔧 Проверьте подключение к интернету и попробуйте позже"
exit 1 