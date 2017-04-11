from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import FormView, ListView, DateDetailView
from account.forms import FileForm
from .models import Area, Category, LandNum, Owner
from account.models import People
import xlrd
import decimal


class OwnerListView(ListView):
    context_object_name = 'asset_list'
    items=[]
    querysett = Owner.objects.all()
    for item in querysett:
        if item.old_owner not in querysett:
            items.append(item)
    queryset = Owner.objects.filter(old_owner__in=querysett)
    template_name = 'asset/index.html'


# def owner_land_listview(request, owner_id):
#     aold_owner = get_object_or_404(Owner, pk = owner_id).old_owner
#     owner_lst = Owner.objects.filter(old_owner=aold_owner)
#     for i in owner_lst:
#         try:
#             int(i.owner)
#             i.owner = People.objects.get(pk=int(i.owner))
#         except:
#             i.owner = i.owner
#     return render(request, 'asset/owner_land_list.html', locals())


class FileUploadView(FormView):
    template_name = 'account/file.html'
    form_class = FileForm

    # def form_valid(self, form):
    #     f = form.files.get('file')
    #     if f:
    #         data = xlrd.open_workbook(file_contents=f.read())
    #         # table = data.sheet_by_name(by_name)
    #         table = data.sheets()[0]
    #         nrows = table.nrows  # 总行数
    #         colnames = table.row_values(0)  # 表头列名称数据
    #         print(colnames)
    #         list = []
    #         list2 = []
    #         area = [Area(name=str(x)) for x in set(table.col_values(2, 1))]
    #         categroy = [Category(name=str(x)) for x in set(table.col_values(1, 1))]
    #         old_owner = [People(first_name=str(x[:1]), last_name=str(x[1:6])) for x in set(table.col_values(0, 1))]
    #         print(area, categroy, old_owner)
            # Area.objects.bulk_create(area)
            # Category.objects.bulk_create(categroy)
            # for rownum in range(1, nrows):
            #     row = table.row_values(rownum)
            #
            #     for index, i in enumerate(range(len(colnames))):
            #         if row:
            #             if index == 0:
            #                 people = People.objects.all()
            #                 sname = str(row[i])
            #                 row[7] = str(row[i])
            #                 if people.filter(first_name=sname[:1], last_name=sname[1:6]).exists():
            #                     row[i] = people.get(first_name=sname[:1], last_name=sname[1:6]).id
            #                 # else:
            #                 #     row[i] = None
            #             elif index == 1:
            #                 row[i] = Category.objects.get(name=str(row[i]))
            #             elif index == 2:
            #                 row[i] = Area.objects.get(name=str(row[i]))
            #             elif index == 4:
            #                 row[i] = decimal.Decimal(row[i])
            #             elif index == 6:
            #                 if row[i]:
            #                     row[i] = row[5] + '--编辑备注:' + str(row[i])
            #                 else:
            #                     row[i] = row[5]
            #             else:
            #                 row[i] = str(row[i])
            #
            #
            #     # if not LandNum.objects.filter(area=row[2], num=row[3]):
            #     land = LandNum(area=row[2], num=row[3], category=row[1], fm=row[4], ps=row[6])
            #     land.save()
            #     Owner.objects.create(num=land, owner=str(row[0]), old_owner=row[7], ps=row[6])
            #     # owner.save()


        #
        #     print('OK')
        # return HttpResponse('OK')
                # account = row[10],
        # People.objects.bulk_create(list)