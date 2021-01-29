from django.utils import timezone, formats

from django.db import models

# Create your models here.


class RegularInputItemsModel(models.Model):
    """定投对象"""
    name = models.CharField('名称', max_length=255, blank=False, null=False)
    code = models.CharField('代码', max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'tb_regular_input_items'
        verbose_name = '定投对象'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.name}({self.code})'


class RegularInputModel(models.Model):
    """定投记录"""
    date = models.DateField('日期', default=timezone.now, unique=True, blank=False)
    day_price = models.FloatField('成交单价', blank=False, null=False)
    amount = models.FloatField('定投金额', blank=False, null=False)
    item_id = models.ForeignKey(
        "RegularInputItemsModel",
        on_delete=models.CASCADE,
        verbose_name="定投对象",
        db_column="item_id",
        related_name="item_ids",
        blank=False,
        null=False
    )
    amounts = models.FloatField('累计投资', blank=False, null=False, default=1)
    copies = models.FloatField('成交份额', blank=False, null=False)
    worth = models.FloatField('当前价值', blank=False, null=False, default=0)

    yield_rate = models.CharField('收益率', max_length=255)
    note = models.TextField('备注', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'tb_regular_input'
        verbose_name = '定投记录'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.yield_rate = '{:.2%}'.format((self.worth - self.amounts) / self.amounts)
        return super(RegularInputModel, self).save(args, **kwargs)

    def __str__(self):
        return f"{formats.date_format(self.date)}"