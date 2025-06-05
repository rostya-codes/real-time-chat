from django.forms import ModelForm
from django import forms

from .models import *


class ChatMessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Aa',
                'class': 'p-4 text-blank',
                'maxlength': '300',
                'autofocus': True}
            )
        }
