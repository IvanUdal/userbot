import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def auth():
    print("🔐 Интерактивная аутентификация Telegram...")
    
    # Ваши данные
    api_id = 25874482
    api_hash = "5463e25bfff2c0f8b1a90041f162bb0f"
    
    # Создаем клиент
    client = TelegramClient('userbot', api_id, api_hash)
    
    try:
        print("📱 Подключение к Telegram...")
        await client.start()
        
        if not await client.is_user_authorized():
            print("�� Введите номер телефона (с кодом страны, например: +79001234567):")
            phone = input("Телефон: ")
            
            print("📱 Отправляем код подтверждения...")
            await client.send_code_request(phone)
            
            print("📱 Введите код подтверждения из Telegram:")
            code = input("Код: ")
            
            try:
                await client.sign_in(phone, code)
                print("✅ Успешная авторизация!")
            except Exception as e:
                if "2FA" in str(e) or "password" in str(e).lower():
                    print("🔐 Введите пароль от двухфакторной аутентификации:")
                    password = input("Пароль: ")
                    await client.sign_in(password=password)
                    print("✅ Успешная авторизация с 2FA!")
                else:
                    print(f"❌ Ошибка авторизации: {e}")
                    return False
        else:
            print("✅ Пользователь уже авторизован!")
        
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
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(auth())
