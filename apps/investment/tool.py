# -*- coding: utf-8 -*-
# ========================================
# Author: wjh
# Date：2021/1/9
# FILE: tool
# ========================================
import calendar
import datetime
from dateutil.relativedelta import relativedelta

from .models import InvestmentModel
from index.models import DayDetailModel

from django.utils import formats, timezone
from django.db.models import Sum

from tools.draw import draw_balance_line


def get_total_earnings(earnings: list) -> list:
    """
    将每日起伏的数据做成汇总列表
    >>> earnings = [1, 2, 3, 4, 5]
    >>> return [1, 3, 6, 10, 15]
    """
    total_earnings_list = []
    tool_num = 0
    for earning in earnings:
        tool_num += earning
        total_earnings_list.append(tool_num)
    return list(map(lambda f: round(f, 3), total_earnings_list))


def earnings(start, end):
    objects: InvestmentModel = InvestmentModel.objects.filter(
        date__gte=start,
        date__lte=end,
    ).order_by("date")
    date = [formats.date_format(date) for date in objects.values_list("date", flat=True)]
    earnings = list(objects.values_list("earnings", flat=True))
    total_earnings: list = get_total_earnings(earnings)
    option = draw_balance_line(
        xaxis=date,
        yaxis=[("收益", earnings), ("总计", total_earnings)],
        title="理财收益"
    ).dump_options()

    total_amount = DayDetailModel.objects.filter(
        date__gte=start,
        date__lte=end,
    ).aggregate(sum=Sum("amount")).get('sum', 0)
    total_earnings = total_earnings and total_earnings[-1] or 0

    result = {
        "code": 200,
        "option": option,
        "total_amount": round(total_amount, 2),
        "total_earnings": round(total_earnings, 2)
    }
    return result


def change_date(action):
    today = timezone.localdate()
    year = today.year
    month = today.month
    end_day = calendar.monthrange(year, month)[-1]
    weekday = today.weekday()
    if action == 'YEAR':
        start = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 30)
    elif action == 'MONTH':
        start = datetime.date(year, month, 1)
        end = datetime.date(year, month, end_day)
    elif action == 'LAST_WEEK':
        start = today - relativedelta(days=weekday) - relativedelta(days=7)
        end = today + relativedelta(days=7 - weekday) - relativedelta(days=7)
    elif action == 'ALL':
        start = InvestmentModel.objects.order_by('date').first().date
        end = InvestmentModel.objects.order_by('date').last().date
    else:  # WEEKEND
        start = today - relativedelta(days=weekday)
        end = today + relativedelta(days=7 - weekday)
    result = {
        'code': 200,
        'start': start,
        'end': end,
    }
    return result
