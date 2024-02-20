from django.contrib import admin
from .models import Client, Mailing, Message, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'comment')
    search_fields = ('email', 'full_name')
    list_filter = ('email',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'get_frequency_display', 'status')
    list_filter = ('time', 'frequency', 'status')
    search_fields = ('time', 'status')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'subject')
    search_fields = ('mailing__time', 'subject')
    list_filter = ('mailing',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'timestamp', 'status')
    search_fields = ('mailing__time', 'status')
    list_filter = ('mailing', 'status')
