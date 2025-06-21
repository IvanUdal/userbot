import asyncio
from telethon import TelegramClient
from telethon.events import NewMessage
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Импорт конфигурации
from config import API_ID, API_HASH, SESSION_NAME, CMD_PREFIX

# Создание клиента
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(NewMessage(pattern=f'\\{CMD_PREFIX}ping'))
async def ping_handler(event):
    """Команда .ping для проверки работы бота"""
    await event.edit('🏓 Pong!')

@client.on(NewMessage(pattern=f'\\{CMD_PREFIX}info'))
async def info_handler(event):
    """Команда .info для получения информации о сообщении"""
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    info_text = f"""
**Информация о сообщении:**
📊 **Чат:** {chat.title if hasattr(chat, 'title') else 'Личные сообщения'}
👤 **Отправитель:** {sender.first_name if hasattr(sender, 'first_name') else 'Неизвестно'}
🆔 **ID чата:** `{event.chat_id}`
🆔 **ID сообщения:** `{event.id}`
    """
    
    await event.edit(info_text)

async def main():
    """Основная функция запуска бота"""
    print("🚀 Запуск userbot...")
    
    # Подключение к Telegram
    await client.start()
    
    # Получение информации о себе
    me = await client.get_me()
    print(f"✅ Userbot запущен как: {me.first_name} (@{me.username})")
    
    # Запуск в режиме ожидания
    print("🔄 Userbot работает. Нажмите Ctrl+C для остановки.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Userbot остановлен пользователем.")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
