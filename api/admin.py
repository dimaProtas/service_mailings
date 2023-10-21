from django.contrib import admin
from .models import MessageModel, MailingListModel, ClientModel, Tag, OperatorCodeModel, TimeZoneModel


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'creation_datetime', 'status', 'mailing_list', 'client']
    list_display_links = ['id']


class MailingListAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_datetime', 'end_datetime', 'message', 'operator_code']
    list_display_links = ['id']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone_number', 'operator_code', 'timezone']
    list_display_links = ['id']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id']


class OperationCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code']
    list_display_links = ['id']


class TimeZoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'timezone']
    list_display_links = ['id']


admin.site.register(TimeZoneModel, TimeZoneAdmin)
admin.site.register(OperatorCodeModel, OperationCodeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ClientModel, ClientAdmin)
admin.site.register(MessageModel, MessageAdmin)
admin.site.register(MailingListModel, MailingListAdmin)
