from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import MoneyAccount, Tag, Document
import re

from chartit import DataPool, Chart


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
        year = self.request.GET.get('year')
        list = [type, tag, status, year]
        list2 = ['type', 'tag', 'status', 'date']
        kwargs = {}
        for k, v in zip(list2, list):
            if k == 'tag':
                if v:
                    kwargs['{}__id'.format(k)] = v
            elif k == 'date':
                if v:
                    kwargs['{}__year'.format(k)] = int(v)
            elif v:
                kwargs[k] = v
        if kwargs:
            qs = qs.filter(**kwargs)

        return qs

    def get_context_data(self, **kwargs):
        '''
        full_path:把筛选的条件返回下次多个条件组合
        tag:把所有的标签展示到筛选
        status:把筛选的status状态返回高亮
        type:同上
        tag_id:同上
        title:方便把title更改
        '''
        kwargs['tag'] = Tag.objects.all()
        kwargs['tag_id'] = self.request.GET.get('tag', '')
        kwargs['status'] = self.request.GET.get('status', '')
        kwargs['year'] = self.request.GET.get('year', '')
        kwargs['type'] = self.request.GET.get('type', '')
        kwargs['title'] = self.object_list.filter(type=kwargs['type']).first()
        kwargs['date_label'] = [i.year for i in MoneyAccount.objects.dates('date', 'year')]
        kwargs['b_balance'] = MoneyAccount.objects.filter(type='b').last()
        kwargs['c_balance'] = MoneyAccount.objects.filter(type='c').last()
        '''
        图表数据设置
        '''
        money_list = \
            DataPool(
                series=
                [{'options': {
                    'source': self.object_list.filter(status=1)},
                    'terms': [
                        'date',
                        'amount',
                        'detail']},
                    {'options': {
                        'source': self.object_list.filter(status=-1).extra(
                            select={'absamount': 'abs(amount)'}).order_by('absamount')},
                        'terms': [{'date2': 'date',
                                   'amount2': 'absamount',
                                   'detail2': 'detail'}
                                  ]}
                ])

        # Step 2: Create the Chart object
        '''
        圖表設置
        https://www.hcharts.cn/docs/pie-chart
        '''
        cht = Chart(
            datasource=money_list,
            series_options=
            [{'options': {
                'type': 'pie',# 图表类型
                'stacking': False,
                'size': '70%',#图表大小
                'dataLabels': {'enabled': True},#标签显示
                'center': ['20%', '50%'],#中心位置
            },
                'terms': {
                    'detail': [
                        'amount']
                }},
                {'options': {
                    'type': 'pie',
                    'stacking': False,
                    'size': '70%',
                    'center': ['80%', '50%'],
                },
                    'terms': {
                        'detail2': [
                            'amount2']
                    }},
            ],
            chart_options=
            {'title': {
                'text': '收支情况饼图'},
                'subtitle': {
                    'text': '左图为收入,右图为支出'
                },
                'xAxis': {
                    'title': {
                        'text': 'amount'}},
                'yAxis': {
                    'title': {
                        'text': 'amount2'}},
            }
        )

        kwargs['money_list'] = cht

        return super(MoneyDetailListView, self).get_context_data(**kwargs)


class ItemDetailView(LoginRequiredMixin, DetailView):
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
