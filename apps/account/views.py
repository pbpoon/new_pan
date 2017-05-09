from django.shortcuts import HttpResponse
from django.views.generic import ListView, DetailView, FormView
import xlrd
from xlrd.xldate import xldate_as_datetime

from .models import Account, People
from asset.models import LandOwner
from .forms import FileForm

from django.contrib.auth.mixins import LoginRequiredMixin


class AccountListView(ListView):
    queryset = Account.objects.filter(people__is_del=False).distinct()
    template_name = 'account/index.html'
    context_object_name = 'account_list'


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'account/detail.html'
    context_object_name = 'account'
    slug_field = 'name' #重新设定slug的字段
    slug_url_kwarg = 'name' #定位到slug字段，可能他存入的是字典类型
    # redirect_field_name = 'user'
    # raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context['people_list'] = self.object.people.filter(is_del=False)
        context['waternum_list'] = self.object.water_num.all()
        qs = LandOwner.objects.filter(land_num__owner__account=self.object)
        owner_list = []
        for i in qs:
            if i not in owner_list:
                owner_list.append(i)
        context['landnum_list'] = owner_list
        return context


class PeopleView(LoginRequiredMixin, DetailView):
    model = People
    template_name = 'account/people.html'
    context_object_name = 'people'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(PeopleView, self).get_context_data(**kwargs)
        context['account'] = Account.objects.get(people=self.object)
        return context


class FileUploadView(FormView):
    template_name = 'account/file.html'
    form_class = FileForm

    def form_valid(self, form):
        f = form.files.get('file')
        if f:
            data = xlrd.open_workbook(file_contents=f.read())
            # table = data.sheet_by_name(by_name)
            table = data.sheets()[0]
            nrows = table.nrows  # 总行数
            colnames = table.row_values(0)  # 表头列名称数据
            print(colnames)
            list = []
            accounts = [Account(name=str(x)) for x in set(table.col_values(10, 1))]
            print(accounts)
            # Account.objects.bulk_create(accounts)
            for rownum in range(1, nrows):
                row = table.row_values(rownum)
                for index,i in enumerate(range(len(colnames))):
                    if row:
                        if index==4 or index==14:
                            row[i] = xldate_as_datetime(row[i],0)
                        elif index == 8 or index ==13 or index ==15:
                            row[i] = bool(row[i])
                        elif index ==10:
                            row[i] = Account.objects.get(name=str(row[i]))
                        else:
                            row[i] = str(row[i])
                if not People.objects.filter(first_name=row[1],last_name=row[2]):
                    list.append(People(first_name=row[1],last_name=row[2], sex=row[3], birthday=row[4],
                                       nationality=row[5], education=row[6], account_type=row[7], is_marry=row[8],
                                       id_card_num=row[9], phone_num=row[12], is_getmoney=row[13],account=row[10],
                                       join_d=row[14],
                                       is_main=row[15]
                                       ))
                print(list)
                # account = row[10],
        People.objects.bulk_create(list)
        return HttpResponse('OK')
        # form.save()
        # return redirect(order)
