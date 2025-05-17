# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы (для psycopg2, если используешь PostgreSQL)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Указываем порт
EXPOSE 8000

# Устанавливаем переменную окружения для Python
ENV PYTHONUNBUFFERED=1

# Команда по умолчанию (переопределяется в docker-compose.yml)
CMD ["python", "project/manage.py", "runserver", "0.0.0.0:8000"]
