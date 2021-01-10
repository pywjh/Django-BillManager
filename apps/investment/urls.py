# -*- coding: utf-8 -*-
# ========================================
# Author: wjh
# Date：2021/1/9
# FILE: urls
# ========================================
from django.urls import path
from . import views

app_name = 'investment'

urlpatterns = [
    path('investment', views.investment, name='investment'),
    path('earnings', views.earnings, name='earnings'),
    path('changeDate', views.change_date, name='change_date'),
]
