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
    path('index', views.IndexView.as_view(), name='index'),
    path('detail', views.DetailView.as_view(), name='detail'),
    path('month', views.MonthlyPaymentsView.as_view(), name='month'),
    path('annual', views.AnnualPaymentsView.as_view(), name='annual'),
    path('statistics', views.StatisticsView.as_view(), name='statistics'),
    path('search', views.SearchView.as_view(), name='search'),
]