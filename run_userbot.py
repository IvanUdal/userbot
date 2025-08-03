#!/usr/bin/env python3
"""
Простой скрипт для запуска Telegram Userbot
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Проверяем наличие необходимых переменных
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

if not api_id or not api_hash:
    print("❌ Ошибка: API_ID и API_HASH должны быть установлены в .env файле")
    sys.exit(1)

print("🚀 Запуск Telegram Userbot...")
print(f"API_ID: {api_id}")
print(f"API_HASH: {api_hash[:10]}...")

# Импортируем и запускаем основной модуль
try:
    from main_pipeline import main
    asyncio.run(main())
except KeyboardInterrupt:
    print("\n🛑 Получен сигнал остановки")
except Exception as e:
    print(f"❌ Ошибка: {e}")
    sys.exit(1) 