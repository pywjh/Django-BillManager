from django.db import models

from ckeditor.fields import RichTextField
from django.utils import timezone, formats

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
    date = models.DateField('日期', default=timezone.now, blank=False)
    day_price = models.FloatField('成交单价', blank=False, null=False)
    amount = models.FloatField('定投金额', blank=False, null=False)
    item_id = models.ForeignKey(
        "RegularInputItemsModel",
        on_delete=models.CASCADE,
        verbose_name="定投对象",
        db_column="item_id",
        related_name="regular_input_ids",
        blank=False,
        null=False
    )
    amounts = models.FloatField('累计投资', blank=False, null=False, default=1)
    copies = models.FloatField('成交份额', blank=False, null=False)
    worth = models.FloatField('当前价值', blank=False, null=False, default=0)

    yield_rate = models.CharField('收益率', max_length=255)
    total_earning = models.FloatField('总收益', default=0)
    note = RichTextField('备注', blank=True, null=True)

    class Meta:
        db_table = 'tb_regular_input'
        verbose_name = '定投记录'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.yield_rate = '{:.2%}'.format((self.worth - self.amounts) / self.amounts)
        self.total_earning = round(self.worth - self.amounts, 2)
        return super(RegularInputModel, self).save(args, **kwargs)

    def __str__(self):
        return f"{formats.date_format(self.date)}-{self.item_id.name}"


class ButtStockModel(models.Model):
    """烟蒂股"""
    date = models.DateField('日期', default=timezone.now, blank=False)
    day_price = models.FloatField('成交单价', blank=False, null=False)
    amount = models.FloatField('金额', blank=True, null=True)
    item_id = models.ForeignKey(
        "RegularInputItemsModel",
        on_delete=models.CASCADE,
        verbose_name="投资对象",
        db_column="item_id",
        related_name="butt_stock_ids",
        blank=False,
        null=False
    )
    copies = models.FloatField('成交份额', blank=False, null=False)
    end_worth = models.FloatField('完结价值', blank=True, null=True, default=0)

    yield_rate = models.CharField('收益率', max_length=255)
    total_earning = models.FloatField('总收益', default=0)
    note = RichTextField('备注', blank=True, null=True)

    class Meta:
        db_table = 'tb_butt_stock'
        verbose_name = '烟蒂股'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        self.amount = round((self.copies * self.day_price), 2)
        self.yield_rate = '{:.2%}'.format((self.end_worth - self.amount) / self.amount)
        self.total_earning = round(self.end_worth - self.amount, 2)
        return super(ButtStockModel, self).save(args, **kwargs)

    def __str__(self):
        return f"{formats.date_format(self.date)}-{self.item_id.name}"
