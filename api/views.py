from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import ClientModel, MailingListModel, MessageModel, Tag, TimeZoneModel, OperatorCodeModel
from .serializers import ClientSerializer, MailingListSerializer, MessageSerializer, TagSerializer, TimeZoneSerializer, OperatorCodeSerializer
from rest_framework.decorators import action
from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # Проверяем, что пользователь авторизован
        return request.user.is_authenticated


class ClientViewSet(viewsets.ModelViewSet):
    queryset = ClientModel.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete_client(self, request, pk=None):
        try:
            client = self.get_object()
            client.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        except ClientModel.DoesNotExist:
            return Response({"detail": "Client not found"}, status=status.HTTP_404_NOT_FOUND)


class MailingListViewSet(viewsets.ModelViewSet):
    queryset = MailingListModel.objects.all()
    serializer_class = MailingListSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True)
    def delete_mailing_list(self, request, pk=None):
        try:
            mailing_list = self.get_object()
            mailing_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MailingListModel.DoesNotExist:
            return Response({"detail": "MailingList not found"}, status=status.HTTP_404_NOT_FOUND)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageSerializer


class TimeZoneViewSet(viewsets.ModelViewSet):
    queryset = TimeZoneModel.objects.all()
    serializer_class = TimeZoneSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OperatorCodeViewSet(viewsets.ModelViewSet):
    queryset = OperatorCodeModel.objects.all()
    serializer_class = OperatorCodeSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)