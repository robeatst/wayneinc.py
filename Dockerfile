# 1. Берём готовый образ Python
FROM python:3.11-slim

# 2. Указываем рабочую папку внутри контейнера
WORKDIR /app

# 3. Копируем всё содержимое проекта в контейнер
COPY . .

# 4. Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Убираем буферизацию, чтобы логи шли сразу
ENV PYTHONUNBUFFERED=1

# 6. Запускаем бота
CMD ["python", "main.py"]

