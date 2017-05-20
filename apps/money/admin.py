from django.contrib import admin
from .models import MoneyAccount, Tag, Document


class DocumentInline(admin.TabularInline):
    model = Document
    raw_id_fields = ['money_num']


@admin.register(MoneyAccount)
class MoneyAccountAdmin(admin.ModelAdmin):
    list_display = ['num', 'date', 'detail', 'type','status', 'amount', 'get_balance', 'operator', 'ps', 'update_d']
    readonly_fields = ['get_balance', 'num']
    inlines = (DocumentInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass