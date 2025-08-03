import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def auth():
    print("🔐 Начинаем аутентификацию...")
    
    # Ваши данные
    api_id = 25874482
    api_hash = "5463e25bfff2c0f8b1a90041f162bb0f"
    
    # Создаем клиент
    client = TelegramClient('userbot', api_id, api_hash)
    
    try:
        print("📱 Подключение к Telegram...")
        await client.start()
        
        if await client.is_user_authorized():
            print("✅ Пользователь авторизован!")
            
            # Получаем информацию о пользователе
            me = await client.get_me()
            print(f"�� Авторизован как: {me.first_name} (@{me.username})")
            
            # Создаем строку сессии
            session_string = StringSession.save(client.session)
            print(f"🔑 Строка сессии получена (длина: {len(session_string)} символов)")
            
            # Сохраняем в файл
            with open('session_string.txt', 'w') as f:
                f.write(session_string)
            print("💾 Строка сессии сохранена в session_string.txt")
            
            return True
        else:
            print("❌ Пользователь не авторизован")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(auth())
