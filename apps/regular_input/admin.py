from django.contrib import admin
from .models import RegularInputItemsModel, RegularInputModel

# Register your models here.
admin.site.register(RegularInputItemsModel)


@admin.register(RegularInputModel)
class RegularInputModelAdmin(admin.ModelAdmin):
    # 设置模型字段，用于Admin后台数据的表头设置
    list_display = ['date', 'day_price', 'amount', 'item_id', 'amounts', 'copies', 'worth', 'yield_rate', 'note']
    # 设置可搜索的字段并在Admin后台数据生成搜索框，如有外键应使用双下划线连接两个模型的字段
    search_fields = ['date', 'item_id', 'item_id__name', 'note']
    # 过滤
    list_filter = ['date']
    fieldsets = (  # form页面 显示字段
        (None, {'fields': (
            'date', 'day_price', 'amount', 'item_id', 'amounts', 'copies', 'worth', 'note'
        )}),
    )
    # 设置排序方式
    ordering = ['-date']



