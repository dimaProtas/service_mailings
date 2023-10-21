import pytest
from celery import current_app, Celery
from api.models import MailingListModel, OperatorCodeModel, Tag
from api.task import log_mailings
from datetime import datetime
from django.utils import timezone


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'pyamqp://guest:guest@localhost:5672//',
        'result_backend': 'rpc',
    }

def test_my_celery_task(celery_config):
    app = Celery('myapp', broker=celery_config['broker_url'], backend=celery_config['result_backend'])

    result = app.send_task('my_task_name', args=(1,))

    assert result.status == 'PENDING'


@pytest.mark.django_db
def test_log_mailings(celery_config):
    app = Celery('myapp', broker=celery_config['broker_url'], backend=celery_config['result_backend'])

    mailing_list = MailingListModel.objects.create(
        start_datetime=timezone.now(),
        end_datetime=datetime.fromisoformat('2023-10-20 17:36:06.593577+00:00'),
        message='Test Message',
        operator_code=OperatorCodeModel.objects.create(code="1"),
    )
    tag = Tag.objects.create(name="Test Tag")
    mailing_list.tags.set([tag])

    task = log_mailings.s(mailing_list.id)
    result = task.apply()

    # Проверяем, что задача была выполнена успешно
    assert result.status == 'SUCCESS'
