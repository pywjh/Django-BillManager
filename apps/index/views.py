from django.views import View
from django.shortcuts import render, redirect
from django.utils import dateformat, timezone

from .models import BillModel, DayDetailModel
from tools import tool, draw

# Create your views here.


class IndexView(View):
    def get(self, request):
        """
        首页由4个东西组成：日付、条形图、表格、饼状图
        """
        # 日付
        paid_limit = tool.get_paid_limit()
        # 条形图
        bar = draw.draw_balance_bar(
            xaxis=[
                f"{date.strftime('%m月%d日')}({dateformat.DateFormat(date).D()[-1]})" for date in tool.get_current_x()
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


class UpdateView(View):
    def get(self, request):
        today = dateformat.DateFormat(timezone.localdate()).c()
        return render(request, 'index/update.html', locals())

    def post(self):
        return redirect('index/update.html')
