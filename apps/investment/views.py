from django.shortcuts import render
from django.http import JsonResponse

from . import tool
# Create your views here.


def investment(request):
    return render(request, 'investment/investment.html')


def earnings(request):
    try:
        start = request.GET.get('start')
        end = request.GET.get('end')
        if start and end:
            result = tool.earnings(start, end)
            return JsonResponse(result)
        raise Exception('错误的请求参数')
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
        start = request.GET.get('start')
        end = request.GET.get('end')

        can_action = ['LAST_YEAR', 'YEAR', 'LAST_MONTH', 'MONTH', 'LAST_WEEK', 'WEEK', 'ALL']

        if action and action in can_action:
            result = tool.change_date(action, start, end)
            return JsonResponse(result)
        raise Exception('错误的请求参数`action`')
    except Exception as e:
        result = {
            'code': 500,
            'message': e,
        }
        return JsonResponse(result)
