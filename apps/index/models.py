from django.db import models
from django.utils import timezone, formats

# Create your models here.


class BillModel(models.Model):
    date = models.DateField('日期', default=timezone.now, unique=True)
    salary = models.FloatField('工资')
    save_amount = models.FloatField('存储金')
    budget = models.FloatField('预算')
    rent = models.FloatField('房租')
    salary_day = models.IntegerField('发薪日')
    note = models.CharField('备注', blank=True, null=True, max_length=256)
    detail_id = models.OneToOneField('DayDetailModel', on_delete=models.SET_NULL, verbose_name='日记账', null=True, blank=True)

    class Meta:
        ordering = ['-date', '-id']
        db_table = 'tb_bill'  # 指明数据库表明
        verbose_name = '总账表'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.date.strftime('%Y-%m')


class DayDetailModel(models.Model):
    date = models.DateField('日期', default=timezone.now)
    name = models.CharField('用途', max_length=20)
    amount = models.FloatField('金额')
    type = models.CharField('类别', choices={('饮食', 'eat'), ('其他', 'other')}, max_length=10)
    note = models.TextField('备注', max_length=256)
    bill_id = models.OneToOneField('BillModel', on_delete=models.CASCADE, to_field='date', verbose_name='总账')

    class Meta:
        ordering = ['-date', '-id']
        db_table = 'tb_day_detail'
        verbose_name = '日记账'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return formats.dateformat(self.date)