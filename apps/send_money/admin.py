from django.contrib import admin
from .models import FriendsModel, FriendShipModel, SendMoneyRecordModel

# Register your models here.


@admin.register(FriendsModel)
class FriendsModelAdmin(admin.ModelAdmin):
    # 搜索的时候，在搜出来的结果"xx条结果"后面不显示"总共xx"，耗性能
    # 但是好像基本也用不上搜索功能..
    show_full_result_count = False
    list_display = ['name', 'friendship', 'city', 'note']
    # 过滤
    list_filter = ['name']
    # # 设置排序方式
    ordering = ['name']
    search_fields = ['name', 'note']
    list_per_page = 20


@admin.register(FriendShipModel)
class FriendShipModelAdmin(admin.ModelAdmin):
    show_full_result_count = False
    list_display = ['extent', 'level']
    # 过滤
    list_filter = ['extent', 'level']
    # # 设置排序方式
    ordering = ['level']
    search_fields = ['extent', 'level']
    list_per_page = 20


@admin.register(SendMoneyRecordModel)
class SendMoneyRecordModelAdmin(admin.ModelAdmin):
    show_full_result_count = False
    list_display = ['thing', 'friend', 'amount', 'create_time', 'is_refund', 'refund_time']
    # 过滤
    list_filter = ['friend', 'is_refund']
    # # 设置排序方式
    ordering = ['-create_time']
    search_fields = ['thing', 'create_time', 'refund_time']
    list_per_page = 20