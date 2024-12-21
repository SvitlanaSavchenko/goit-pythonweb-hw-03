# Використання базового образу Python
FROM python:3.10-slim

# Робоча директорія
WORKDIR /app

# Копіювання файлів проекту
COPY . /app

# Встановлення залежностей
RUN pip install flask

# Відкриття порту 3000
EXPOSE 3000

# Команда для запуску додатку
CMD ["python", "app.py"]
