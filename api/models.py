from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class OperatorCodeModel(models.Model):
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'Код оператора'


class TimeZoneModel(models.Model):
    name = models.CharField(max_length=63)
    timezone = models.CharField(max_length=63, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Временная зона'


class ClientModel(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    operator_code = models.ForeignKey(OperatorCodeModel, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)
    timezone = models.ForeignKey(TimeZoneModel, on_delete=models.PROTECT)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name_plural = 'Клиент'


class MailingListModel(models.Model):
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    operator_code = models.ForeignKey(OperatorCodeModel, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name_plural = 'Рассылка'


class MessageModel(models.Model):
    creation_datetime = models.DateTimeField()
    STATUS_CHOICE = (
        (1, 'Sent'),
        (2, 'Waiting'),
        (3, 'Not sent'),
    )
    status = models.IntegerField(choices=STATUS_CHOICE, default=3)
    mailing_list = models.ForeignKey(MailingListModel, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Cообщение'