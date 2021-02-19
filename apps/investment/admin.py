from django.contrib import admin
from .models import InvestmentModel

# Register your models here.


@admin.register(InvestmentModel)
class InInvestmentModelAdmin(admin.ModelAdmin):
    # 搜索的时候，在搜出来的结果"xx条结果"后面不显示"总共xx"，耗性能
    # 但是好像基本也用不上搜索功能..
    show_full_result_count = False
    list_display = ['date', 'earnings']
    # 过滤
    list_filter = ['date']
    # # 设置排序方式
    ordering = ['-date']