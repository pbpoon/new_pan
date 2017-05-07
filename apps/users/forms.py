# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/5/6 15:27'


from django import forms


class LoginForm(forms.Form):
    user_name = forms.CharField(label='账号', required=True, min_length=5)
    password = forms.CharField(widget=forms.PasswordInput)
