from django.shortcuts import render
from django.views.generic import ListView, DetailView
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