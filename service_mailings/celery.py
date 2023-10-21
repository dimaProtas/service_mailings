from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging


# Устанавливаю переменную окружения, которая указывает Celery, как использовать настройки Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service_mailings.settings')

app = Celery('myapp', broker='pyamqp://guest:guest@rabbitmq:5672//')

# настройки из файла settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически загружайте задачи из всех приложений Django
app.autodiscover_tasks()

# Создать логгер для Celery
celery_logger = logging.getLogger('celery')
celery_logger.setLevel(logging.DEBUG)  # Установите желаемый уровень логирования

# Добавить обработчик для записи в файл
handler = logging.FileHandler('logs/celery.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
celery_logger.addHandler(handler)



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# Команда запуска celery
# celery -A service_mailings worker --loglevel=info


