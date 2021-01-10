from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.http import JsonResponse
from .models import InvestmentModel
from django.utils import formats, timezone
from tools.draw import draw_balance_line

from . import tool
# Create your views here.


def investment(request):
    return render(request, 'investment/investment.html')


def earnings(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')

        objects: InvestmentModel = InvestmentModel.objects.filter(
            date__gte=start,
            date__lte=end,
        ).order_by("date")
        date = [formats.date_format(date) for date in objects.values_list("date", flat=True)]
        earnings = list(objects.values_list("earnings", flat=True))
        total_earnings: list = tool.get_total_earnings(earnings)
        option = draw_balance_line(
            xaxis=date,
            yaxis=[("收益", earnings), ("总计", total_earnings)],
            title="理财收益"
        ).dump_options()
        result = {
            "code": 200,
            "option": option
        }
        return JsonResponse(result)
    except Exception as e:
        result = {
            "code": 500,
            "option": e
        }
        return JsonResponse(result)


def change_date(request):
    """通过界面选择`本年`、`本月`、`本周`返回对应的开始、结束时间"""
    try:
        action = request.GET.get('type')

        if action and action in ('YEAR', 'MONTH', 'WEEKEND'):
            end = timezone.localdate()
            if action == 'YEAR':
                start = end + relativedelta(years=-1)
            elif action == 'MONTH':
                start = end + relativedelta(months=-1)
            else:  # WEEKEND
                start = end + relativedelta(weeks=-1)
            result = {
                'code': 200,
                'start': start,
                'end': end,
            }
            return JsonResponse(result)
    except Exception as e:
        result = {
            'code': 500,
            'message': e,
        }
        return JsonResponse(result)
