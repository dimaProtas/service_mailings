import pytest
from api.models import Tag, OperatorCodeModel, ClientModel, TimeZoneModel, MailingListModel, MessageModel
from django.utils import timezone
from unittest.mock import patch


@pytest.mark.django_db
def test_create_tag():
    tag = Tag.objects.create(name="Test Tag")
    assert tag.name == "Test Tag"


def test_tag_string_representation():
    tag = Tag(name="Test Tag")
    assert str(tag) == "Test Tag"


@pytest.mark.django_db
def test_create_operator_code():
    code = OperatorCodeModel.objects.create(code="123")
    assert code.code == "123"


def test_operator_code_string_representation():
    code = OperatorCodeModel(code="123")
    assert str(code) == "123"


@pytest.mark.django_db
def test_create_time_zone():
    time_zone = TimeZoneModel.objects.create(name="Test Zone", timezone="UTC")
    assert time_zone.timezone == "UTC"


def test_time_zone_string_representation():
    time_zone = TimeZoneModel(name="Test Zone", timezone="UTC")
    assert str(time_zone) == "Test Zone"


@pytest.mark.django_db
def test_create_client():
    operator_code = OperatorCodeModel.objects.create(code="123")
    time_zone = TimeZoneModel.objects.create(name="Test Zone", timezone="UTC")
    client = ClientModel.objects.create(
        phone_number="1234567890",
        operator_code=operator_code,
        timezone=time_zone,
    )
    assert client.phone_number == "1234567890"


@pytest.mark.django_db
def test_client_string_representation():
    operator_code = OperatorCodeModel.objects.create(code="123")
    time_zone = TimeZoneModel.objects.create(name="Test Zone", timezone="UTC")
    client = ClientModel(
        phone_number="1234567890",
        operator_code=operator_code,
        timezone=time_zone,
    )
    assert str(client) == "1234567890"


@patch('celery.app.task.Task.apply_async')
@pytest.mark.django_db
def test_create_mailing_list(mock_send_to_celery):

    operator_code = OperatorCodeModel.objects.create(code="123")
    mailing_list = MailingListModel.objects.create(
        start_datetime=timezone.now(),
        end_datetime=timezone.now(),
        message="Test Message",
        operator_code=operator_code,
    )

    # mock_send_to_rabbitmq будет вызван вместо отправки в celery
    assert mailing_list.message == "Test Message"
    mock_send_to_celery.assert_called_once()


@pytest.mark.django_db
def test_mailing_list_string_representation():
    operator_code = OperatorCodeModel.objects.create(code="123")
    mailing_list = MailingListModel(
        message="Test Message",
        operator_code=operator_code,
    )
    assert str(mailing_list) == "Test Message"


@patch('celery.app.task.Task.apply_async')
@pytest.mark.django_db
def test_create_message(mock_send_to_celery):
    client = ClientModel.objects.create(
        phone_number="1234567890",
        operator_code=OperatorCodeModel.objects.create(code="123"),
        timezone=TimeZoneModel.objects.create(name="Test Zone", timezone="UTC"),
    )
    mailing_list = MailingListModel.objects.create(
        message="Test Message",
        operator_code=OperatorCodeModel.objects.create(code="123"),
    )
    message = MessageModel.objects.create(
        creation_datetime=timezone.now(),
        status=1,
        mailing_list=mailing_list,
        client=client,
    )
    assert message.status == 1
    mock_send_to_celery.assert_called_once()


# pytest - тестировать
# python manage.py flush - отчистить тестовую бд
