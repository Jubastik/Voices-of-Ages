# Используем официальный образ Python 3.12 как базовый
FROM python:3.12-slim

# Устанавливаем переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновляем
RUN apt-get update

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости проекта с помощью Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . /app

# Команда для запуска вашего приложения
CMD ["python", "-m", "src"]
