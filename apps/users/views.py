from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import FormView, View
from django.contrib.auth import  authenticate, login
from django.contrib.auth.backends import ModelBackend

from .models import UserProfile
from .forms import LoginForm


# class LoginView(View):
#     form_class = LoginForm
#     template_name = 'users/login.html'
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#         user = authenticate(username=data.get('user_name'), password=data.get('password'))
#         if user is not None:
#             login(request, user=user)
#             return HttpResponseRedirect('index.html')

class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data.get('user_name'), password=data.get('password'))
            if user is not None:
                login(request, user)
                return render(request, 'login.html', locals())

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', locals())

