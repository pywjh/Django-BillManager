from datetime import datetime

from django.views import View
from django.shortcuts import render, redirect, reverse
from django.utils import dateformat, timezone

from django.conf import settings
from tools import tool, draw

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
        date = month and datetime.strptime(month, '%Y-%m') or ''
        line = draw.draw_balance_line(
            xaxis=[
                f"{date.strftime('%m月%d日')}({dateformat.DateFormat(date).D()[-1]})"
                for date in tool.get_current_x(date)
            ],
            yaxis=tool.get_current_y(date),
            title=f"{tool.get_sure_month_bill(date)}总消费:{tool.get_index_pie(date)[0][1][1]}",  # pie里面有需要的数据
        ).dump_options()
        #  table
        data, columns = tool.to_detail_table(date)
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
        date = month and datetime.strptime(month, '%Y-%m') or ''
        inner, outside = tool.get_category_amount(date)
        line = draw.draw_category_pie(
            inner=inner[:settings.NUMBER_WEB_CATEGORY_PIE_EAT],
            outside=outside[:settings.NUMBER_WEB_CATEGORY_PIE_OTHER],
            inner_title=f'{date.year}年{date.month}饮食报表',
            outer_title=f'{date.year}年{date.month}其他报表'
        ).dump_options()
        # 表格
        data, columns = tool.get_table_info(month=True)
        return render(request, 'index/month.html', locals())

    def post(self, request):
        month = request.POST.get('month', '')
        request.session['month'] = month
        return redirect(reverse('index:month'))


class UpdateView(View):
    def get(self, request):
        today = dateformat.DateFormat(timezone.localdate()).c()
        return render(request, 'index/update.html', locals())

    def post(self):
        return redirect('index/update.html')
