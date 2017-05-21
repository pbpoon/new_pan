from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import MoneyAccount, Tag, Document
import re


class MoneyListView(LoginRequiredMixin, ListView):
    template_name = 'money/index.html'
    context_object_name = 'money_list'
    '''
    把最后的 count 条数据调出来，然后在template再用 dictsort:"num" 重新按顺序来排序列出
    '''
    count = 3
    qs1 = MoneyAccount.objects.filter(type='b').order_by('-num')[:count]
    qs2 = MoneyAccount.objects.filter(type='c').order_by('-num')[:count]
    qs = [item for item in qs1] + [item for item in qs2]
    queryset = qs


class MoneyDetailListView(LoginRequiredMixin, ListView):
    template_name = 'money/detail.html'
    model = MoneyAccount

    def get_queryset(self):
        qs = super(MoneyDetailListView, self).get_queryset()
        type = self.request.GET.get('type')
        tag = self.request.GET.get('tag')
        status = self.request.GET.get('status')
        list = [type, tag, status]
        list2 = ['type', 'tag', 'status']
        kwargs = {}
        for k, v in zip(list2, list):
            if k == 'tag':
                if v:
                    kwargs['{}__id'.format(k)] = v
            if v:
                kwargs[k] = v
        if kwargs:
            qs = qs.filter(**kwargs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(MoneyDetailListView, self).get_context_data(**kwargs)
        '''
        full_path:把筛选的条件返回下次多个条件组合
        tag:把所有的标签展示到筛选
        status:把筛选的status状态返回高亮
        type:同上
        tag_id:同上
        title:方便把title更改
        '''

        string = r'.*?detail\?(.*)'
        match_path = re.match(string, self.request.get_full_path())
        full_path = match_path.group(1) if match_path else ''
        context['full_path'] = full_path
        context['tag'] = Tag.objects.all()
        context['tag_id'] = int(self.request.GET.get('tag')) if self.request.GET.get('tag') else None
        context['status'] = self.request.GET.get('status')
        context['type'] = self.request.GET.get('type')
        context['title'] = self.object_list.filter(type=context['type']).first()

        return context


class ItemDetailView(DetailView):
    template_name = 'money/item_detail.html'
    model = MoneyAccount
    context_object_name = 'money'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['doc'] = self.object.doc.all()

        return context

#
# class FileUploadView(FormView):
#     from account.forms import FileForm
#
#     template_name = 'account/file.html'
#     form_class = FileForm
#
#     def form_valid(self, form):
#         f = form.files.get('file')
#         if f:
#             import xlrd
#             from xlrd.xldate import xldate_as_datetime
#             from decimal import Decimal
#             import re
#
#             data = xlrd.open_workbook(file_contents=f.read())
#             # table = data.sheet_by_name(by_name)
#             table = data.sheets()[0]
#             nrows = table.nrows  # 总行数
#             colnames = table.row_values(0)  # 表头列名称数据
#             print(colnames)
#             list = []
#             # accounts = [MoneyAccount(name=str(x)) for x in set(table.col_values(10, 1))]
#             # print(accounts)
#             # Account.objects.bulk_create(accounts)
#             for rownum in range(1, nrows):
#                 row = table.row_values(rownum)
#                 for index, i in enumerate(range(len(colnames))):
#                     if row:
#                         if index == 0:
#                             row[i] = xldate_as_datetime(row[i], 0)
#                         elif index == 2:
#                             row[i] = Decimal(row[i]).quantize(Decimal('0.00'))
#                         else:
#                             row[i] = str(row[i])
#                 print(row)
#
#                 list.append(MoneyAccount(date=row[0], detail=row[1], amount=row[2], ps=row[3], type=row[4],
#                                          status=row[5],num=row[6], operator=self.request.user))
#         #         print(list)
#         #         # account = row[10],
#         MoneyAccount.objects.bulk_create(list)
#         return HttpResponse('OK')
#         # form.save()
#         # return redirect(order)
