import os
import asyncio
from dotenv import load_dotenv
from typing import Optional, List

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    """Класс для управления конфигурацией Telegram userbot"""
    
    def __init__(self):
        # Основные настройки Telegram API
        self.api_id: Optional[int] = None
        self.api_hash: Optional[str] = None
        self.session_name: str = "userbot"
        self.cmd_prefix: str = "."
        
        # Настройки пересылки
        self.forwarding_enabled: bool = False
        self.source_group_id: Optional[int] = None
        self.target_group_id: Optional[int] = None
        self.forward_text: bool = True
        self.forward_media: bool = True
        self.forward_stickers: bool = True
        self.forward_voice: bool = True
        self.forward_documents: bool = True
        self.add_forward_info: bool = True
        
        # Настройки парсинга
        self.parsing_enabled: bool = False
        self.parsing_group_id: Optional[int] = None
        self.parse_text: bool = True
        self.parse_media: bool = True
        self.parse_documents: bool = True
        self.parse_voice: bool = True
        self.parse_stickers: bool = True
        self.parse_bots: bool = False
        self.parse_metadata: bool = True
        self.parse_reactions: bool = True
        self.parse_hashtags: bool = True
        self.parse_urls: bool = True
        self.parse_forwards: bool = True
        self.parse_replies: bool = True
        self.parse_buttons: bool = True  # Добавляем парсинг кнопок
        
        # Настройки парсинга ботов
        self.parse_bot_messages: bool = False
        self.parse_bot_commands: bool = False
        self.parse_bot_responses: bool = False
        self.parse_bot_buttons: bool = False
        self.parse_bot_media: bool = False
        
        # Анализ ботов
        self.analyze_bot_patterns: bool = False
        self.analyze_bot_commands: bool = False
        self.analyze_bot_interactions: bool = False
        
        # Фильтрация ботов
        self.bot_filter_enabled: bool = False
        self.allowed_bot_ids: List[int] = []
        self.blocked_bot_ids: List[int] = []
        
        # Настройки сохранения данных
        self.save_to_file: bool = True
        self.save_to_database: bool = False
        self.save_to_csv: bool = False
        self.data_directory: str = "data"
        self.parsed_messages_file: str = "parsed_messages.json"
        self.export_csv_file: str = "export.csv"
        self.database_url: str = "sqlite:///parsed_messages.db"
        self.database_type: str = "sqlite"
        
        # Настройки производительности
        self.max_messages_per_hour: int = 1000
        self.max_file_size_mb: int = 100
        self.backup_interval_hours: int = 24
        self.cache_enabled: bool = True
        self.cache_size_mb: int = 50
        
        # Настройки безопасности
        self.encrypt_data: bool = False
        self.encryption_key: Optional[str] = None
        self.log_level: str = "INFO"
        self.log_to_file: bool = True
        self.log_file: str = "userbot.log"
        self.allowed_users: List[int] = []
        self.admin_only: bool = False
        
        # Настройки уведомлений
        self.notify_start: bool = True
        self.notify_stop: bool = True
        self.notify_errors: bool = True
        self.notify_stats: bool = True
        self.notification_chat_id: Optional[int] = None
    
    async def load_from_env(self) -> None:
        """Загрузка конфигурации из переменных окружения"""
        # Загружаем .env файл
        load_dotenv()
        
        # Основные настройки Telegram API
        self.api_id = int(os.getenv("API_ID", "0"))
        self.api_hash = os.getenv("API_HASH", "")
        self.session_name = os.getenv("SESSION_NAME", "userbot")
        self.cmd_prefix = os.getenv("CMD_PREFIX", ".")
        
        # Настройки пересылки
        self.forwarding_enabled = os.getenv("FORWARDING_ENABLED", "false").lower() == "true"
        self.source_group_id = int(os.getenv("SOURCE_GROUP_ID", "0")) if os.getenv("SOURCE_GROUP_ID") else None
        self.target_group_id = int(os.getenv("TARGET_GROUP_ID", "0")) if os.getenv("TARGET_GROUP_ID") else None
        self.forward_text = os.getenv("FORWARD_TEXT", "true").lower() == "true"
        self.forward_media = os.getenv("FORWARD_MEDIA", "true").lower() == "true"
        self.forward_stickers = os.getenv("FORWARD_STICKERS", "true").lower() == "true"
        self.forward_voice = os.getenv("FORWARD_VOICE", "true").lower() == "true"
        self.forward_documents = os.getenv("FORWARD_DOCUMENTS", "true").lower() == "true"
        self.add_forward_info = os.getenv("ADD_FORWARD_INFO", "true").lower() == "true"
        
        # Настройки парсинга
        self.parsing_enabled = os.getenv("PARSING_ENABLED", "false").lower() == "true"
        self.parsing_group_id = int(os.getenv("PARSING_GROUP_ID", "0")) if os.getenv("PARSING_GROUP_ID") else None
        self.parse_text = os.getenv("PARSE_TEXT", "true").lower() == "true"
        self.parse_media = os.getenv("PARSE_MEDIA", "true").lower() == "true"
        self.parse_documents = os.getenv("PARSE_DOCUMENTS", "true").lower() == "true"
        self.parse_voice = os.getenv("PARSE_VOICE", "true").lower() == "true"
        self.parse_stickers = os.getenv("PARSE_STICKERS", "true").lower() == "true"
        self.parse_bots = os.getenv("PARSE_BOTS", "false").lower() == "true"
        self.parse_metadata = os.getenv("PARSE_METADATA", "true").lower() == "true"
        self.parse_reactions = os.getenv("PARSE_REACTIONS", "true").lower() == "true"
        self.parse_hashtags = os.getenv("PARSE_HASHTAGS", "true").lower() == "true"
        self.parse_urls = os.getenv("PARSE_URLS", "true").lower() == "true"
        self.parse_forwards = os.getenv("PARSE_FORWARDS", "true").lower() == "true"
        self.parse_replies = os.getenv("PARSE_REPLIES", "true").lower() == "true"
        self.parse_buttons = os.getenv("PARSE_BUTTONS", "true").lower() == "true"  # Добавляем парсинг кнопок
        
        # Настройки парсинга ботов
        self.parse_bot_messages = os.getenv("PARSE_BOT_MESSAGES", "false").lower() == "true"
        self.parse_bot_commands = os.getenv("PARSE_BOT_COMMANDS", "false").lower() == "true"
        self.parse_bot_responses = os.getenv("PARSE_BOT_RESPONSES", "false").lower() == "true"
        self.parse_bot_buttons = os.getenv("PARSE_BOT_BUTTONS", "false").lower() == "true"
        self.parse_bot_media = os.getenv("PARSE_BOT_MEDIA", "false").lower() == "true"
        
        # Анализ ботов
        self.analyze_bot_patterns = os.getenv("ANALYZE_BOT_PATTERNS", "false").lower() == "true"
        self.analyze_bot_commands = os.getenv("ANALYZE_BOT_COMMANDS", "false").lower() == "true"
        self.analyze_bot_interactions = os.getenv("ANALYZE_BOT_INTERACTIONS", "false").lower() == "true"
        
        # Фильтрация ботов
        self.bot_filter_enabled = os.getenv("BOT_FILTER_ENABLED", "false").lower() == "true"
        allowed_bots_str = os.getenv("ALLOWED_BOT_IDS", "")
        if allowed_bots_str:
            self.allowed_bot_ids = [int(bid.strip()) for bid in allowed_bots_str.split(",") if bid.strip()]
        else:
            self.allowed_bot_ids = []
        
        blocked_bots_str = os.getenv("BLOCKED_BOT_IDS", "")
        if blocked_bots_str:
            self.blocked_bot_ids = [int(bid.strip()) for bid in blocked_bots_str.split(",") if bid.strip()]
        else:
            self.blocked_bot_ids = []
        
        # Настройки сохранения данных
        self.save_to_file = os.getenv("SAVE_TO_FILE", "true").lower() == "true"
        self.save_to_database = os.getenv("SAVE_TO_DATABASE", "false").lower() == "true"
        self.save_to_csv = os.getenv("SAVE_TO_CSV", "false").lower() == "true"
        self.data_directory = os.getenv("DATA_DIRECTORY", "data")
        self.parsed_messages_file = os.getenv("PARSED_MESSAGES_FILE", "parsed_messages.json")
        self.export_csv_file = os.getenv("EXPORT_CSV_FILE", "export.csv")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///parsed_messages.db")
        self.database_type = os.getenv("DATABASE_TYPE", "sqlite")
        
        # Настройки производительности
        self.max_messages_per_hour = int(os.getenv("MAX_MESSAGES_PER_HOUR", "1000"))
        self.max_file_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
        self.backup_interval_hours = int(os.getenv("BACKUP_INTERVAL_HOURS", "24"))
        self.cache_enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.cache_size_mb = int(os.getenv("CACHE_SIZE_MB", "50"))
        
        # Настройки безопасности
        self.encrypt_data = os.getenv("ENCRYPT_DATA", "false").lower() == "true"
        self.encryption_key = os.getenv("ENCRYPTION_KEY")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_to_file = os.getenv("LOG_TO_FILE", "true").lower() == "true"
        self.log_file = os.getenv("LOG_FILE", "userbot.log")
        
        # Ограничения доступа
        allowed_users_str = os.getenv("ALLOWED_USERS", "")
        if allowed_users_str:
            self.allowed_users = [int(uid.strip()) for uid in allowed_users_str.split(",") if uid.strip()]
        else:
            self.allowed_users = []
        
        self.admin_only = os.getenv("ADMIN_ONLY", "false").lower() == "true"
        
        # Настройки уведомлений
        self.notify_start = os.getenv("NOTIFY_START", "true").lower() == "true"
        self.notify_stop = os.getenv("NOTIFY_STOP", "true").lower() == "true"
        self.notify_errors = os.getenv("NOTIFY_ERRORS", "true").lower() == "true"
        self.notify_stats = os.getenv("NOTIFY_STATS", "true").lower() == "true"
        
        notification_chat_id = os.getenv("NOTIFICATION_CHAT_ID")
        self.notification_chat_id = int(notification_chat_id) if notification_chat_id else None
    
    def validate(self) -> bool:
        """Проверка корректности конфигурации"""
        # Проверяем обязательные параметры
        if not self.api_id or not self.api_hash:
            print("❌ Ошибка: API_ID и API_HASH обязательны")
            return False
        
        # Проверяем настройки пересылки
        if self.forwarding_enabled:
            if not self.source_group_id or not self.target_group_id:
                print("❌ Ошибка: SOURCE_GROUP_ID и TARGET_GROUP_ID обязательны для пересылки")
                return False
        
        # Проверяем настройки парсинга
        if self.parsing_enabled:
            if not self.parsing_group_id:
                print("❌ Ошибка: PARSING_GROUP_ID обязателен для парсинга")
                return False
        
        # Проверяем настройки безопасности
        if self.encrypt_data and not self.encryption_key:
            print("❌ Ошибка: ENCRYPTION_KEY обязателен при включенном шифровании")
            return False
        
        return True
    
    def get_config_info(self) -> str:
        """Получить информацию о текущей конфигурации"""
        info = f"""
📋 **Конфигурация Telegram Userbot**

🔧 **Основные настройки:**
- API_ID: {'✅' if self.api_id else '❌'}
- API_HASH: {'✅' if self.api_hash else '❌'}
- Session: {self.session_name}
- Prefix: {self.cmd_prefix}

📤 **Пересылка:**
- Включена: {'✅' if self.forwarding_enabled else '❌'}
- Источник: {self.source_group_id or 'Не указан'}
- Цель: {self.target_group_id or 'Не указан'}
- Фильтры: Текст={self.forward_text}, Медиа={self.forward_media}, Стикеры={self.forward_stickers}

📊 **Парсинг:**
- Включен: {'✅' if self.parsing_enabled else '❌'}
- Группа: {self.parsing_group_id or 'Не указана'}
- Фильтры: Текст={self.parse_text}, Медиа={self.parse_media}, Кнопки={self.parse_buttons}
- Дополнительно: Метаданные={self.parse_metadata}, Реакции={self.parse_reactions}, Хештеги={self.parse_hashtags}

🤖 **Парсинг ботов:**
- Включен: {'✅' if self.parse_bots else '❌'}
- Сообщения ботов: {'✅' if self.parse_bot_messages else '❌'}
- Команды ботов: {'✅' if self.parse_bot_commands else '❌'}
- Кнопки ботов: {'✅' if self.parse_bot_buttons else '❌'}
- Анализ паттернов: {'✅' if self.analyze_bot_patterns else '❌'}
- Фильтрация: {'✅' if self.bot_filter_enabled else '❌'}
- Разрешенных ботов: {len(self.allowed_bot_ids)}
- Заблокированных ботов: {len(self.blocked_bot_ids)}

💾 **Сохранение данных:**
- В файл: {'✅' if self.save_to_file else '❌'}
- В БД: {'✅' if self.save_to_database else '❌'}
- В CSV: {'✅' if self.save_to_csv else '❌'}
- Папка: {self.data_directory}

⚡ **Производительность:**
- Макс сообщений/час: {self.max_messages_per_hour}
- Размер файла: {self.max_file_size_mb}MB
- Кэширование: {'✅' if self.cache_enabled else '❌'}

🔒 **Безопасность:**
- Шифрование: {'✅' if self.encrypt_data else '❌'}
- Логирование: {self.log_level}
- Логи в файл: {'✅' if self.log_to_file else '❌'}
- Ограничения: {'Только админы' if self.admin_only else 'Все пользователи'}

📢 **Уведомления:**
- При запуске: {'✅' if self.notify_start else '❌'}
- При остановке: {'✅' if self.notify_stop else '❌'}
- Об ошибках: {'✅' if self.notify_errors else '❌'}
- Статистика: {'✅' if self.notify_stats else '❌'}
"""
        return info

# Создаем глобальный экземпляр конфигурации
config = Config()

# Функция для асинхронной инициализации конфигурации
async def init_config() -> 'Config':
    """Инициализация конфигурации"""
    config = Config()
    await config.load_from_env()
    
    if not config.validate():
        raise ValueError("Неверная конфигурация")
    return config 