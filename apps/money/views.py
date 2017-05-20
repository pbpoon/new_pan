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
        qs = qs.filter(**kwargs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(MoneyDetailListView, self).get_context_data(**kwargs)
        context['type'] = self.object_list.first()
        string = r'.*?detail\?(.*)'
        match_path = re.match(string, self.request.get_full_path())
        full_path = match_path.group(1)
        context['full_path'] = full_path
        return context