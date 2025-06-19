# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Установка зависимостей системы
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --upgrade pip \
    && pip install django pillow python-dotenv toml

# Копируем проект
COPY . .

# Копируем .env, если есть (или используйте переменные окружения при запуске)
# COPY .env .

# Открываем порт
EXPOSE 8000

# Команда запуска: миграции, сборка статики, запуск сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"] 