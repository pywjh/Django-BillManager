from django.shortcuts import render
from django.views import View
from index.models import BillModel, DayDetailModel

# Create your views here.


class IndexView(View):
    def get(self, request):
        return render(request, 'common/base.html')