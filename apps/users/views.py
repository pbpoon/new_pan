from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import  View
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.backends import ModelBackend


from .forms import LoginForm


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data.get('user_name'), password=data.get('password'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('article:index'))
            msg = '用户名或者密码错误!'
            return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', locals())


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('article:index'))
