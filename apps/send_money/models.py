from django.db import models

# Create your models here.


class FriendShipModel(models.Model):
    """关系程度"""
    extent = models.CharField("程度", max_length=30, unique=True, null=False)
    level = models.IntegerField("权重", default=0)

    class Meta:
        db_table = 'tb_friendship'  # 指明数据库表明
        verbose_name = '关系程度表'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.extent


class FriendsModel(models.Model):
    """朋友圈"""
    name = models.CharField("姓名", max_length=20, unique=True, null=False)
    friendship = models.OneToOneField(FriendShipModel, on_delete=models.CASCADE, related_name="friendship", verbose_name="关系")
    city = models.CharField("城市", max_length=20)
    note = models.CharField("备注", max_length=255)

    class Meta:
        db_table = 'tb_friend'  # 指明数据库表明
        verbose_name = '朋友圈'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"<{self.name}>"


class SendMoneyRecordModel(models.Model):
    """随礼记录"""
    thing = models.CharField("事件", max_length=255, null=False)
    friend = models.OneToOneField(FriendsModel, on_delete=models.DO_NOTHING, related_name="friend", verbose_name="关系人")
    amount = models.FloatField("金额", default=0)
    is_refund = models.BooleanField("是否回礼", default=False)

    create_time = models.DateTimeField(verbose_name="发生时间", auto_now_add=True)
    refund_time = models.DateTimeField(verbose_name="回礼时间")

    class Meta:
        db_table = 'tb_send_money_record'  # 指明数据库表明
        verbose_name = '随礼记录'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"<{self.amount}, {self.thing}>"


