from django.urls import path
from . import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

app_name='accounts'
urlpatterns = [
    path('register', views.register, name ='register'),
    path('login', views.login, name ='login'),
    path('logout', views.logout, name ='logout'),
    path('adminregister', views.adminregister, name ='adminregister'),
    path('adminlogin', views.adminlogin, name ='adminlogin'),
    path('changepass', views.changepass, name ='changepass'),
    path('stuchangepass', views.stuchangepass, name ='stuchangepass'),
    path('admin', views.admin, name='admin'),
    path('admina', views.form, name='admina'),
    path('student', views.chart, name='student'),
    path('home', views.home, name='home'),
    #path('form', views.form, name='form'),
    path('index', views.simple_upload, name ='index'),
   
]
# -*- coding: utf-8 -*-
urlpatterns += staticfiles_urlpatterns()