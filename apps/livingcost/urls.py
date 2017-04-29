from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^mark/(?P<pk>\d+)/$', views.CenterWaterMarkDetailView.as_view(), name='mark_detail'),
    url(r'^mark/$', views.CenterWaterMarkListView.as_view(), name='mark'),
    url(r'^(?P<pk>\d+)/$', views.WaterrateDetailView.as_view(), name='detail'),
    url(r'^$', views.WaterRateListView.as_view(), name='index'),
]
