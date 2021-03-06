from django.contrib import admin
from .models import Account, People

class inlinePeople(admin.TabularInline):
    model = People
    raw_id_fields = ['account']
    extra = 1


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated']
    list_filter = ['name', 'created', 'updated']
    search_fields = ['name']
    inlines = [inlinePeople]


@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'sex', 'id_card_num', 'is_main', 'account', 'birthday', 'is_marry',
                    'is_getmoney', 'join_d', 'created', 'updated']
    list_display_links = ['first_name', 'last_name']
    list_filter = ['first_name',  'sex', 'is_main', 'is_getmoney']
    search_fields = ['first_name', 'last_name', 'sex', 'id_card_num', 'account__name']

    def get_queryset(self, request):
        qs = super(PeopleAdmin, self).get_queryset(request)
        return qs.filter(is_del=False)

