"""pan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^add/', views.FileUploadView.as_view(), name='addfile'),
    url(r'^people$', views.PeopleListView.as_view(), name='people_list'),
    url(r'^people/(?P<pk>\d+)/$', views.PeopleView.as_view(), name='people'),
    url(r'^(?P<name>\w+)/$', views.AccountDetailView.as_view(), name='detail'),
    url(r'^$', views.AccountListView.as_view(), name='index'),
]
