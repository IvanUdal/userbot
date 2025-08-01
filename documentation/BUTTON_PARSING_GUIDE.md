# 🔘 Парсинг кнопок в Telegram

## 🎯 Обзор

Парсинг кнопок позволяет извлекать информацию о inline keyboard и обычных кнопках в сообщениях Telegram. Это полезно для анализа интерактивного контента и понимания пользовательского взаимодействия.

## 📋 Типы кнопок

### 1. **URL кнопки** (`url`)
```python
{
    "text": "Открыть сайт",
    "button_type": "url",
    "url": "https://example.com"
}
```

### 2. **Callback кнопки** (`callback`)
```python
{
    "text": "Нажми меня",
    "button_type": "callback",
    "data": "button_action_123"
}
```

### 3. **Web App кнопки** (`web_app`)
```python
{
    "text": "Открыть приложение",
    "button_type": "web_app",
    "web_app_url": "https://t.me/app"
}
```

### 4. **Switch Inline кнопки** (`switch_inline`)
```python
{
    "text": "Поделиться",
    "button_type": "switch_inline",
    "data": "share_message"
}
```

### 5. **Обычные кнопки** (`text`)
```python
{
    "text": "Простая кнопка",
    "button_type": "text"
}
```

## 🔧 Настройка парсинга кнопок

### В .env файле:
```env
# Включить парсинг кнопок
PARSE_BUTTONS=true

# Другие настройки парсинга
PARSING_ENABLED=true
PARSING_GROUP_ID=-1001234567890
```

### В коде:
```python
# Проверка включения парсинга кнопок
if config.parse_buttons:
    buttons = await parser.parse_buttons(event.reply_markup)
```

## 📊 Структура данных

### Пример JSON с кнопками:
```json
{
  "message_id": 12345,
  "chat_id": -1001234567890,
  "sender": {
    "id": 987654321,
    "name": "Бот",
    "username": "@mybot"
  },
  "content": {
    "text": "Выберите действие:",
    "buttons": [
      {
        "text": "Информация",
        "button_type": "callback",
        "data": "info_action"
      },
      {
        "text": "Сайт",
        "button_type": "url",
        "url": "https://example.com"
      },
      {
        "text": "Приложение",
        "button_type": "web_app",
        "web_app_url": "https://t.me/app"
      }
    ]
  },
  "metadata": {
    "timestamp": "2024-01-15T14:30:00Z",
    "is_bot": true
  }
}
```

## 🚀 Использование

### 1. **Запуск парсинга с кнопками:**
```python
# Включи парсинг кнопок в .env
PARSE_BUTTONS=true

# Запусти парсинг
await parser.start_parsing(chat_id)
```

### 2. **Просмотр статистики:**
```python
stats = parser.get_stats()
print(f"Сообщений с кнопками: {stats['messages_with_buttons']}")
```

### 3. **Анализ кнопок:**
```python
# Получи все кнопки из сообщения
buttons = parsed_message.buttons

for button in buttons:
    print(f"Кнопка: {button.text}")
    print(f"Тип: {button.button_type}")
    
    if button.button_type == "url":
        print(f"URL: {button.url}")
    elif button.button_type == "callback":
        print(f"Data: {button.data}")
```

## 📈 Анализ данных

### Статистика по типам кнопок:
```python
def analyze_buttons(messages):
    button_types = {}
    total_buttons = 0
    
    for message in messages:
        if 'buttons' in message:
            for button in message['buttons']:
                button_type = button['button_type']
                button_types[button_type] = button_types.get(button_type, 0) + 1
                total_buttons += 1
    
    return {
        'total_buttons': total_buttons,
        'by_type': button_types
    }
```

### Популярные callback данные:
```python
def analyze_callback_data(messages):
    callback_data = {}
    
    for message in messages:
        if 'buttons' in message:
            for button in message['buttons']:
                if button['button_type'] == 'callback':
                    data = button['data']
                    callback_data[data] = callback_data.get(data, 0) + 1
    
    return dict(sorted(callback_data.items(), key=lambda x: x[1], reverse=True))
```

## 🔍 Примеры использования

### 1. **Анализ ботов:**
```python
# Найди сообщения от ботов с кнопками
bot_messages_with_buttons = [
    msg for msg in messages 
    if msg.get('is_bot') and msg.get('buttons')
]

print(f"Ботов с кнопками: {len(bot_messages_with_buttons)}")
```

### 2. **Поиск URL кнопок:**
```python
# Найди все URL кнопки
url_buttons = []
for message in messages:
    if 'buttons' in message:
        for button in message['buttons']:
            if button['button_type'] == 'url':
                url_buttons.append({
                    'text': button['text'],
                    'url': button['url'],
                    'message_id': message['message_id']
                })

print(f"URL кнопок найдено: {len(url_buttons)}")
```

### 3. **Анализ интерактивности:**
```python
# Подсчитай интерактивность сообщений
interactive_messages = 0
total_messages = len(messages)

for message in messages:
    if 'buttons' in message and message['buttons']:
        interactive_messages += 1

interactivity_rate = (interactive_messages / total_messages) * 100
print(f"Интерактивность: {interactivity_rate:.1f}%")
```

## ⚠️ Ограничения

### 1. **Права доступа:**
- ✅ Достаточно быть участником группы
- ❌ НЕ нужно быть администратором
- ✅ Нужны права на чтение сообщений

### 2. **Технические ограничения:**
- Кнопки парсятся только из новых сообщений
- Callback данные могут быть зашифрованы
- Некоторые типы кнопок могут быть недоступны

### 3. **Этические соображения:**
- Получи разрешение на парсинг
- Не используй данные для спама
- Соблюдай правила группы

## 🛠️ Отладка

### Проверка парсинга кнопок:
```python
# Включи отладочный режим
LOG_LEVEL=DEBUG

# Проверь логи
docker-compose logs -f telegram-userbot
```

### Тестовая команда:
```python
# Добавь в бота команду для тестирования
@client.on(events.NewMessage(pattern=r'\.test_buttons'))
async def test_buttons(event):
    # Создай сообщение с кнопками для тестирования
    buttons = [
        [Button.inline("Тест", b"test_callback")],
        [Button.url("Сайт", "https://example.com")]
    ]
    
    await event.respond("Тестовые кнопки:", buttons=buttons)
```

## 📊 Экспорт данных

### CSV экспорт с кнопками:
```python
# Кнопки будут экспортированы как JSON в CSV
await parser.export_to_csv("data/export_with_buttons.csv")
```

### JSON экспорт:
```python
# Полные данные с кнопками в JSON
with open("data/parsed_messages.json", "r") as f:
    data = json.load(f)
    
# Фильтруй сообщения с кнопками
messages_with_buttons = [msg for msg in data if msg.get('buttons')]
```

## 🎯 Лучшие практики

### 1. **Фильтрация данных:**
```python
# Фильтруй только нужные типы кнопок
def filter_buttons_by_type(messages, button_type):
    filtered = []
    for message in messages:
        if 'buttons' in message:
            message_buttons = [b for b in message['buttons'] if b['button_type'] == button_type]
            if message_buttons:
                filtered.append({
                    **message,
                    'buttons': message_buttons
                })
    return filtered
```

### 2. **Агрегация статистики:**
```python
# Создай сводку по кнопкам
def create_button_summary(messages):
    summary = {
        'total_messages': len(messages),
        'messages_with_buttons': len([m for m in messages if m.get('buttons')]),
        'total_buttons': sum(len(m.get('buttons', [])) for m in messages),
        'button_types': {},
        'top_callback_data': {}
    }
    
    # Анализируй типы кнопок
    for message in messages:
        for button in message.get('buttons', []):
            button_type = button['button_type']
            summary['button_types'][button_type] = summary['button_types'].get(button_type, 0) + 1
    
    return summary
```

### 3. **Визуализация:**
```python
# Создай график типов кнопок
import matplotlib.pyplot as plt

def plot_button_types(summary):
    types = list(summary['button_types'].keys())
    counts = list(summary['button_types'].values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(types, counts)
    plt.title('Распределение типов кнопок')
    plt.ylabel('Количество')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('button_types.png')
```

## 🎯 Итог

Парсинг кнопок позволяет:
- ✅ **Анализировать интерактивность** - понимать, как пользователи взаимодействуют с контентом
- ✅ **Изучать ботов** - анализировать функциональность Telegram ботов
- ✅ **Отслеживать ссылки** - собирать URL из кнопок
- ✅ **Исследовать UX** - понимать паттерны использования кнопок
- ✅ **Создавать отчеты** - генерировать статистику по интерактивности

**Важно:** Всегда получай разрешение на парсинг и используй данные этично! 🔒 