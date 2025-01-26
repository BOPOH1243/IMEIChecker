# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app
COPY db /app/db

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Устанавливаем переменные среды (опционально, можно переопределить в docker-compose.yml)
ENV API_SANDBOX_TOKEN=Uor8AZbHYRb6ocM13TYgOLDDTbhdDC4whQeP1SrJ27c45746 \
    API_LIVE_TOKEN=sy5woSxuac7xKalljXFjgbB2hCRw7GQLueRtGp1974d8fe72 \
    PYTHONPATH=/app \
    TELEGRAM_BOT_TOKEN=7950989453:AAHRsPWrOU4CYWj03muFb4g4WpNS5fp1qWE

# Указываем команду для запуска приложения
CMD ["python", "tg_bot/main.py"]
