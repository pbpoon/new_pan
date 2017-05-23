from django.contrib import admin
from .models import MoneyAccount, Tag, Document
from sorl.thumbnail.admin import AdminImageMixin #缩略图的adminmixin


class DocumentInline(AdminImageMixin, admin.TabularInline):
    model = Document
    raw_id_fields = ['money_num']


@admin.register(MoneyAccount)
class MoneyAccountAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ['num', 'date', 'detail', 'type','status', 'amount', 'get_balance', 'operator', 'ps', 'update_d']
    readonly_fields = ['num', 'get_balance']
    inlines = (DocumentInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass