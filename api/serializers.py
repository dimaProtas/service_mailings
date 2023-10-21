from rest_framework import serializers
from .models import ClientModel, MailingListModel, MessageModel, TimeZoneModel, Tag, OperatorCodeModel


class OperatorCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatorCodeModel
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = '__all__'


class TimeZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeZoneModel
        fields = '__all__'


class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingListModel
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = '__all__'
