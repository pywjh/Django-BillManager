from django.contrib import admin
from .models import BillModel, DayDetailModel, SalaryDayModel

admin.site.site_title = '账单管理后台'
admin.site.site_header = '我的账单'

# Register your models here.
# admin.site.register(BillModel)
# admin.site.register(DayDetailModel)


@admin.register(BillModel)
class BillModelAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['date', 'salary', 'save_amount', 'budget', 'rent', 'salary_day', 'note']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['date', 'detail_id__note', 'detail_id__name']
    # 过滤
    list_filter = ['date']
    # # 设置排序方式
    # ordering = ['-date']


@admin.register(DayDetailModel)
class DayDetailAdmin(admin.ModelAdmin):
    list_display = ['date', 'name', 'amount', 'type', 'note']
    search_fields = ['date', 'name', 'type', 'note']
    # 过滤
    list_filter = ['date', 'type']
    list_per_page = 20


@admin.register(SalaryDayModel)
class DayDetailAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'company', 'day']
    search_fields = ['company']
    list_filter = ['company']