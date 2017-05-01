from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/', views.FileUploadView.as_view(), name='addfile'),
    url(r'^landnum/(?P<pk>\d+)/$', views.LandNumDetaiView.as_view(), name='landnum'),
    url(r'^owner/(?P<pk>\d+)/$', views.PeopleLandListView.as_view(), name='owner'),
    url(r'^area/(?P<pk>\d+)/$', views.AreaDetailView.as_view(), name='area_detail'),
    url(r'^area/$', views.AreaListView.as_view(), name='area'),
    url(r'^$', views.OwnerListView.as_view(), name='index'),
]
