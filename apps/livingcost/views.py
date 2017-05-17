from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import CenterWater, WaterNum, WaterRate


class WaterRateListView(ListView):
    context_object_name = 'num_list'
    queryset = WaterNum.objects.filter(is_del=False)
    template_name = 'livingcost/index.html'


class WaterrateDetailView(DetailView):
    context_object_name = 'num'
    model = WaterNum
    template_name = 'livingcost/detail.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(WaterrateDetailView, self).get_context_data(**kwargs)
        context['rate'] = self.object.rate.all()
        return context


class CenterWaterMarkListView(ListView):
    context_object_name = 'mark_d_list'
    model = CenterWater
    template_name = 'livingcost/mark_d_list.html'


class CenterWaterMarkDetailView(DetailView):
    context_object_name = 'mark_d'
    model = CenterWater
    template_name = 'livingcost/mark_d_detail.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(CenterWaterMarkDetailView, self).get_context_data(**kwargs)
        context['num_list'] = self.object.account_rate.all()
        return context


