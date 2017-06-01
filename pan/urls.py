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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static
from markdownx import urls as markdownx

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', RedirectView.as_view(pattern_name='article:index'), name='index'),
    url(r'^no_perm/', TemplateView.as_view(template_name='no_prem.html'),name='no_perm'),
    url(r'^user/', include('users.urls', namespace='user')),
    url(r'^document/', include('document.urls', namespace='document')),
    url(r'^', include('article.urls', namespace='article')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^asset/', include('asset.urls', namespace='asset')),
    url(r'^livingcost/', include('livingcost.urls', namespace='livingcost')),
    url(r'^money/', include('money.urls', namespace='money')),
]
urlpatterns += [
    url(r'^markdownx/', include(markdownx))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)