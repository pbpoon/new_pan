from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend

from .models import UserProfile
from .forms import LoginForm, RegisterForm


class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data.get('user_name'), password=data.get('password'))
            if user is not None:
                login(request, user)
                # return HttpResponseRedirect(reverse('article:index'))
                return HttpResponseRedirect(request.POST['next'])
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


class RegisterView(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            '''
            创建用户并绑定村民信息
            '''
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            bind_people = form.cleaned_data['card_num']
            new_user = UserProfile.objects.create(username=username, bind_people=bind_people)
            new_user.set_password(password)
            new_user.save()
            return render(request, 'login.html', {'msg':'注册成功!','form': form})
        return render(request, 'register.html', {'form': form})

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})