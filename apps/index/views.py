from datetime import datetime

from django.views import View
from django.shortcuts import render, redirect, reverse
from django.utils import dateformat, timezone
from django.utils.timezone import localdate

from django.conf import settings
from tools import draw
from . import tool


# Create your views here.


class IndexView(View):
    """
    首页
    """
    def get(self, request):
        """
        首页由4个东西组成：日付、条形图、表格、饼状图
        """
        # 日付
        paid_limit = tool.get_paid_limit()
        # 条形图
        bar = draw.draw_balance_bar(
            xaxis=[
                f"{date.strftime('%m月%d日')}({dateformat.DateFormat(date).D()[-1]})"
                for date in tool.get_current_x()
            ],
            yaxis=tool.get_current_y(),
            title='消费统计',
            markline=paid_limit
        ).dump_options()
        # 表格
        data, columns = tool.get_table_info()
        # 饼状图
        rest_out, budget = tool.get_index_pie()
        pie = draw.draw_usage_pie(
            payout=rest_out,
            budget=[('预算', budget)],
            title="本月结余"
        ).dump_options()
        return render(request, 'index/index.html', locals())


class DetailView(View):
    """
    详情页
    """
    def get(self, request):
        # 条形图
        month = request.session.get('month', '')
        date = month and datetime.strptime(month, '%Y-%m') or localdate()
        line = draw.draw_balance_line(
            xaxis=[
                f"{date.strftime('%m月%d日')}({dateformat.DateFormat(date).D()[-1]})"
                for date in tool.get_current_x(date)
            ],
            yaxis=tool.get_current_y(date),
            title=f"消费统计图",  # pie里面有需要的数据
        ).dump_options()
        #  table
        data, columns = tool.to_detail_table(date)
        # 月消费合计
        month_expend = "{:,}".format(tool.get_index_pie(date)[0][1][1])
        month = tool.get_sure_month_bill(date)
        return render(request, 'index/detail.html', locals())

    def post(self, request):
        month = request.POST.get('month')
        request.session['month'] = month
        return redirect(reverse('index:detail'))


class MonthlyPaymentsView(View):
    """
    月度收支 页
    """
    def get(self, request):
        # 条形图
        month = request.session.get('month', '')
        date = month and datetime.strptime(month, '%Y-%m') or localdate()
        inner, outside = tool.get_category_amount(date)
        line = draw.draw_category_pie(
            inner=inner[:settings.NUMBER_WEB_CATEGORY_PIE_EAT],
            outside=outside[:settings.NUMBER_WEB_CATEGORY_PIE_OTHER],
            inner_title=f'{date.year}年{date.month}饮食报表',
            outer_title=f'{date.year}年{date.month}其他报表'
        ).dump_options()
        # 表格
        data, columns = tool.get_table_info(date=date, month=True)
        # 月消费合计
        month_expend = "{:,}".format(tool.get_index_pie(date)[0][1][1])
        month = tool.get_sure_month_bill(date)
        return render(request, 'index/month.html', locals())

    def post(self, request):
        month = request.POST.get('month', '')
        request.session['month'] = month
        return redirect(reverse('index:month'))


class AnnualPaymentsView(View):
    """
    年度收支
    """
    def get(self, request):
        year = request.session.get('year', '')
        result = tool.annual(year)
        columns = result.get('columns')  # 表格标题
        data = result.get('status', [])  # 表格内容
        if data:
            annual_earnings = "{:,}".format(result.get('annual_earnings', 0))  # 年度收益
            annual_bar = draw.draw_balance_bar(
                xaxis=result.get('bar_x', []),
                yaxis=result.get('bar_y', []),
                difference=result.get('difference'),
                title=f'{year}年年度收支',
                markline=result.get('markline', 0)
            ).dump_options()  # 年度条形图
            annual_pie = draw.draw_category_pie(
                inner=result.get('eat_list')[:settings.NUMBER_WEB_CATEGORY_PIE_EAT],
                outside=result.get('other_list')[:settings.NUMBER_WEB_CATEGORY_PIE_OTHER],
            ).dump_options()
        return render(request, 'index/annual.html', locals())

    def post(self, request):
        year = request.POST.get('year')
        request.session['year'] = year
        return redirect(reverse('index:annual'))


class StatisticsView(View):
    """
    统计
    """
    def get(self, request):
        result = tool.statistics()
        total_assets = "{:,}".format(result['total_assets'])
        bar = draw.draw_balance_bar(
            xaxis=result['bar_x'],
            yaxis=result['bar_y'],
            difference=result['line_y'],
            title='总 收支统计'
        ).dump_options()
        return render(request, 'index/statistics.html', locals())


class SearchView(View):
    """
    详情
    """
    def get(self, request):
        year_search = request.session.get('year_search', '')
        select = request.session.get('select', '')
        word = request.session.get('word', '')
        result = tool.search(year_search, select, word)
        bar = draw.draw_balance_bar(
            xaxis=result['bar_x'],
            yaxis=result['bar_y'],
            title='',
        ).dump_options()
        total = result['total']
        data = result['table_data']
        columns = result['columns']
        return render(request, 'index/search.html', locals())

    def post(self, request):
        year_search = request.POST.get('year_search', '')
        select = request.POST.get('select')
        word = request.POST.get('word')
        request.session['year_search'] = year_search
        request.session['select'] = select
        request.session['word'] = word
        return redirect(reverse('index:search'))
