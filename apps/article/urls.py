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
    url(r'^like/', views.LikeView.as_view(), name='article_like'),
    url(r'^comment/(?P<article_id>\d+)', views.CommentView.as_view(), name='comment'),
    url(r'^article/tag/(?P<tag_id>\d+)/$', views.TagListView.as_view(), name='tag'),
    url(r'^article/(?P<pk>\d+)/$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'', views.ArticleListView.as_view(), name='index'),
]
