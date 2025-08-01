# Пример реализации парсера сообщений для закрытой группы
# ВАЖНО: Для парсинга достаточно быть участником группы (НЕ обязательно администратором)
import asyncio
import json
import re
from datetime import datetime
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from pathlib import Path

from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage
from telethon.tl.types import ReplyInlineMarkup, KeyboardButton, KeyboardButtonUrl, KeyboardButtonCallback
from telethon.errors import ChatAdminRequiredError, FloodWaitError

# ===========================================
# КЛАССЫ ДЛЯ ПАРСИНГА
# ===========================================

@dataclass
class ParsedButton:
    """Структура для хранения информации о кнопке"""
    text: str
    button_type: str  # 'url', 'callback', 'web_app', 'switch_inline', etc.
    data: Optional[str] = None  # callback_data или URL
    url: Optional[str] = None
    web_app_url: Optional[str] = None

@dataclass
class BotCommand:
    """Структура для хранения информации о команде бота"""
    command: str
    description: Optional[str] = None
    usage_count: int = 0
    last_used: Optional[datetime] = None

@dataclass
class ParsedMessage:
    """Структура для хранения распарсенного сообщения"""
    message_id: int
    chat_id: int
    sender_id: int
    sender_name: str
    sender_username: str
    text: str
    media_type: Optional[str]
    media_url: Optional[str]
    timestamp: datetime
    reply_to: Optional[int]
    forwards: Optional[Dict]
    reactions: List[Dict]
    hashtags: List[str]
    urls: List[str]
    buttons: List[ParsedButton]  # Добавляем кнопки
    is_bot: bool = False
    bot_info: Optional[Dict] = None  # Дополнительная информация о боте

@dataclass
class ParsingStats:
    """Статистика парсинга"""
    total_messages: int = 0
    text_messages: int = 0
    media_messages: int = 0
    bot_messages: int = 0
    messages_with_buttons: int = 0  # Добавляем статистику кнопок
    bot_commands: int = 0  # Добавляем статистику команд ботов
    errors: int = 0
    start_time: Optional[datetime] = None

# ===========================================
# КЛАСС ПАРСЕРА СООБЩЕНИЙ
# ===========================================

class MessageParser:
    """Класс для парсинга сообщений из Telegram групп
    ВАЖНО: Для парсинга достаточно быть участником группы (НЕ обязательно администратором)
    """
    
    def __init__(self, client: TelegramClient, save_path: str = "data/parsed_messages.json"):
        self.client = client
        self.save_path = Path(save_path)
        self.save_path.parent.mkdir(exist_ok=True)
        self.stats = ParsingStats()
        self.parsing_active = False
        
        # Статистика ботов
        self.bot_stats = {
            'total_bots': 0,
            'bot_commands': {},
            'bot_patterns': {},
            'bot_interactions': {}
        }
        
    async def check_group_access(self, chat_id: int) -> bool:
        """Проверка доступа к группе (достаточно быть участником)"""
        try:
            chat = await self.client.get_entity(chat_id)
            print(f"✅ Доступ к группе: {chat.title}")
            return True
        except Exception as e:
            print(f"❌ Нет доступа к группе: {e}")
            print("💡 Убедитесь, что вы участник группы")
            return False
        
    async def start_parsing(self, chat_id: int) -> None:
        """Начать парсинг сообщений из группы"""
        # Проверяем доступ к группе
        if not await self.check_group_access(chat_id):
            print("❌ Невозможно начать парсинг - нет доступа к группе")
            return
            
        self.parsing_active = True
        self.stats.start_time = datetime.now()
        
        @self.client.on(NewMessage(chats=chat_id))
        async def parsing_handler(event):
            if not self.parsing_active:
                return
                
            try:
                parsed_message = await self.parse_message(event)
                
                # Проверяем, нужно ли парсить это сообщение
                if await self.should_parse_message(parsed_message):
                    await self.save_message(parsed_message)
                    await self.update_bot_stats(parsed_message)
                    self.stats.total_messages += 1
                    
                    # Обновляем статистику кнопок
                    if parsed_message.buttons:
                        self.stats.messages_with_buttons += 1
                    
                    # Обновляем статистику ботов
                    if parsed_message.is_bot:
                        self.stats.bot_messages += 1
                        if await self.is_bot_command(parsed_message.text):
                            self.stats.bot_commands += 1
                
            except FloodWaitError as e:
                print(f"⚠️ FloodWait: {e}")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"❌ Ошибка парсинга: {e}")
                self.stats.errors += 1
    
    async def should_parse_message(self, message: ParsedMessage) -> bool:
        """Проверка, нужно ли парсить сообщение"""
        # Если это бот, проверяем настройки парсинга ботов
        if message.is_bot:
            # Здесь можно добавить фильтры по конкретным ботам
            return True
        
        return True
    
    async def is_bot_command(self, text: str) -> bool:
        """Проверка, является ли сообщение командой бота"""
        if not text:
            return False
        
        # Команды обычно начинаются с /
        if text.startswith('/'):
            return True
        
        # Проверяем паттерны команд ботов
        command_patterns = [
            r'^/[a-zA-Z_]+',  # /command
            r'^![a-zA-Z_]+',  # !command
            r'^\.\w+',        # .command
        ]
        
        for pattern in command_patterns:
            if re.match(pattern, text.strip()):
                return True
        
        return False
    
    async def update_bot_stats(self, message: ParsedMessage) -> None:
        """Обновление статистики ботов"""
        if not message.is_bot:
            return
        
        bot_id = message.sender_id
        
        # Обновляем общую статистику ботов
        if bot_id not in self.bot_stats['bot_interactions']:
            self.bot_stats['total_bots'] += 1
            self.bot_stats['bot_interactions'][bot_id] = {
                'name': message.sender_name,
                'username': message.sender_username,
                'message_count': 0,
                'commands': [],
                'buttons_used': 0,
                'media_sent': 0
            }
        
        # Обновляем статистику конкретного бота
        bot_stats = self.bot_stats['bot_interactions'][bot_id]
        bot_stats['message_count'] += 1
        
        # Анализируем команды
        if await self.is_bot_command(message.text):
            command = self.extract_command(message.text)
            if command:
                bot_stats['commands'].append(command)
                if command not in self.bot_stats['bot_commands']:
                    self.bot_stats['bot_commands'][command] = 0
                self.bot_stats['bot_commands'][command] += 1
        
        # Анализируем кнопки
        if message.buttons:
            bot_stats['buttons_used'] += len(message.buttons)
        
        # Анализируем медиа
        if message.media_type:
            bot_stats['media_sent'] += 1
    
    def extract_command(self, text: str) -> Optional[str]:
        """Извлечение команды из текста"""
        if not text:
            return None
        
        # Убираем лишние пробелы
        text = text.strip()
        
        # Ищем команду
        command_patterns = [
            r'^/([a-zA-Z_]+)',  # /command
            r'^!([a-zA-Z_]+)',  # !command
            r'^\.(\w+)',        # .command
        ]
        
        for pattern in command_patterns:
            match = re.match(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    async def stop_parsing(self) -> None:
        """Остановить парсинг"""
        self.parsing_active = False
        print("🛑 Парсинг остановлен")
    
    async def parse_buttons(self, reply_markup) -> List[ParsedButton]:
        """Парсинг кнопок из сообщения"""
        buttons = []
        
        if not reply_markup:
            return buttons
            
        try:
            # Обрабатываем inline keyboard
            if hasattr(reply_markup, 'rows'):
                for row in reply_markup.rows:
                    for button in row.buttons:
                        button_info = await self.parse_single_button(button)
                        if button_info:
                            buttons.append(button_info)
            
            # Обрабатываем обычную клавиатуру
            elif hasattr(reply_markup, 'resize') or hasattr(reply_markup, 'single_use'):
                for row in reply_markup.rows:
                    for button in row.buttons:
                        button_info = await self.parse_single_button(button)
                        if button_info:
                            buttons.append(button_info)
                            
        except Exception as e:
            print(f"⚠️ Ошибка парсинга кнопок: {e}")
            
        return buttons
    
    async def parse_single_button(self, button) -> Optional[ParsedButton]:
        """Парсинг одной кнопки"""
        try:
            text = button.text
            
            # URL кнопка
            if hasattr(button, 'url'):
                return ParsedButton(
                    text=text,
                    button_type='url',
                    url=button.url
                )
            
            # Callback кнопка
            elif hasattr(button, 'data'):
                return ParsedButton(
                    text=text,
                    button_type='callback',
                    data=button.data.decode('utf-8') if isinstance(button.data, bytes) else str(button.data)
                )
            
            # Web App кнопка
            elif hasattr(button, 'web_app'):
                return ParsedButton(
                    text=text,
                    button_type='web_app',
                    web_app_url=button.web_app.url
                )
            
            # Switch Inline кнопка
            elif hasattr(button, 'query'):
                return ParsedButton(
                    text=text,
                    button_type='switch_inline',
                    data=button.query
                )
            
            # Обычная кнопка
            else:
                return ParsedButton(
                    text=text,
                    button_type='text'
                )
                
        except Exception as e:
            print(f"⚠️ Ошибка парсинга кнопки: {e}")
            return None
    
    async def parse_message(self, event) -> ParsedMessage:
        """Парсинг одного сообщения"""
        # Получаем информацию об отправителе
        sender = await event.get_sender()
        sender_name = sender.first_name if hasattr(sender, 'first_name') else 'Неизвестно'
        sender_username = f"@{sender.username}" if hasattr(sender, 'username') and sender.username else ""
        is_bot = hasattr(sender, 'bot') and sender.bot
        
        # Дополнительная информация о боте
        bot_info = None
        if is_bot:
            bot_info = {
                'bot_id': sender.id,
                'bot_name': sender_name,
                'bot_username': sender_username,
                'is_verified': hasattr(sender, 'verified') and sender.verified,
                'is_scam': hasattr(sender, 'scam') and sender.scam,
                'is_fake': hasattr(sender, 'fake') and sender.fake
            }
        
        # Определяем тип медиа
        media_type = None
        media_url = None
        if event.media:
            if isinstance(event.media, MessageMediaPhoto):
                media_type = "photo"
            elif isinstance(event.media, MessageMediaDocument):
                media_type = "document"
            elif isinstance(event.media, MessageMediaWebPage):
                media_type = "webpage"
        
        # Извлекаем хештеги и ссылки
        text = event.text or ""
        hashtags = re.findall(r'#\w+', text)
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        
        # Получаем реакции (если доступно)
        reactions = []
        try:
            if hasattr(event, 'reactions') and event.reactions:
                for reaction in event.reactions.results:
                    reactions.append({
                        "emoji": reaction.reaction.emoticon,
                        "count": reaction.count
                    })
        except:
            pass
        
        # Информация о пересылке
        forwards = None
        if event.forward:
            try:
                original_chat = await event.get_chat()
                forwards = {
                    "original_chat_id": original_chat.id,
                    "original_chat_title": getattr(original_chat, 'title', 'Неизвестно'),
                    "original_message_id": event.forward.from_id
                }
            except:
                pass
        
        # Парсим кнопки
        buttons = []
        if hasattr(event, 'reply_markup') and event.reply_markup:
            buttons = await self.parse_buttons(event.reply_markup)
        
        return ParsedMessage(
            message_id=event.id,
            chat_id=event.chat_id,
            sender_id=sender.id,
            sender_name=sender_name,
            sender_username=sender_username,
            text=text,
            media_type=media_type,
            media_url=media_url,
            timestamp=event.date,
            reply_to=event.reply_to.reply_to_msg_id if event.reply_to else None,
            forwards=forwards,
            reactions=reactions,
            hashtags=hashtags,
            urls=urls,
            buttons=buttons,  # Добавляем кнопки
            is_bot=is_bot,
            bot_info=bot_info  # Добавляем информацию о боте
        )
    
    async def save_message(self, parsed_message: ParsedMessage) -> None:
        """Сохранение сообщения в JSON файл"""
        try:
            # Загружаем существующие данные
            existing_data = []
            if self.save_path.exists():
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            
            # Добавляем новое сообщение
            message_dict = asdict(parsed_message)
            message_dict['timestamp'] = message_dict['timestamp'].isoformat()
            
            # Конвертируем кнопки в словари
            message_dict['buttons'] = [asdict(button) for button in parsed_message.buttons]
            
            existing_data.append(message_dict)
            
            # Сохраняем обратно
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
                
            button_count = len(parsed_message.buttons)
            sender_type = "🤖 Бот" if parsed_message.is_bot else "👤 Пользователь"
            print(f"✅ Сохранено сообщение {parsed_message.message_id} от {parsed_message.sender_name} ({sender_type}) (кнопок: {button_count})")
            
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику парсинга"""
        duration = None
        if self.stats.start_time:
            duration = (datetime.now() - self.stats.start_time).total_seconds()
        
        return {
            "total_messages": self.stats.total_messages,
            "bot_messages": self.stats.bot_messages,
            "bot_commands": self.stats.bot_commands,
            "messages_with_buttons": self.stats.messages_with_buttons,
            "errors": self.stats.errors,
            "duration_seconds": duration,
            "messages_per_second": self.stats.total_messages / duration if duration else 0,
            "parsing_active": self.parsing_active,
            "bot_statistics": self.bot_stats
        }
    
    def get_bot_analysis(self) -> Dict[str, Any]:
        """Получить анализ ботов"""
        return {
            "total_bots": self.bot_stats['total_bots'],
            "bot_commands": self.bot_stats['bot_commands'],
            "bot_interactions": self.bot_stats['bot_interactions'],
            "top_commands": dict(sorted(self.bot_stats['bot_commands'].items(), key=lambda x: x[1], reverse=True)[:10]),
            "most_active_bots": sorted(
                self.bot_stats['bot_interactions'].items(),
                key=lambda x: x[1]['message_count'],
                reverse=True
            )[:5]
        }
    
    async def export_to_csv(self, output_path: str = "data/export.csv") -> None:
        """Экспорт данных в CSV формат"""
        import csv
        
        if not self.save_path.exists():
            print("❌ Нет данных для экспорта")
            return
        
        with open(self.save_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print("❌ Нет данных для экспорта")
            return
        
        # Определяем все возможные поля
        all_fields = set()
        for message in data:
            all_fields.update(message.keys())
        
        # Сортируем поля для стабильного порядка
        fieldnames = sorted(list(all_fields))
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✅ Экспорт завершен: {output_path}")

# ===========================================
# ПРИМЕР ИСПОЛЬЗОВАНИЯ
# ===========================================

async def example_usage():
    """Пример использования парсера"""
    
    # Инициализация клиента (замени на свои данные)
    client = TelegramClient(
        'parser_session',
        api_id=12345678,  # Замени на свой API_ID
        api_hash='your_api_hash_here'  # Замени на свой API_HASH
    )
    
    await client.start()
    
    # Создаем парсер
    parser = MessageParser(client)
    
    # ID группы для парсинга (замени на реальный ID)
    chat_id = -1001234567890
    
    print("🚀 Начинаем парсинг...")
    print("💡 Используй Ctrl+C для остановки")
    print("ℹ️ Для парсинга достаточно быть участником группы")
    print("🔘 Парсинг кнопок включен")
    print("🤖 Парсинг ботов включен")
    
    try:
        # Начинаем парсинг
        await parser.start_parsing(chat_id)
        
        # Ждем ввода для остановки
        await asyncio.sleep(3600)  # Парсим 1 час
        
    except KeyboardInterrupt:
        print("\n🛑 Остановка парсинга...")
        await parser.stop_parsing()
        
        # Показываем статистику
        stats = parser.get_stats()
        print(f"📊 Статистика парсинга:")
        print(f"   Всего сообщений: {stats['total_messages']}")
        print(f"   Сообщений от ботов: {stats['bot_messages']}")
        print(f"   Команд ботов: {stats['bot_commands']}")
        print(f"   Сообщений с кнопками: {stats['messages_with_buttons']}")
        print(f"   Ошибок: {stats['errors']}")
        print(f"   Время работы: {stats['duration_seconds']:.1f} сек")
        print(f"   Сообщений/сек: {stats['messages_per_second']:.2f}")
        
        # Показываем анализ ботов
        bot_analysis = parser.get_bot_analysis()
        print(f"\n🤖 Анализ ботов:")
        print(f"   Всего ботов: {bot_analysis['total_bots']}")
        print(f"   Популярные команды: {list(bot_analysis['top_commands'].keys())[:5]}")
        
        # Экспортируем данные
        await parser.export_to_csv()
        
    finally:
        await client.disconnect()

# ===========================================
# КОМАНДЫ ДЛЯ ИНТЕГРАЦИИ В ОСНОВНОЙ БОТ
# ===========================================

class ParsingCommands:
    """Команды для управления парсингом"""
    
    def __init__(self, parser: MessageParser):
        self.parser = parser
        self.target_chat_id = None
    
    async def start_parsing_command(self, event):
        """Команда .parsing_start"""
        if self.parser.parsing_active:
            await event.respond("⚠️ Парсинг уже запущен!")
            return
        
        # Получаем ID группы из конфигурации или аргумента
        chat_id = self.target_chat_id or -1001234567890  # Замени на реальный ID
        
        await self.parser.start_parsing(chat_id)
        await event.respond("✅ Парсинг запущен! (включая кнопки и ботов)")
    
    async def stop_parsing_command(self, event):
        """Команда .parsing_stop"""
        if not self.parser.parsing_active:
            await event.respond("⚠️ Парсинг не запущен!")
            return
        
        await self.parser.stop_parsing()
        await event.respond("🛑 Парсинг остановлен!")
    
    async def parsing_status_command(self, event):
        """Команда .parsing_status"""
        stats = self.parser.get_stats()
        
        status_text = f"📊 **Статус парсинга:**\n"
        status_text += f"🔄 Активен: {'Да' if stats['parsing_active'] else 'Нет'}\n"
        status_text += f"📝 Сообщений: {stats['total_messages']}\n"
        status_text += f"🤖 От ботов: {stats['bot_messages']}\n"
        status_text += f"🔘 С кнопками: {stats['messages_with_buttons']}\n"
        status_text += f"❌ Ошибок: {stats['errors']}\n"
        
        if stats['duration_seconds']:
            status_text += f"⏱️ Время: {stats['duration_seconds']:.1f} сек\n"
            status_text += f"⚡ Скорость: {stats['messages_per_second']:.2f} сообщ/сек"
        
        await event.respond(status_text)
    
    async def bot_analysis_command(self, event):
        """Команда .bot_analysis"""
        bot_analysis = self.parser.get_bot_analysis()
        
        analysis_text = f"🤖 **Анализ ботов:**\n"
        analysis_text += f"📊 Всего ботов: {bot_analysis['total_bots']}\n\n"
        
        if bot_analysis['top_commands']:
            analysis_text += f"🔝 **Популярные команды:**\n"
            for i, (command, count) in enumerate(list(bot_analysis['top_commands'].items())[:5], 1):
                analysis_text += f"{i}. /{command}: {count} раз\n"
        
        if bot_analysis['most_active_bots']:
            analysis_text += f"\n🔥 **Самые активные боты:**\n"
            for i, (bot_id, bot_info) in enumerate(bot_analysis['most_active_bots'][:3], 1):
                analysis_text += f"{i}. {bot_info['name']}: {bot_info['message_count']} сообщений\n"
        
        await event.respond(analysis_text)
    
    async def parsing_export_command(self, event):
        """Команда .parsing_export"""
        try:
            await self.parser.export_to_csv()
            await event.respond("✅ Экспорт завершен! Файл: data/export.csv")
        except Exception as e:
            await event.respond(f"❌ Ошибка экспорта: {e}")

# ===========================================
# ЗАПУСК ПРИМЕРА
# ===========================================

if __name__ == "__main__":
    print("🚀 Запуск примера парсера...")
    print("⚠️ Не забудь заменить API_ID и API_HASH!")
    print("⚠️ Не забудь заменить chat_id на реальный ID группы!")
    print("ℹ️ Для парсинга достаточно быть участником группы (НЕ обязательно администратором)")
    print("🔘 Парсинг кнопок включен")
    print("🤖 Парсинг ботов включен")
    
    # Раскомментируй для запуска:
    # asyncio.run(example_usage()) 