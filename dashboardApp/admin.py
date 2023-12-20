from django.contrib import admin

from .models import *


# Register your models here.
# class User(admin.ModelAdmin):
admin.site.register(Notes)
admin.site.register(Homework)
admin.site.register(Todo)
