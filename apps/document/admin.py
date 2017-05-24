from django.contrib import admin
from .models import Category, Document, DocumentItem


class DocumentItemInline(admin.TabularInline):
    model = DocumentItem
    fields = ['file', 'name', 'desc']
    raw_id_fields = ['document']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['category', 'title', 'desc', 'item_count']
    readonly_fields = ['views', 'item_count']
    inlines = [DocumentItemInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass