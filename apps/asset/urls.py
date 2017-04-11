from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/', views.FileUploadView.as_view(), name='addfile'),
    url(r'^owner/(?P<owner_id>\d+)/$', views.owner_land_listview, name='owner'),
    # url(r'^(?P<name>\w+)/$', views.AccountDetailView.as_view(), name='detail'),
    url(r'^$', views.OwnerListView.as_view(), name='index'),

]
