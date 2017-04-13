from django.contrib import admin
from .models import Area, Category, LandNum, LandOwnerShip, LandOwner


class InlineAreaLandNum(admin.TabularInline):
    model = LandNum
    extra = 1
    # raw_id_fields = ('area',)


class InlineOwner(admin.TabularInline):
    model = LandOwnerShip
    fk_name = 'owner'
    raw_id_fields = ('owner',)
    extra = 1


class InlineLandNum(admin.TabularInline):
    model = LandOwnerShip
    extra = 1
#     fk_name = 'owner'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc']
    search_fields = ['name', 'desc']
    inlines = [InlineAreaLandNum]


@admin.register(LandOwner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'get_total_land']
    fields = ['first_name', 'last_name']
    inlines = [InlineOwner]


@admin.register(LandNum)
class OwnerAdmin(admin.ModelAdmin):
    inlines = [InlineLandNum]