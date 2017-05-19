from django.contrib import admin
from .models import MoneyAccount

@admin.register(MoneyAccount)
class MoneyAccountAdmin(admin.ModelAdmin):
    pass


