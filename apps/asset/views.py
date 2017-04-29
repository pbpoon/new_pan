from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import FormView, ListView, DetailView
from account.forms import FileForm
from .models import Area, Category, LandNum, LandOwnerShip, LandOwner
from account.models import People, Account
import xlrd
import decimal


class OwnerListView(ListView):
    context_object_name = 'asset_list'
    qs = LandOwner.objects.filter(landownership__isnull=False)
    owner_list = []
    for i in qs:
        if i not in owner_list:
            owner_list.append(i)
    queryset = owner_list
    template_name = 'asset/index.html'


class PeopleLandListView(DetailView):
    context_object_name = 'people'
    model = LandOwner
    template_name = 'asset/owner_land_list.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(PeopleLandListView, self).get_context_data(**kwargs)
        context['landnum_list'] = LandNum.objects.filter(owner=self.object)
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
            old_owner = []
            area = [Area(name=str(x)) for x in set(table.col_values(2, 1))]
            categroy = [Category(name=str(x)) for x in set(table.col_values(1, 1))]
            account = Account.objects.get(name='xxx')
            # for x in set(table.col_values(0, 1)):
            #     if not People.objects.filter(first_name=str(x[:1]), last_name=str(x[1:6])):
            #         old_owner.append(People(first_name=str(x[:1]), last_name=str(x[1:6]), sex='male', is_del=True,
            #                                 account=account))
            # print(old_owner)
            # People.objects.bulk_create(old_owner)
            # Area.objects.bulk_create(area)
            # Category.objects.bulk_create(categroy)
            for rownum in range(1, nrows):
                row = table.row_values(rownum)
                for index, i in enumerate(range(len(colnames))):
                    if row:

                        if index == 0:
                            sname = str(row[i])
                            # row[7] = str(row[i])
                            row[i] =People.objects.get(first_name=sname[:1], last_name=sname[1:6])
                            # else:
                            #     row[i] = None
                        elif index == 1:
                            row[i] = Category.objects.get(name=str(row[i]))
                        elif index == 2:
                            row[i] = Area.objects.get(name=str(row[i]))
                        elif index == 4:
                            row[i] = decimal.Decimal(row[i])
                        elif index == 6:
                            if row[i]:
                                row[i] = row[5] + '--编辑备注:' + str(row[i])
                            else:
                                row[i] = row[5]
                        else:
                            row[i] = str(row[i])


                # # if not LandNum.objects.filter(area=row[2], num=row[3]):
                land = LandNum.objects.create(area=row[2], num=row[3], category=row[1], fm=row[4], ps=row[6])
                owner= LandOwnerShip.objects.create(num=land, owner=row[0], old_owner=row[0], ps=row[6])
                # land.owner.add(LandOwnerShip.objects.filter(num=row[3]))

            print('OK')
        return HttpResponse('OK')
                # account = row[10],
        # People.objects.bulk_create(list)