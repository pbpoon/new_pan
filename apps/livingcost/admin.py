from django.contrib import admin
from .models import CenterWater, WaterNum, WaterRate
# Register your models here.


class InlineCenterWaterRate(admin.TabularInline):
    model = WaterRate
    raw_id_fields = ['mark_d']


class InlineNumWaterRate(admin.TabularInline):
    model = WaterRate
    raw_id_fields = ['WaterNum']


@admin.register(CenterWater)
class CenterWaterAdmin(admin.ModelAdmin):
    list_display = ['mark_d', 'meter_num', 'get_total_m3', 'real_price', 'ps', 'is_pay']
    inlines = [InlineCenterWaterRate]


@admin.register(WaterNum)
class WaterNumAdmin(admin.ModelAdmin):
    list_display = ['account','desc']
    inlines = [InlineNumWaterRate]