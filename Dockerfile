# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

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
CMD ["python", "manage.py"]