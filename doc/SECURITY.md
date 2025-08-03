# 🔒 Безопасность Telegram Userbot

## ⚠️ ВАЖНО: Защита секретных данных

### Файлы, которые НЕ должны попадать в Git:
- `.env` - содержит API_ID и API_HASH
- `session_string.txt` - содержит строку сессии Telegram
- `bot_token.txt` - содержит токен бота
- `*.session` - файлы сессий Telegram
- `config.env`, `dddd.env`, `no_limits.env` и другие файлы с секретными данными

### Что уже защищено:
✅ Файл `.gitignore` настроен правильно
✅ Секретные данные удалены из `docker-compose.yml`
✅ Создан пример конфигурации `config.example`

### Инструкции по настройке:

1. **Скопируйте пример конфигурации:**
   ```bash
   cp config.example .env
   ```

2. **Заполните секретные данные в `.env`:**
   - Получите API_ID и API_HASH на https://my.telegram.org/apps
   - Добавьте свои данные в файл `.env`

3. **Настройте аутентификацию:**
   ```bash
   python auth_setup.py
   ```

4. **Проверьте, что секретные файлы не попадают в Git:**
   ```bash
   git status
   ```

### Проверка безопасности:
```bash
# Проверьте, что секретные файлы не отслеживаются Git
git check-ignore .env session_string.txt bot_token.txt

# Проверьте, что в docker-compose.yml нет секретных данных
grep -i "api_id\|api_hash" docker-compose.yml
```

### Если секретные данные попали в Git:
1. Немедленно измените API_ID и API_HASH на https://my.telegram.org/apps
2. Удалите файлы из истории Git:
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch .env session_string.txt' --prune-empty --tag-name-filter cat -- --all
   ```
3. Принудительно обновите репозиторий:
   ```bash
   git push origin --force
   ```

## 🛡️ Дополнительные меры безопасности:

1. **Используйте переменные окружения** вместо хардкода
2. **Регулярно обновляйте API ключи**
3. **Не делитесь файлами сессий**
4. **Используйте разные API ключи для разных проектов**
5. **Мониторьте активность аккаунта**

## 📞 Поддержка:
Если у вас есть вопросы по безопасности, создайте issue в репозитории. 