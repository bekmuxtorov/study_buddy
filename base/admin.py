from django.contrib import admin
from . import models

# Register your models here.


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'topic', 'update', 'created']


class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'created']


admin.site.register(models.Room, RoomAdmin)
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Message, MessageAdmin)
