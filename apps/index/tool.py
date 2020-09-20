# -*- coding: utf-8 -*-
# ========================================
# Author: wjh
# Date：2020/9/9
# FILE: tools
# ========================================
import datetime
import logging

from django.db.models import Count, Sum, Avg, Q
from django.utils.timezone import localdate
from django.utils.dateformat import DateFormat
from django.conf import settings

from index.models import BillModel, DayDetailModel, SalaryDayModel

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


def to_detail_table(date) -> tuple:
    """
    详情页的详细消费信息
    """
    bill_id = get_sure_month_bill(date)
    bills = []
    detail_data = bill_id.day_detail.all().order_by('date')
    for data in detail_data:
        bills.append({
            'date': DateFormat(data.date).c(),
            'name': data.name or '',
            'amount': data.amount or 0,
            'note': data.note or '',
            'type': data.type,
        })
    return bills, columns


def get_category_amount(date) -> tuple:
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


def annual(year) -> dict:
    """
    年度收支
    """
    if not year:
        year = localdate().year

    bills = BillModel.objects.filter(date__year=year).order_by('date')

    if not bills:
        return {}

    # 表格
    total_salary = round(bills.aggregate(total=Sum('salary')).get('total', 0), 2)
    total_eat = round(sum([bill.day_detail.filter(type='eat').aggregate(total=Sum('amount'))['total'] for bill in bills]), 2)
    total_other = round(sum([bill.day_detail.filter(type='other').aggregate(total=Sum('amount'))['total'] for bill in bills]), 2)
    total_rent = round(bills.aggregate(total=Sum('rent')).get('total', 0), 2)
    total_cost = round((total_eat + total_other), 2)
    total_cost_all = round((total_rent + total_cost), 2)
    annual_earnings = round((total_salary - total_cost_all), 2)

    # 条形图
    bar_x = [date.strftime('%Y年%m月') for date in bills.values_list('date', flat=True)]
    bar_expend_y = [('支出', [round(bill.day_detail.aggregate(total=Sum('amount'))['total'], 2) for bill in bills])]
    bar_income_y = [('收入', [bill.salary for bill in bills])]

    # 辅助线
    mark_line = round(bills.aggregate(budget_avg=Avg('budget'))['budget_avg'], 2)

    # 月收支差值
    difference = [
        '结余',
        [
            round((income - expend), 2)
            for income, expend in zip(bar_income_y[0][1], bar_expend_y[0][1])
        ]
    ]
    # 饼状图
    eat_list = list(
                DayDetailModel.objects.filter(
                    bill_id__date__year=year,
                    type='eat'
                ).values('name').annotate(sum=Sum('amount')).order_by('-sum').values_list('name', 'sum'))
    other_list = list(
                DayDetailModel.objects.filter(
                    bill_id__date__year=year,
                    type='other'
                ).values('name').annotate(sum=Sum('amount')).order_by('-sum').values_list('name', 'sum'))

    result = {
        'total_salary': total_salary,  # 年度总工资
        'total_eat': total_eat,  # 年度总饮食消费
        'total_other': total_other,  # 年度总其他消费
        'total_rent': total_rent,  # 年度总房租消费
        'total_cost': total_cost,  # 年度总吃穿用消费
        'total_cost_all': total_cost_all,  # 年度所有消费
        'annual_earnings': annual_earnings,  # 年度总盈亏
        'columns': [
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
        ],  # 表格标题
        'status': [
            {'name': f'{year}年收入金额', 'balance': "{:,}".format(total_salary)},
            {'name': f'{year}年饮食金额', 'balance': "{:,}".format(total_eat)},
            {'name': f'{year}年其他金额', 'balance': "{:,}".format(total_other)},
            {'name': f'{year}年吃穿金额', 'balance': "{:,}".format(total_cost)},
            {'name': f'{year}年租金金额', 'balance': "{:,}".format(total_rent)},
            {'name': f'{year}年支出金额', 'balance': "{:,}".format(total_cost_all)},
            {'name': f'{year}年盈亏金额', 'balance': "{:,}".format(annual_earnings)},
        ],  # 表格内容
        'bar_x': bar_x,  # 条形图x轴
        'bar_y': bar_expend_y+bar_income_y,  # 条形图y轴
        'markline': mark_line,  # 年度统计图辅助线
        'difference': difference,  # 月剩余
        'eat_list': list(map(lambda t: (t[0], round(t[1], 2)), eat_list)),  # 年度饼状图eat，内圈
        'other_list': list(map(lambda t: (t[0], round(t[1], 2)), other_list)),  # 年度饼状图other，外圈
    }
    return result


def statistics():
    # 总收入
    total_income = round(BillModel.objects.values('salary').aggregate(total=Sum('salary')).get('total', 0), 2)
    # 总房租
    total_rent = round(BillModel.objects.values('rent').aggregate(total=Sum('rent')).get('total', 0), 2)
    # 总消费
    total_expend = round(DayDetailModel.objects.values('amount').aggregate(total=Sum('amount')).get('total', 0), 2)
    # 剩余资产
    total_assets = round(total_income - total_expend - total_rent, 2)

    # 条形图x轴
    bar_x = list(BillModel.objects.values('date__year').annotate(c=Count('date__year')).order_by('date__year').values_list('date__year', flat=True))
    # 条形图y轴1
    bar_income_y = (
        '收入',
        [
            round(BillModel.objects.filter(date__year=year).values('salary').aggregate(total=Sum('salary')).get('total', 0), 2)
            for year in bar_x
        ]
    )
    # 条形图y轴2
    bar_expend_y = (
        '支出',
        [
            round(
                sum(  # 房租和总消费之和
                    [
                        BillModel.objects.filter(
                            date__year=year
                        ).values('rent').aggregate(total=Sum('rent')).get('total', 0),
                        DayDetailModel.objects.filter(
                            date__year=year
                        ).values('amount').aggregate(total=Sum('amount')).get('total', 0)
                    ]
                ),
                2
            )
            for year in bar_x
        ]
    )
    # 折线图
    line_y = ('结余', [round(income - expend, 2) for income, expend in zip(bar_income_y[1], bar_expend_y[1])])
    return {
        'total_assets': total_assets,
        'bar_x': list(map(str, bar_x)),  # 卡了我好久，不是字符串line试图显示不出数据来,
        'bar_y': list([bar_expend_y, bar_income_y]),
        'line_y': line_y,
    }


def search(year_search, select, word):
    """
    搜索功能 
    """
    word = word.strip()
    result = DayDetailModel.objects.filter(
        Q(name__contains=word) | Q(note__contains=word)
    ).order_by('date')

    if select == 'year':
        year = year_search or localdate().year
        result = result.filter(date__year=year)

    table = result.values_list('date', 'name', 'amount', 'type', 'note')
    result = result.values('date').annotate(s=Sum('amount')).order_by('date').values_list('date', 's')

    if len(result) > settings.NUMBER_MAX_STATISTICS:
        result = result[:settings.NUMBER_MAX_STATISTICS]

    bar_x = list(
        map(
            lambda t: f"""{t[0]}({DateFormat(t[0]).D()})""",
            result
        )
    )
    bar_y = [(word, list(map(lambda t: t[1], result)))]

    total = round(sum(bar_y[0][1]), 2)

    table_data = [
        {
            'date': DateFormat(data[0]).c(),
            'name': data[1] or '',
            'amount': data[2] or 0,
            'type': data[3],
            'note': data[4] or '',
        }
        for data in table
    ]
    table_columns = columns[::]
    table_columns.append(
        {
            "field": "type",  # which is the field's name of data key
            "title": "类别",  # display as the table header's name
            "sortable": 'false',
        }
    )

    return {
        'bar_x': bar_x,
        'bar_y': bar_y,
        'total': total,
        'columns': table_columns,
        'table_data': table_data,
    }
