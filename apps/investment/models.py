from django.db import models
from django.utils import timezone, formats
from ckeditor.fields import RichTextField

# Create your models here.


class InvestmentModel(models.Model):
    date = models.DateField('日期', default=timezone.now, unique=True, blank=False)
    earnings = models.FloatField('收益', blank=False, null=False)
    note = RichTextField('备注', blank=True, null=True)

    class Meta:
        db_table = 'tb_investment'  # 指明数据库表明
        verbose_name = '理财收益'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return formats.date_format(self.date)