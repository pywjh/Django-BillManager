# -*- coding: utf-8 -*-
# ========================================
# Author: wjh
# Date：2020/9/9
# FILE: tools
# ========================================
import datetime
import logging

from django.db.models import Sum
from django.utils.timezone import localdate
from django.utils.dateformat import DateFormat

from index.models import BillModel, DayDetailModel, SalaryDayModel


def get_objective_day(date) -> int:
    """获取准确的发薪日期"""
    objective = SalaryDayModel.objects.filter(
        start_date__lte=date,
    ).order_by('-start_date').first()
    if not objective:
        logging.warning('没有匹配到对应时间账单')
    else:
        return objective.day


def get_remaining_days(date=localdate()) -> int:
    """
    返回根据发薪日，来控制的截止时间（到发薪日还有多少天）
    """
    objective_day = get_objective_day(date)
    current_month_max_day = int(DateFormat(date).t())

    if date.day >= objective_day:
        return current_month_max_day - date.day + objective_day
    return objective_day - date.day


def get_sure_month_bill(date=None) -> BillModel:
    """
    获取准确的月份（由发薪日控制）
    :param date: date类型时间
    :return: 对应时间的总账
    """
    if not date:
        date = localdate()
        year = DateFormat(date).Y()
        month = DateFormat(date).n()
        day = DateFormat(date).j()

        objective_day = get_objective_day(date)

        if not objective_day:
            return BillModel.objects.first()

        month = month - 1 or 12 if day < objective_day else month
        return BillModel.objects.get(date=f"{year}-{month}-{objective_day}")

    else:
        bill_id = BillModel.objects.filter(date__gte=date).order_by('date').first()
        if not bill_id:
            return BillModel.objects.first()
        return bill_id


def get_paid_limit() -> float:
    """
    获取日付上线金额
    """
    bill_id = get_sure_month_bill()
    # 本月消费
    total_cost = sum(map(lambda d: d.get('amount', 0), bill_id.day_detail.all().values('amount')))
    # 本月剩余天数
    remaining_days = get_remaining_days()
    return round((bill_id.budget - total_cost) / remaining_days, 2)


def get_current_x(date=None) -> list:
    """
    获取统计图的x轴
    """
    bill_id = get_sure_month_bill(date)
    x_date = sorted(
        list(set([date.date for date in bill_id.day_detail.only('date')])),
        key=lambda m: datetime.datetime(m.year, m.month, m.day),
    )
    return x_date


def get_current_y(date=None) -> list:
    """
    获取统计图的y轴
    return: [('title', [1,2,3,4]), ('title', [1,2,3,4])]
    """
    y_eat = [('饮食', [])]
    y_other = [('其他', [])]
    y_all = [('全部', [])]
    x_date = get_current_x(date)
    for date in x_date:
        eat_amount = DayDetailModel.objects.filter(date=date, type='eat').aggregate(sum=Sum('amount'))['sum'] or 0
        other_amount = DayDetailModel.objects.filter(date=date, type='other').aggregate(sum=Sum('amount'))['sum'] or 0
        y_eat[0][1].append(round(eat_amount, 2))
        y_other[0][1].append(round(other_amount, 2))
        y_all[0][1].append(round((eat_amount + other_amount), 2))
    return y_eat + y_other + y_all


def get_table_info(date=None, month=None) -> tuple:
    """
    首页小表格
    """
    bill_id = get_sure_month_bill(date)
    columns = [
        {
            "field": "name",  # which is the field's name of data key
            "title": "名称",  # display as the table header's name
            "sortable": 'false',
        },
        {
            "field": "balance",
            "title": "金额 (元)",
            "sortable": 'false',
        },
    ]

    payment = round(bill_id.day_detail.aggregate(sum=Sum('amount'))['sum'] or 0, 2)

    status = [
        {'name': '本月收入', 'balance': bill_id.salary},
        {'name': '本月支出', 'balance': payment},
        {'name': '本月房租', 'balance': bill_id.rent},
        {'name': '本月预算', 'balance': bill_id.budget},
        {'name': '预算结余', 'balance': round(bill_id.budget - payment, 2)},
        {'name': '日付上限', 'balance': get_paid_limit()},
        {'name': '月储金额', 'balance': bill_id.save_amount},
        {'name': '本月结余', 'balance': round((bill_id.salary - payment - bill_id.rent), 2)},
    ]
    if month:
        status.insert(
            1, {'name': '饮食支出', 'balance': round(bill_id.day_detail.filter(type='eat').aggregate(sum=Sum('amount'))['sum'] or 0, 2)}
        )
        status.insert(
            2, {'name': '其他支出', 'balance': round(bill_id.day_detail.filter(type='other').aggregate(sum=Sum('amount'))['sum'] or 0, 2)}
        )
    return status, columns


def get_index_pie(date=None) -> tuple:
    """
    网站首页饼状图
    :return:
        data -> list [(title1, num1), (title2, num2)]
    """
    bill_id = get_sure_month_bill(date)
    payment = round(bill_id.day_detail.aggregate(sum=Sum('amount'))['sum'] or 0, 2)
    surplus = round(bill_id.budget - payment, 2)
    if surplus < 0:
        surplus = 0

    rest_out = [('结余', surplus), ('支出', payment)]
    return rest_out, bill_id.budget


def to_detail_table(date):
    """
    详情页的详细消费信息
    """
    bill_id = get_sure_month_bill(date)
    bills = []
    columns = [
        {
            "field": "date",  # which is the field's name of data key
            "title": "日期",  # display as the table header's name
            "sortable": 'false',
        },
        {
            "field": "name",
            "title": "用途",
            "sortable": 'false',
        },
        {
            "field": "amount",
            "title": "金额（元）",
            "sortable": 'false',
        },
        {
            "field": "note",
            "title": "备注",
            "sortable": 'false',
        },
    ]
    detail_data = bill_id.day_detail.all().order_by('date')
    for data in detail_data:
        bills.append({
            'date': DateFormat(data.date).c(),
            'name': data.name,
            'amount': data.amount,
            'note': data.note,
            'type': data.type,
        })
    return bills, columns


def get_category_amount(date):
    """
    饼状统计图
    """
    bill_id = get_sure_month_bill(date)
    eat_list = []
    other_list = []
    eat_name = set([i['name'] for i in bill_id.day_detail.filter(type='eat').values('name')])
    other_name = set([i['name'] for i in bill_id.day_detail.filter(type='other').values('name')])
    for name in eat_name:
        eat_list.append(
            (name,
                sum(map(
                        lambda d: d.get('amount', 0),
                        bill_id.day_detail.filter(name=name, type='eat').values('amount'))
                )))
    for name in other_name:
        other_list.append(
            (name,
                sum(map(
                        lambda d: d.get('amount', 0),
                        bill_id.day_detail.filter(name=name, type='other').values('amount'))
                )))
    eat_list.sort(key=lambda t: t[1], reverse=True)
    other_list.sort(key=lambda t: t[1], reverse=True)
    return eat_list, other_list