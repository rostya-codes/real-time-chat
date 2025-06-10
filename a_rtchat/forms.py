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
                'autofocus': True
            }),
        }


class NewGroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Aa',
                'class': 'p-4 text-black',
                'maxlenght': '300',
                'autofocus': True,
            }),
        }


class ChatRoomEditForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold mb-4',
                'maxlength': '300',
            }),
        }
