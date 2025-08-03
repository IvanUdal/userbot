# 🔄 Git Workflow для Telegram Userbot

## 📋 Обзор

Этот документ описывает стандарты работы с Git для проекта Telegram Userbot, обеспечивающие качество кода и эффективную командную работу.

## 🎯 Основные принципы

### 1. **Семантическое версионирование**
```
MAJOR.MINOR.PATCH
- MAJOR: несовместимые изменения API
- MINOR: новая функциональность (обратная совместимость)
- PATCH: исправления багов (обратная совместимость)
```

### 2. **Conventional Commits**
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Типы коммитов:**
- `feat:` - новая функциональность
- `fix:` - исправление бага
- `docs:` - изменения в документации
- `style:` - форматирование кода
- `refactor:` - рефакторинг
- `test:` - добавление тестов
- `chore:` - обновление зависимостей

## 🌿 Структура веток

### **Основные ветки:**
- `main` - стабильная версия
- `develop` - разработка
- `feature/*` - новые функции
- `hotfix/*` - срочные исправления
- `release/*` - подготовка релиза

### **Схема ветвления:**
```
main ← develop ← feature/user-management
     ↑
hotfix/critical-bug
```

## 🚀 Workflow

### **1. Начало работы**
```bash
# Клонирование репозитория
git clone https://github.com/username/userbot.git
cd userbot

# Создание ветки разработки
git checkout -b develop
git push -u origin develop
```

### **2. Создание feature ветки**
```bash
# Переключение на develop
git checkout develop
git pull origin develop

# Создание feature ветки
git checkout -b feature/new-pipeline
```

### **3. Разработка**
```bash
# Регулярные коммиты
git add .
git commit -m "feat: add new pipeline for analytics"

# Push в feature ветку
git push origin feature/new-pipeline
```

### **4. Code Review**
```bash
# Создание Pull Request
# Слияние через GitHub/GitLab интерфейс
```

### **5. Слияние в develop**
```bash
# После одобрения PR
git checkout develop
git pull origin develop
git merge feature/new-pipeline
git push origin develop
```

## 📝 Стандарты коммитов

### **Примеры хороших коммитов:**
```bash
git commit -m "feat(pipeline): add analytics destination support"
git commit -m "fix(security): resolve session string vulnerability"
git commit -m "docs(commands): update pipeline management guide"
git commit -m "refactor(config): simplify environment loading"
```

### **Примеры плохих коммитов:**
```bash
git commit -m "fix bug"  # Слишком общий
git commit -m "update"   # Неинформативный
git commit -m "WIP"      # Неполный
```

## 🔍 Code Review

### **Что проверять:**
1. **Функциональность** - код работает как ожидается
2. **Безопасность** - нет уязвимостей
3. **Производительность** - нет утечек памяти
4. **Читаемость** - понятный код
5. **Документация** - обновлены README и docstrings

### **Checklist для PR:**
- [ ] Код соответствует стандартам проекта
- [ ] Добавлены/обновлены тесты
- [ ] Обновлена документация
- [ ] Проверена безопасность
- [ ] Нет конфликтов с main/develop

## 🏷️ Теги и релизы

### **Создание релиза:**
```bash
# Подготовка релиза
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# Обновление версии
# В main_pipeline.py или config.py
version = "1.2.0"

# Коммит изменений
git add .
git commit -m "chore: bump version to 1.2.0"

# Слияние в main
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# Слияние в develop
git checkout develop
git merge release/v1.2.0
git push origin develop
```

## 🚨 Hotfix процесс

### **Срочные исправления:**
```bash
# Создание hotfix ветки от main
git checkout main
git pull origin main
git checkout -b hotfix/critical-security-fix

# Исправление
# ... внесение изменений ...

# Коммит и тег
git add .
git commit -m "fix(security): patch critical vulnerability"
git tag -a v1.1.1 -m "Hotfix release 1.1.1"

# Слияние в main и develop
git checkout main
git merge hotfix/critical-security-fix
git push origin main --tags

git checkout develop
git merge hotfix/critical-security-fix
git push origin develop
```

## 📊 Мониторинг и метрики

### **Полезные команды:**
```bash
# Статистика коммитов
git log --oneline --graph --all

# Кто что изменил
git blame main_pipeline.py

# Размер изменений
git diff --stat HEAD~1

# Несохраненные изменения
git status
```

## 🔧 Настройка Git

### **Глобальные настройки:**
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "code --wait"
```

### **Настройки проекта:**
```bash
# .gitignore
__pycache__/
*.pyc
.env
*.session
logs/
data/
venv/
```

### **Git hooks (опционально):**
```bash
# pre-commit hook для проверки кода
pip install pre-commit
pre-commit install
```

## 🎯 Best Practices

### **1. Частые коммиты**
- Делайте коммиты часто и по логическим блокам
- Каждый коммит должен быть самодостаточным

### **2. Описательные сообщения**
- Используйте present tense ("add feature" не "added feature")
- Первая строка < 50 символов
- Описывайте "что" и "почему", не "как"

### **3. Ветвление**
- Создавайте ветки для каждой задачи
- Используйте понятные имена веток
- Удаляйте ветки после слияния

### **4. Code Review**
- Всегда делайте code review
- Будьте конструктивными в комментариях
- Проверяйте не только код, но и тесты

## 🚨 Антипаттерны

### **Избегайте:**
- Коммитов "WIP" или "temp"
- Слияния без code review
- Прямых коммитов в main
- Больших коммитов с множественными изменениями
- Коммитов с отладочным кодом

## 📚 Дополнительные ресурсы

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 🔄 Обновление документа

Этот документ должен обновляться при изменении процессов разработки. Коммиты с изменениями в этом файле должны использовать тип `docs(workflow)`. 