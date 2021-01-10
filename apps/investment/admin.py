from django.contrib import admin
from .models import InvestmentModel

# Register your models here.


@admin.register(InvestmentModel)
class InInvestmentModelAdmin(admin.ModelAdmin):
    list_display = ['date', 'earnings']
    # 过滤
    list_filter = ['date']
    # # 设置排序方式
    ordering = ['-date']