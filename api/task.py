from celery import shared_task
from django.utils import timezone
import time
from django.db.models import Q
from .models import MailingListModel, MessageModel, ClientModel
import requests
import logging
from django.conf import settings


logger = logging.getLogger(__name__)

# Настройки логгера из settings.py
if not logger.hasHandlers():
    logging.config.dictConfig(settings.LOGGING)


# Удаление задачи поле выполнения (ignore_result=True)
@shared_task(ignore_result=True)
def log_mailings(mailing_list_id):
    logger.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(levelname)s - %(message)s')
    # handler = logging.FileHandler('logs/my_task.log')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)

    current_time = timezone.localtime(timezone.now())
    mailing = MailingListModel.objects.get(id=mailing_list_id)


    if mailing.start_datetime < current_time and current_time < mailing.end_datetime:
        message_data = {
            "id": mailing.id,
            "start_datetime": mailing.start_datetime,
            "message": mailing.message,
        }

        mailing_tags = mailing.tags.all()  # Получить теги рассылки

        operator_code_filter = Q(operator_code=mailing.operator_code)

        # Получите клиентов с совпадающим operator_code
        clients = ClientModel.objects.filter(operator_code_filter)

        # Теперь создайте фильтр для клиентов, у которых есть хотя бы один из выбранных тегов
        tag_filter = Q()
        for tag in mailing_tags:
            tag_filter |= Q(tags=tag)

        clients = clients.filter(tag_filter).distinct()

        for client in clients:
            client_message = {
                "id": client.id,
                "phone_number": client.phone_number,
                "operator_code": client.operator_code,
                "timezone": client.timezone,
            }

            message = MessageModel(
                creation_datetime=current_time,
                status=1,
                mailing_list=mailing,
                client=client,
            )
            message.save()
            logger.info(f'Сообщение сохранено в статистику как отправленное id: {message.id}')

            #URL эндпоинта для отправки сообщения
            send_message_url = f"https://probe.fbrq.cloud/v1/send/{message.id}"

            # JWT-токен
            jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg0ODg1NTIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9Qcm9EaW1hcyJ9.WkqGPTICVP7AYzGOUk3_999glQJZlwKBmWOrZVrNcFs"

            # Заголовок с JWT-токеном
            headers = {
                "Authorization": f"Bearer {jwt_token}"
            }
            send_message_data = {
                'id': message.id,
                'phone': message.client.phone_number,
                'text': mailing.message
            }

            send_message(send_message_url, send_message_data, headers)

    else:
        logger.info("Время рассылки закончилось. Задача не выполняется.")


# Функция для отправки сообщения и обработки исключений
def send_message(send_message_url, send_message, headers):
    try:
        response = requests.post(send_message_url, json=send_message, headers=headers)
        logger.info(f'Отправляем запрос на удалённый api {send_message}')
        if response.status_code == 200:
            response_json = response.json()
            if 'code' in response_json and response_json['code'] == 0:
                logger.info(f'Сообщение успешно отправлено ответ response.status_code == {response.status_code}')
                logger.info(f'Ответ: {response_json}')
            else:
                logger.info(f'Некорректные данные в ответе: {response_json}')
                # Повторная попытка отправки через 5 минут
                time.sleep(300)  # Повторить попытку через 5 минут
                send_message(send_message_url, send_message, headers)
                logger.info(f'Повторная отправка сообщения через 5 минут id: {send_message.id}')
        else:
            logger.info(f'Ошибка при отправке сообщения id: {send_message.id}')
            raise Exception("Ошибка при отправке сообщения")
    except requests.exceptions.RequestException as e:
        # Обработка сетевых ошибок
        logger.info(f"Ошибка запроса: {e}")
        # Повторная попытка отправки через 5 минут
        time.sleep(300)  # Повторить попытку через 5 минут
        send_message(send_message_url, send_message, headers)
    except Exception as e:
        # Общая обработка других исключений
        logger.info(f"Необработанная ошибка:{e}")









