from django.forms import ModelForm
from . import models


class RoomForms(ModelForm):
    class Meta:
        model = models.Room
        fields = '__all__'
