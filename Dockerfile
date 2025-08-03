# Dockerfile для Telegram Userbot
# Включает поддержку пересылки и парсинга сообщений

# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем метаданные
LABEL maintainer="Telegram Userbot"
LABEL description="Telegram Userbot с функциями пересылки и парсинга сообщений"
LABEL version="1.0.0"

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Создаем необходимые директории
RUN mkdir -p /app/data /app/logs /app/sessions /app/config

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash userbot && \
    chown -R userbot:userbot /app

# Переключаемся на пользователя
USER userbot

# Устанавливаем переменные окружения
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Открываем порт для мониторинга (опционально)
EXPOSE 8080

# Создаем health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# Создаем точку входа
ENTRYPOINT ["python", "main_pipeline.py"] 