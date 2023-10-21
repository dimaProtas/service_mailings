from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import MailingListModel
from api.task import log_mailings
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


@receiver(post_save, sender=MailingListModel)
def execute_log_mailings(sender, instance, **kwargs):
    current_time = timezone.localtime(timezone.now())
    # Вызываем функцию log_mailings, передавая объект MailingListModel
    if instance.start_datetime <= current_time and current_time <= instance.end_datetime:
        print('Задача выпоняеться', instance.start_datetime, current_time, current_time < instance.end_datetime)
        log_mailings.delay(instance.id)
        logger.info(f'Задача выполняеться id: {instance.id}')
    else:
        print('Отложенная задача', instance.start_datetime, current_time, current_time < instance.end_datetime)
        time_interval = instance.start_datetime - current_time
        # отложенный запуск задачи
        log_mailings.apply_async(args=(instance.id,), eta=current_time + time_interval)
        logger.info(f'Отложенная задача id: {instance.id}, запущена {current_time}, выполнитьсся через {time_interval}')
