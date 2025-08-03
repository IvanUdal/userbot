"""
Основной файл для масштабируемого Telegram Userbot с архитектурой пайплайнов
"""

import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError, ChatAdminRequiredError

# Импорт модулей
from config import Config
from modules.pipeline_manager import PipelineManager
from modules.pipeline_commands import PipelineCommands
from safety_manager import SafetyManager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/userbot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TelegramUserbot:
    """Основной класс Telegram Userbot с архитектурой пайплайнов"""
    
    def __init__(self):
        # Загрузка конфигурации
        load_dotenv()
        self.config = Config()
        
        # Инициализация переменных
        self.client = None
        self.pipeline_manager = None
        self.pipeline_commands = None
        
        # Статистика
        self.stats = {
            'start_time': None,
            'messages_processed': 0,
            'pipelines_active': 0,
            'errors': 0
        }
    
    async def start(self):
        """Запуск бота"""
        try:
            logger.info("🚀 Запуск Telegram Userbot с архитектурой пайплайнов...")
            
            # Загрузка конфигурации
            await self.config.load_from_env()
            
            # Создание клиента с кастомными параметрами для обхода ограничений
            # Проверяем наличие строки сессии для автоматического входа
            session_string = None
            if os.path.exists("session_string.txt"):
                try:
                    with open("session_string.txt", "r") as f:
                        session_string = f.read().strip()
                    logger.info("🔐 Найдена строка сессии для автоматического входа")
                except Exception as e:
                    logger.warning(f"⚠️ Не удалось прочитать строку сессии: {e}")
            
            if session_string:
                # Используем строку сессии для автоматического входа
                from telethon.sessions import StringSession
                logger.info(f"🔐 Используем строку сессии длиной {len(session_string)} символов")
                self.client = TelegramClient(
                    StringSession(session_string),
                    self.config.api_id,
                    self.config.api_hash,
                    system_version="4.16.30-vxCUSTOM",
                    device_model="Samsung Galaxy S23",
                    app_version="9.4.2"
                )
            else:
                # Обычный клиент с файловой сессией
                self.client = TelegramClient(
                    self.config.session_name,
                    self.config.api_id,
                    self.config.api_hash,
                    system_version="4.16.30-vxCUSTOM",
                    device_model="Samsung Galaxy S23",
                    app_version="9.4.2"
                )
            
            # Инициализация менеджера пайплайнов
            self.pipeline_manager = PipelineManager(self.client)
            
            # Инициализация команд
            self.pipeline_commands = PipelineCommands(self.client, self.pipeline_manager)
            
            # Инициализация менеджера безопасности
            self.safety_manager = SafetyManager()
            
            # Подключение к Telegram
            try:
                # Используем connect() вместо start() для избежания интерактивного ввода
                await self.client.connect()
                
                if not await self.client.is_user_authorized():
                    if session_string:
                        logger.error("❌ Пользователь не авторизован даже со строкой сессии")
                        raise Exception("Не удалось авторизоваться со строкой сессии")
                    else:
                        logger.error("❌ Пользователь не авторизован. Нужна интерактивная аутентификация")
                        raise Exception("Требуется интерактивная аутентификация")
                
                logger.info("✅ Подключение к Telegram установлено")
            except Exception as e:
                logger.error(f"❌ Ошибка при подключении: {e}")
                raise
            
            # Настройка команд
            await self.pipeline_commands.setup_commands()
            logger.info("✅ Команды пайплайнов настроены")
            
            # Настройка базовых команд
            await self.setup_basic_commands()
            logger.info("✅ Базовые команды настроены")
            
            # Запуск всех активных пайплайнов
            await self.start_active_pipelines()
            
            # Запуск мониторинга
            asyncio.create_task(self.monitoring_task())
            
            self.stats['start_time'] = asyncio.get_event_loop().time()
            logger.info("🎉 Telegram Userbot успешно запущен!")
            
            # Уведомление о запуске
            if self.config.notify_start:
                await self.send_startup_notification()
            
            # Ожидание завершения
            await self.client.run_until_disconnected()
        
        except Exception as e:
            logger.error(f"❌ Критическая ошибка при запуске: {e}")
            raise
    
    async def setup_basic_commands(self):
        """Настройка базовых команд"""
        
        @self.client.on(events.NewMessage(pattern=r'^\.ping$'))
        async def ping_command(event):
            await self.ping_command_handler(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.info$'))
        async def info_command(event):
            await self.info_command_handler(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.help$'))
        async def help_command(event):
            await self.help_command_handler(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.status$'))
        async def status_command(event):
            await self.status_command_handler(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.safety$'))
        async def safety_command(event):
            await self.safety_command_handler(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.config$'))
        async def config_command(event):
            await self.config_command_handler(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.test_access$'))
        async def test_access_command(event):
            await self.test_access_command_handler(event)
        
        @self.client.on(events.NewMessage(pattern=r'^\.test_media$'))
        async def test_media_command(event):
            await self.test_media_command_handler(event)
        
        # Обработчик пересылки сообщений
        if self.config.forwarding_enabled and self.config.source_group_id and self.config.target_group_id:
            logger.info(f"🔄 Регистрация обработчика пересылки: {self.config.source_group_id} -> {self.config.target_group_id}")
            @self.client.on(events.NewMessage(chats=self.config.source_group_id))
            async def forward_handler(event):
                await self.forward_message_handler(event)
        else:
            logger.warning(f"⚠️ Обработчик пересылки не зарегистрирован:")
            logger.warning(f"   - forwarding_enabled: {self.config.forwarding_enabled}")
            logger.warning(f"   - source_group_id: {self.config.source_group_id}")
            logger.warning(f"   - target_group_id: {self.config.target_group_id}")
    
    async def start_active_pipelines(self):
        """Запуск всех активных пайплайнов"""
        try:
            active_pipelines = [
                name for name, pipeline in self.pipeline_manager.pipelines.items()
                if pipeline.enabled
            ]
            
            if active_pipelines:
                logger.info(f"🚀 Запуск {len(active_pipelines)} активных пайплайнов...")
                
                for pipeline_name in active_pipelines:
                    success = await self.pipeline_manager.start_pipeline(pipeline_name)
                    if success:
                        self.stats['pipelines_active'] += 1
                        logger.info(f"✅ Пайплайн '{pipeline_name}' запущен")
                    else:
                        logger.error(f"❌ Ошибка запуска пайплайна '{pipeline_name}'")
                
                logger.info(f"📊 Запущено пайплайнов: {self.stats['pipelines_active']}")
            else:
                logger.info("ℹ️ Нет активных пайплайнов для запуска")
        
        except Exception as e:
            logger.error(f"❌ Ошибка запуска пайплайнов: {e}")
    
    async def monitoring_task(self):
        """Задача мониторинга"""
        while True:
            try:
                # Обновление статистики
                await self.update_statistics()
                
                # Проверка состояния пайплайнов
                await self.check_pipeline_health()
                
                # Отправка периодических отчетов
                await self.send_periodic_reports()
                
                await asyncio.sleep(300)  # Проверка каждые 5 минут
            
            except Exception as e:
                logger.error(f"❌ Ошибка в задаче мониторинга: {e}")
                await asyncio.sleep(60)
    
    async def update_statistics(self):
        """Обновление статистики"""
        try:
            stats = await self.pipeline_manager.get_statistics()
            
            self.stats['messages_processed'] = stats['report']['summary']['total_processed']
            self.stats['errors'] = stats['report']['summary']['total_errors']
            self.stats['pipelines_active'] = stats['active_pipelines']
            
        except Exception as e:
            logger.error(f"❌ Ошибка обновления статистики: {e}")
    
    async def check_pipeline_health(self):
        """Проверка состояния пайплайнов"""
        try:
            for pipeline_name in self.pipeline_manager.pipelines:
                status = await self.pipeline_manager.get_pipeline_status(pipeline_name)
                if status and status['stats']:
                    last_activity = status['stats'].get('last_activity')
                    if last_activity:
                        # Проверка активности за последние 10 минут
                        from datetime import datetime, timedelta
                        last_activity_dt = datetime.fromisoformat(last_activity)
                        if datetime.now() - last_activity_dt > timedelta(minutes=10):
                            logger.warning(f"⚠️ Пайплайн '{pipeline_name}' неактивен более 10 минут")
        
        except Exception as e:
            logger.error(f"❌ Ошибка проверки состояния пайплайнов: {e}")
    
    async def send_periodic_reports(self):
        """Отправка периодических отчетов"""
        try:
            if self.config.notify_stats:
                stats = await self.pipeline_manager.get_statistics()
                
                report = f"📊 **Периодический отчет**\n\n"
                report += f"📈 Обработано сообщений: {stats['report']['summary']['total_processed']}\n"
                report += f"❌ Ошибок: {stats['report']['summary']['total_errors']}\n"
                report += f"🔄 Активных пайплайнов: {stats['active_pipelines']}\n"
                report += f"📥 Источников: {stats['sources_count']}\n"
                report += f"📤 Назначений: {stats['destinations_count']}"
                
                # Отправка отчета в указанный чат
                if hasattr(self.config, 'admin_chat_id') and self.config.admin_chat_id:
                    await self.client.send_message(self.config.admin_chat_id, report)
        
        except Exception as e:
            logger.error(f"❌ Ошибка отправки периодического отчета: {e}")
    
    async def send_startup_notification(self):
        """Отправка уведомления о запуске"""
        try:
            notification = f"🚀 **Telegram Userbot запущен**\n\n"
            notification += f"📊 Статистика:\n"
            notification += f"• Пайплайнов: {len(self.pipeline_manager.pipelines)}\n"
            notification += f"• Источников: {len(self.pipeline_manager.sources)}\n"
            notification += f"• Назначений: {len(self.pipeline_manager.destinations)}\n"
            notification += f"• Активных пайплайнов: {self.stats['pipelines_active']}"
            
            if hasattr(self.config, 'admin_chat_id') and self.config.admin_chat_id:
                await self.client.send_message(self.config.admin_chat_id, notification)
        
        except Exception as e:
            logger.error(f"❌ Ошибка отправки уведомления о запуске: {e}")
    
    # Обработчики базовых команд
    
    async def ping_command_handler(self, event):
        """Обработчик команды .ping"""
        try:
            response = f"🏓 **Pong!**\n\n"
            response += f"⏱️ Время ответа: {asyncio.get_event_loop().time() - self.stats['start_time']:.2f}с\n"
            response += f"📊 Сообщений обработано: {self.stats['messages_processed']}\n"
            response += f"🔄 Активных пайплайнов: {self.stats['pipelines_active']}"
            
            await event.respond(response)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка: {e}")
    
    async def info_command_handler(self, event):
        """Обработчик команды .info"""
        try:
            config_info = self.config.get_config_info()
            await event.respond(config_info)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка получения информации: {e}")
    
    async def help_command_handler(self, event):
        """Обработчик команды .help"""
        try:
            help_text = """
🤖 **Telegram Userbot - Справка**

📋 **Базовые команды:**
• `.ping` - Проверка работоспособности
• `.info` - Информация о конфигурации
• `.status` - Статус системы
• `.safety` - Отчет о безопасности
• `.help` - Эта справка

🔄 **Команды пайплайнов:**
• `.pipelines_start_all` - Запуск всех пайплайнов
• `.pipelines_stop_all` - Остановка всех пайплайнов
• `.pipeline_status <name>` - Статус пайплайна
• `.pipelines_list` - Список пайплайнов

📥 **Управление источниками:**
• `.source_add <name> <id>` - Добавить источник
• `.source_remove <name>` - Удалить источник
• `.sources_list` - Список источников

📤 **Управление назначениями:**
• `.destination_add <name> <type> <config>` - Добавить назначение
• `.destination_remove <name>` - Удалить назначение
• `.destinations_list` - Список назначений

📊 **Статистика и экспорт:**
• `.stats_export all_pipelines` - Экспорт статистики

🔧 **Примеры использования:**
• `.source_add news_channel -1001234567890`
• `.destination_add telegram_dest telegram {"chat_id": -100111222333}`
• `.pipeline_create news_analytics news_channel telegram_dest,export_file`
"""
            await event.respond(help_text)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка отображения справки: {e}")
    
    async def status_command_handler(self, event):
        """Обработчик команды .status"""
        try:
            stats = await self.pipeline_manager.get_statistics()
            
            status_text = f"📊 **Статус системы**\n\n"
            status_text += f"🔄 **Пайплайны:**\n"
            status_text += f"• Всего: {stats['pipelines_count']}\n"
            status_text += f"• Активных: {stats['active_pipelines']}\n\n"
            
            status_text += f"📥 **Источники:**\n"
            status_text += f"• Всего: {stats['sources_count']}\n"
            status_text += f"• Активных: {stats['active_sources']}\n\n"
            
            status_text += f"📤 **Назначения:**\n"
            status_text += f"• Всего: {stats['destinations_count']}\n"
            status_text += f"• Активных: {stats['active_destinations']}\n\n"
            
            if stats['report']:
                report = stats['report']
                status_text += f"📈 **Статистика обработки:**\n"
                status_text += f"• Обработано сообщений: {report['summary']['total_processed']}\n"
                status_text += f"• Ошибок: {report['summary']['total_errors']}\n"
                status_text += f"• Активных пайплайнов: {report['summary']['active_pipelines']}"
            
            await event.respond(status_text)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка получения статуса: {e}")
    
    async def safety_command_handler(self, event):
        """Обработчик команды .safety"""
        try:
            safety_report = self.safety_manager.get_safety_report()
            await event.respond(safety_report)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка получения отчета безопасности: {e}")
    
    async def config_command_handler(self, event):
        """Обработчик команды .config"""
        try:
            config_info = f"📋 **Настройки пересылки:**\n\n"
            config_info += f"🔄 Пересылка включена: {'Да' if self.config.forwarding_enabled else 'Нет'}\n"
            config_info += f"📥 Источник: {self.config.source_group_id}\n"
            config_info += f"📤 Назначение: {self.config.target_group_id}\n"
            config_info += f"📝 Текст: {'Да' if self.config.forward_text else 'Нет'}\n"
            config_info += f"🖼️ Медиа: {'Да' if self.config.forward_media else 'Нет'}\n"
            config_info += f"😀 Стикеры: {'Да' if self.config.forward_stickers else 'Нет'}\n"
            config_info += f"🎤 Голосовые: {'Да' if self.config.forward_voice else 'Нет'}\n"
            config_info += f"📄 Документы: {'Да' if self.config.forward_documents else 'Нет'}\n"
            
            await event.respond(config_info)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка получения конфигурации: {e}")
    
    async def test_access_command_handler(self, event):
        """Обработчик команды .test_access"""
        try:
            access_info = f"🔍 **Проверка доступа к группам:**\n\n"
            
            # Проверяем доступ к исходной группе
            try:
                source_chat = await self.client.get_entity(self.config.source_group_id)
                access_info += f"✅ Источник ({self.config.source_group_id}): Доступ есть\n"
                access_info += f"   Название: {getattr(source_chat, 'title', 'Неизвестно')}\n"
            except Exception as e:
                access_info += f"❌ Источник ({self.config.source_group_id}): Нет доступа - {e}\n"
            
            # Проверяем доступ к целевой группе
            try:
                target_chat = await self.client.get_entity(self.config.target_group_id)
                access_info += f"✅ Назначение ({self.config.target_group_id}): Доступ есть\n"
                access_info += f"   Название: {getattr(target_chat, 'title', 'Неизвестно')}\n"
            except Exception as e:
                access_info += f"❌ Назначение ({self.config.target_group_id}): Нет доступа - {e}\n"
            
            await event.respond(access_info)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка проверки доступа: {e}")
    
    async def test_media_command_handler(self, event):
        """Обработчик команды .test_media"""
        try:
            await event.respond("🔄 Тестирование пересылки медиа...")
            
            # Проверяем настройки медиа
            media_info = f"📋 **Настройки медиа:**\n\n"
            media_info += f"🖼️ Медиа включено: {'Да' if self.config.forward_media else 'Нет'}\n"
            media_info += f"📝 Текст включен: {'Да' if self.config.forward_text else 'Нет'}\n"
            media_info += f"😀 Стикеры включены: {'Да' if self.config.forward_stickers else 'Нет'}\n"
            media_info += f"🎤 Голосовые включены: {'Да' if self.config.forward_voice else 'Нет'}\n"
            media_info += f"📄 Документы включены: {'Да' if self.config.forward_documents else 'Нет'}\n\n"
            media_info += f"📥 Источник: {self.config.source_group_id}\n"
            media_info += f"📤 Назначение: {self.config.target_group_id}\n\n"
            media_info += f"✅ Отправьте картинку в группу для тестирования!"
            
            await event.respond(media_info)
        
        except Exception as e:
            await event.respond(f"❌ Ошибка тестирования медиа: {e}")
    
    async def forward_message_handler(self, event):
        """Обработчик пересылки сообщений"""
        try:
            logger.info(f"📥 Получено сообщение в чате {event.chat_id}")
            logger.info(f"📝 Тип сообщения: {'текст' if event.text else 'медиа' if event.media else 'другое'}")
            logger.info(f"🖼️ Детали медиа: media={bool(event.media)}, photo={bool(event.photo)}, video={bool(event.video)}, document={bool(event.document)}")
            
            # Проверяем, нужно ли пересылать это сообщение
            if not self._should_forward_message(event):
                logger.info(f"❌ Сообщение не подходит для пересылки")
                return
            
            logger.info(f"✅ Сообщение подходит для пересылки, начинаем пересылку...")
            
            # Безопасная пересылка через SafetyManager
            success = await self.safety_manager.safe_forward(
                self.client,
                self.config.source_group_id,
                self.config.target_group_id,
                event.message.id
            )
            
            if success:
                logger.info(f"✅ Сообщение {event.message.id} переслано")
            else:
                logger.warning(f"⚠️ Не удалось переслать сообщение {event.message.id}")
        
        except Exception as e:
            logger.error(f"❌ Ошибка пересылки: {e}")
            logger.error(f"📊 Детали: source={self.config.source_group_id}, target={self.config.target_group_id}")
    
    def _should_forward_message(self, event) -> bool:
        """Проверка, нужно ли пересылать сообщение"""
        logger.info(f"🔍 Проверка сообщения: text={bool(event.text)}, media={bool(event.media)}, photo={bool(event.photo)}, video={bool(event.video)}, document={bool(event.document)}")
        
        # Проверяем, не от бота ли сообщение
        if hasattr(event.sender, 'bot') and event.sender.bot:
            logger.info(f"❌ Сообщение от бота")
            return False
        
        # Проверяем текстовые сообщения
        if event.text and not self.config.forward_text:
            logger.info(f"❌ Текст отключен в настройках")
            return False
        
        # Проверяем медиа-контент (фото, видео)
        if event.media and not self.config.forward_media:
            logger.info(f"❌ Медиа отключено в настройках")
            return False
        
        # Проверяем стикеры
        if event.sticker and not self.config.forward_stickers:
            logger.info(f"❌ Стикеры отключены в настройках")
            return False
        
        # Проверяем голосовые
        if event.voice and not self.config.forward_voice:
            logger.info(f"❌ Голосовые отключены в настройках")
            return False
        
        # Проверяем документы
        if event.document and not self.config.forward_documents:
            logger.info(f"❌ Документы отключены в настройках")
            return False
        
        # Если есть медиа и оно разрешено
        if event.media and self.config.forward_media:
            logger.info(f"✅ Медиа-контент разрешен")
            return True
        
        # Если есть текст и он разрешен
        if event.text and self.config.forward_text:
            logger.info(f"✅ Текстовое сообщение разрешено")
            return True
        
        # Если есть стикер и он разрешен
        if event.sticker and self.config.forward_stickers:
            logger.info(f"✅ Стикер разрешен")
            return True
        
        # Если есть голосовое и оно разрешено
        if event.voice and self.config.forward_voice:
            logger.info(f"✅ Голосовое сообщение разрешено")
            return True
        
        # Если есть документ и он разрешен
        if event.document and self.config.forward_documents:
            logger.info(f"✅ Документ разрешен")
            return True
        
        logger.info(f"❌ Сообщение не подходит для пересылки")
        return False
    
    async def stop(self):
        """Остановка бота"""
        try:
            logger.info("🛑 Остановка Telegram Userbot...")
            
            # Остановка всех пайплайнов
            for pipeline_name in self.pipeline_manager.pipelines:
                await self.pipeline_manager.stop_pipeline(pipeline_name)
            
            # Отключение от Telegram
            await self.client.disconnect()
            
            logger.info("✅ Telegram Userbot остановлен")
        
        except Exception as e:
            logger.error(f"❌ Ошибка при остановке: {e}")

async def main():
    """Основная функция"""
    # Создание директорий
    Path("logs").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("data/exports").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)
    
    # Создание и запуск бота
    bot = TelegramUserbot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    asyncio.run(main()) 