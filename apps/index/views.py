from django.shortcuts import render, redirect
from django.views import View
from index.models import BillModel, DayDetailModel

# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'common/base.html')


class UpdateView(View):
    def get(self, request):
        return render(request, 'index/update.html')

    def post(self):
        return redirect('index/update.html')