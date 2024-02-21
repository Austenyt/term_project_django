from django import forms
from .models import Mailing, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email', 'full_name', 'comment']


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['time', 'frequency', 'client', 'message']

    def clean_time(self):
        time = self.cleaned_data.get('time')

        # Проверяем, что введено время в формате HH:MM
        if time and len(time) == 5 and time[2] != ':':
            # Добавляем двоеточие между часами и минутами
            time = f'{time[:2]}:{time[2:]}'
            self.cleaned_data['time'] = time

        return time


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
