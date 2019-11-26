from django.contrib import admin
from .models import MessageNew, MessageLike

# Register your models here.

admin.site.register(MessageNew)
admin.site.register(MessageLike)
