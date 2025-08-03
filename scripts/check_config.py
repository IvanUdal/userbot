#!/usr/bin/env python3
"""
Script для проверки конфигурации Telegram Userbot
Проверяет .env файл и зависимости
"""

import os
import sys
import importlib
from pathlib import Path

def check_env_file():
    """Проверяет наличие и корректность .env файла"""
    print("📁 Проверка файлов конфигурации:")
    
    if Path(".env").exists():
        print("✅ .env файл найден")
        return True
    elif Path("my.env").exists():
        print("⚠️  Найден my.env, но нужен .env")
        print("   Скопируйте my.env в .env: copy my.env .env")
        return False
    else:
        print("❌ .env файл не найден!")
        print("   Создайте .env файл на основе my.env")
        return False

def check_required_files():
    """Проверяет наличие основных файлов"""
    print("\n📄 Проверка основных файлов:")
    
    required_files = ["config.py", "main_pipeline.py", "requirements.txt"]
    all_exist = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} найден")
        else:
            print(f"❌ {file} не найден!")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Проверяет установленные зависимости"""
    print("\n📦 Проверка зависимостей:")
    
    if not Path("venv").exists():
        print("❌ Виртуальное окружение не найдено!")
        print("   Создайте venv: python -m venv venv")
        print("   Активируйте: venv\\Scripts\\activate")
        print("   Установите зависимости: pip install -r requirements.txt")
        return False
    
    print("✅ Виртуальное окружение найдено")
    
    required_packages = [
        'telethon', 'python-dotenv', 'pandas', 'matplotlib', 
        'aiofiles', 'sqlalchemy', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Отсутствуют пакеты: {', '.join(missing_packages)}")
        print("Установите их: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ Все основные зависимости установлены")
        return True

def check_configuration():
    """Проверяет настройки в .env файле"""
    print("\n⚙️  Проверка конфигурации:")
    
    if not Path(".env").exists():
        print("❌ .env файл не найден для проверки конфигурации")
        return False
    
    # Загружаем переменные окружения
    from dotenv import load_dotenv
    load_dotenv()
    
    # Проверяем обязательные параметры
    required_vars = ['API_ID', 'API_HASH']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value and value != 'your_api_hash_here':
            print(f"✅ {var}")
        else:
            missing_vars.append(var)
            print(f"❌ {var}")
    
    if missing_vars:
        print(f"\n⚠️  Не настроены: {', '.join(missing_vars)}")
        print("Настройте их в .env файле")
        return False
    else:
        print("\n✅ Основные параметры настроены")
    
    # Проверяем группы
    source_group = os.getenv('SOURCE_GROUP_ID')
    target_group = os.getenv('TARGET_GROUP_ID')
    parsing_group = os.getenv('PARSING_GROUP_ID')
    
    if source_group and target_group:
        print("✅ Группы для пересылки настроены")
    else:
        print("⚠️  Группы для пересылки не настроены")
    
    if parsing_group:
        print("✅ Группа для парсинга настроена")
    else:
        print("⚠️  Группа для парсинга не настроена")
    
    return True

def main():
    """Основная функция проверки"""
    print("🔍 Проверка конфигурации Telegram Userbot...")
    
    # Проверяем все компоненты
    env_ok = check_env_file()
    files_ok = check_required_files()
    deps_ok = check_dependencies()
    config_ok = check_configuration()
    
    print("\n🎯 Рекомендации:")
    print("1. Убедитесь, что .env файл содержит правильные API_ID и API_HASH")
    print("2. Настройте ID групп для пересылки и парсинга")
    print("3. Выберите нужные функции (пересылка/парсинг)")
    print("4. Запустите бота: python main_pipeline.py")
    
    if all([env_ok, files_ok, deps_ok, config_ok]):
        print("\n✅ Все проверки пройдены успешно!")
        return 0
    else:
        print("\n⚠️  Есть проблемы, которые нужно исправить")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 