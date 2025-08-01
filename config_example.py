# Примеры конфигураций для разных сценариев использования
# Скопируйте нужную конфигурацию в .env файл

# ===========================================
# ПРИМЕР 1: Базовая пересылка всех сообщений
# ===========================================
"""
# .env файл - Базовая пересылка всех сообщений

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1001234567891

# Пересылать все типы сообщений
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=true
FORWARD_VOICE=true
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 2: Пересылка только текстовых сообщений
# ===========================================
"""
# .env файл - Пересылка только текстовых сообщений

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1001234567891

# Пересылать только текст
FORWARD_TEXT=true
FORWARD_MEDIA=false
FORWARD_STICKERS=false
FORWARD_VOICE=false
FORWARD_DOCUMENTS=false

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 3: Пересылка новостей (текст + медиа)
# ===========================================
"""
# .env файл - Пересылка новостей (текст + медиа)

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Группа с новостями
TARGET_GROUP_ID=-1001234567891  # Группа для пересылки

# Пересылать текст и медиа, но не стикеры
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=false
FORWARD_VOICE=true
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 4: Пересылка документов и файлов
# ===========================================
"""
# .env файл - Пересылка документов и файлов

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1001234567891

# Пересылать только документы и файлы
FORWARD_TEXT=false
FORWARD_MEDIA=false
FORWARD_STICKERS=false
FORWARD_VOICE=false
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 5: Пересылка с отключенной информацией
# ===========================================
"""
# .env файл - Пересылка с отключенной информацией

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1001234567891

# Пересылать все типы сообщений
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=true
FORWARD_VOICE=true
FORWARD_DOCUMENTS=true

# НЕ добавлять информацию о пересылке
ADD_FORWARD_INFO=false
"""

# ===========================================
# ПРИМЕР 6: Отключенная пересылка (для тестирования)
# ===========================================
"""
# .env файл - Отключенная пересылка (для тестирования)

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=false  # Пересылка отключена

# ID групп для пересылки (не важны при отключенной пересылке)
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1001234567891

# Настройки фильтров (не важны при отключенной пересылке)
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=true
FORWARD_VOICE=true
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 7: Множественные группы
# ===========================================
"""
# .env файл - Множественные группы (требует изменения кода)

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки (основная конфигурация)
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1001234567891

# Дополнительные группы (для расширения функционала)
# SOURCE_GROUP_2=-1001234567892
# TARGET_GROUP_2=-1001234567893

# Пересылать все типы сообщений
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=true
FORWARD_VOICE=true
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 8: Продакшн конфигурация
# ===========================================
"""
# .env файл - Продакшн конфигурация

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_prod
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890
TARGET_GROUP_ID=-1001234567891

# Пересылать все типы сообщений
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=true
FORWARD_VOICE=true
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 9: Мемы и развлечения
# ===========================================
"""
# .env файл - Мемы и развлечения

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_memes
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Группа с мемами
TARGET_GROUP_ID=-1001234567891  # Группа друзей

# Пересылать только медиа и стикеры
FORWARD_TEXT=false
FORWARD_MEDIA=true
FORWARD_STICKERS=true
FORWARD_VOICE=false
FORWARD_DOCUMENTS=false

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 10: Образовательный контент
# ===========================================
"""
# .env файл - Образовательный контент

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_education
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Образовательная группа
TARGET_GROUP_ID=-1001234567891  # Группа студентов

# Пересылать текст, медиа и документы
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=false
FORWARD_VOICE=true
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 11: Торговая площадка
# ===========================================
"""
# .env файл - Торговая площадка

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_marketplace
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Группа с товарами
TARGET_GROUP_ID=-1001234567891  # Группа покупателей

# Пересылать текст, медиа и документы
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=false
FORWARD_VOICE=false
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 12: Музыка и аудио
# ===========================================
"""
# .env файл - Музыка и аудио

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_music
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Группа с музыкой
TARGET_GROUP_ID=-1001234567891  # Группа слушателей

# Пересылать текст и голосовые сообщения
FORWARD_TEXT=true
FORWARD_MEDIA=false
FORWARD_STICKERS=false
FORWARD_VOICE=true
FORWARD_DOCUMENTS=false

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 13: Фотографии и искусство
# ===========================================
"""
# .env файл - Фотографии и искусство

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_art
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Группа с искусством
TARGET_GROUP_ID=-1001234567891  # Группа ценителей

# Пересылать только медиа
FORWARD_TEXT=false
FORWARD_MEDIA=true
FORWARD_STICKERS=false
FORWARD_VOICE=false
FORWARD_DOCUMENTS=false

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 14: Техническая поддержка
# ===========================================
"""
# .env файл - Техническая поддержка

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_support
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Группа поддержки
TARGET_GROUP_ID=-1001234567891  # Группа клиентов

# Пересылать текст, медиа и документы
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=false
FORWARD_VOICE=false
FORWARD_DOCUMENTS=true

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 15: Новости и СМИ
# ===========================================
"""
# .env файл - Новости и СМИ

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_news
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Новостная группа
TARGET_GROUP_ID=-1001234567891  # Группа подписчиков

# Пересылать текст и медиа
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=false
FORWARD_VOICE=false
FORWARD_DOCUMENTS=false

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 16: Спорт и активность
# ===========================================
"""
# .env файл - Спорт и активность

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_sport
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Спортивная группа
TARGET_GROUP_ID=-1001234567891  # Группа фанатов

# Пересылать текст, медиа и стикеры
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=true
FORWARD_VOICE=false
FORWARD_DOCUMENTS=false

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 17: Кулинария и рецепты
# ===========================================
"""
# .env файл - Кулинария и рецепты

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_cooking
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Группа с рецептами
TARGET_GROUP_ID=-1001234567891  # Группа кулинаров

# Пересылать текст и медиа
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=false
FORWARD_VOICE=false
FORWARD_DOCUMENTS=false

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# ПРИМЕР 18: Путешествия и туризм
# ===========================================
"""
# .env файл - Путешествия и туризм

# Telegram API данные
API_ID=12345678
API_HASH=your_api_hash_here

# Настройки сессии
SESSION_NAME=userbot_travel
CMD_PREFIX=.

# Настройки пересылки
FORWARDING_ENABLED=true

# ID групп для пересылки
SOURCE_GROUP_ID=-1001234567890  # Группа путешествий
TARGET_GROUP_ID=-1001234567891  # Группа туристов

# Пересылать текст и медиа
FORWARD_TEXT=true
FORWARD_MEDIA=true
FORWARD_STICKERS=false
FORWARD_VOICE=false
FORWARD_DOCUMENTS=false

# Добавлять информацию о пересылке
ADD_FORWARD_INFO=true
"""

# ===========================================
# КАК ИСПОЛЬЗОВАТЬ ЭТИ ПРИМЕРЫ
# ===========================================
"""
1. Выберите подходящий пример выше
2. Скопируйте содержимое между тройными кавычками
3. Создайте файл .env в корне проекта
4. Вставьте содержимое в .env файл
5. Замените API_ID, API_HASH и ID групп на ваши реальные данные
6. Запустите бота: python main.py

ВАЖНО:
- Файл .env НЕ должен попадать в Git (уже добавлен в .gitignore)
- Никогда не передавайте .env файл третьим лицам
- Регулярно обновляйте API ключи для безопасности
"""

# ===========================================
# ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ - ОПИСАНИЕ
# ===========================================
"""
ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ:
- API_ID: ваш Telegram API ID (число)
- API_HASH: ваш Telegram API Hash (строка)

ОПЦИОНАЛЬНЫЕ ПЕРЕМЕННЫЕ:
- SESSION_NAME: имя файла сессии (по умолчанию: userbot)
- CMD_PREFIX: префикс команд (по умолчанию: .)

НАСТРОЙКИ ПЕРЕСЫЛКИ:
- FORWARDING_ENABLED: включить/выключить пересылку (true/false)
- SOURCE_GROUP_ID: ID исходной группы (число)
- TARGET_GROUP_ID: ID целевой группы (число)

ФИЛЬТРЫ ПЕРЕСЫЛКИ:
- FORWARD_TEXT: пересылать текстовые сообщения (true/false)
- FORWARD_MEDIA: пересылать медиа (фото, видео) (true/false)
- FORWARD_STICKERS: пересылать стикеры (true/false)
- FORWARD_VOICE: пересылать голосовые сообщения (true/false)
- FORWARD_DOCUMENTS: пересылать документы/файлы (true/false)
- ADD_FORWARD_INFO: добавлять информацию о пересылке (true/false)

ПРИМЕРЫ ЗНАЧЕНИЙ:
- true/false для булевых переменных
- Числа для ID (например: 12345678)
- Строки для API_HASH и других текстовых значений
""" 