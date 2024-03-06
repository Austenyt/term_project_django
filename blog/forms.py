from django import forms
from .models import Blog


class StyleFormMixin:
    """
    Миксин, добавляющий класс CSS 'form-control' к каждому полю формы.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogForm(StyleFormMixin, forms.ModelForm):
    """
    Форма для создания или редактирования блога.
    """

    class Meta:
        model = Blog
        fields = ['title', 'body', 'preview', 'is_published']
        widgets = {
            'preview': forms.FileInput(attrs={'multiple': True})
        }
