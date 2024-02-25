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
        fields = ['clients', 'date', 'time', 'frequency', 'message', 'is_active']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
