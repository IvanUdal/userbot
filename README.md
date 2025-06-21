# Telegram Userbot

Простой Telegram userbot на основе библиотеки Telethon.

## 🚀 Установка и настройка

### 1. Создание и активация виртуального окружения
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Установка зависимостей
```powershell
pip install -r requirements.txt
```

### 3. Получение API ключей
1. Перейдите на https://my.telegram.org
2. Войдите в свой Telegram аккаунт
3. Создайте новое приложение
4. Скопируйте `API ID` и `API Hash`

### 4. Настройка конфигурации
Отредактируйте файл `config.py`:
```python
API_ID = 12345678  # Ваш API ID
API_HASH = 'your_api_hash_here'  # Ваш API Hash
```

### 5. Запуск
```powershell
python main.py
```

При первом запуске вас попросят ввести номер телефона и код подтверждения.

## 📋 Доступные команды

- `.ping` - Проверка работы бота
- `.info` - Информация о текущем сообщении/чате

## ⚠️ Важно

- Не делитесь своими API ключами
- Используйте userbot ответственно
- Соблюдайте правила Telegram

## 🔧 Добавление новых команд

Пример добавления новой команды:

```python
@client.on(NewMessage(pattern=f'\\{CMD_PREFIX}hello'))
async def hello_handler(event):
    """Команда .hello"""
    await event.edit('👋 Привет!')
``` 