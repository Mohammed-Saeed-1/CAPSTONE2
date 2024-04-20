# from django.contrib import admin
from django.apps import AppConfig


class UtradeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'utrade'

# admin.py
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'favorite_stocks', 'plans', 'wallet')  # Add 'favorite_stocks' to the list_display

from .models import Stock, StockData

admin.site.register(Stock)
admin.site.register(StockData)