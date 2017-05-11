from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import UserProfile
from .forms import LoginForm, RegisterForm


class CustomAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(bind_people__first_name=username[:1],
                                                              bind_people__last_name=username[1:]))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

#
# class LoginView(View):
#     template_name = 'login.html'
#     def post(self, request):
#
#         form = LoginForm(request.POST)
#         data = {}
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd.get('user_name'), password=cd.get('password'))
#             if user is not None:
#                 login(request, user)
#                 # return HttpResponseRedirect(reverse('article:index'))
#                 return HttpResponseRedirect(request.POST['next'])
#             msg = '用户名或者密码错误!'
#             return render(request, self.template_name, locals())
#         else:
#             return render(request, self.template_name, locals())
#
#     def get(self, request):
#         form = LoginForm()
#         return render(request, 'login.html', locals())


# class LogoutView(View):
#
#     def get(self, request):
#         logout(request)
#         return HttpResponseRedirect(reverse('article:index'))


class RegisterView(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            '''
            创建用户并绑定村民信息
            '''
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            bind_people = form.cleaned_data['people_name']

            new_user = UserProfile.objects.create(username=username, bind_people=bind_people)
            new_user.set_password(password)
            new_user.save()
            '''如注册资料有电话号码,保存电话号码到people的资料'''
            telphone = form.cleaned_data['telphone']
            if telphone:
                bind_people.phone_num = telphone
                bind_people.save()
            return render(request, 'login.html', {'msg':'注册成功!', 'form': form})
        return render(request, 'register.html', {'form': form})

    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})