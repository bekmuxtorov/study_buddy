from django.forms import ModelForm
from . import models


class RoomForms(ModelForm):
    class Meta:
        model = models.Room
        fields = ['topic', 'name', 'description',]


class MessageForms(ModelForm):
    class Meta:
        model = models.Message
        fields = ['body',]
