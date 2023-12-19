from django.contrib import admin

from .models import *


# Register your models here.
# class User(admin.ModelAdmin):
admin.site.register(Notes)
