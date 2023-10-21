FROM python:3.10


RUN apt-get update && apt-get install -y netcat-openbsd

# Устанавливаем зависимости
RUN pip install --upgrade pip

# Указываем рабочую директорию внутри контейнера
WORKDIR /service_mailings

# Копируем файлы приложения в контейнер
COPY . /service_mailings

# Устанавливаем зависимости из requirements.txt
RUN pip install -r requirements.txt

# Запускаем Celery в контейнере
CMD celery -A service_mailings worker --loglevel=info


#python manage.py api/fixtures/001_users.json loaddata api/fixtures/002_tag.json api/fixtures/003_operator_code.json api/fixtures/004_timezone.json api/fixtures/005_client.json