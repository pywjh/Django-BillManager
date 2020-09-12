# -*- coding: utf-8 -*-
# ========================================
# Author: wjh
# Date：2020/9/3
# FILE: urls
# ========================================

from django.urls import path, include
from . import views

app_name = 'index'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('update', views.UpdateView.as_view(), name='update')
]