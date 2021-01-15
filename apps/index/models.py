from django.db import models
from django.utils import timezone, formats

# Create your models here.


class BillModel(models.Model):
    date = models.DateField('日期', default=timezone.now, unique=True)
    salary = models.FloatField('工资')
    save_amount = models.FloatField('存储金', null=True, blank=True)
    budget = models.FloatField('预算')
    rent = models.FloatField('房租')
    salary_day = models.IntegerField('发薪日')
    note = models.TextField('备注', blank=True, null=True, max_length=256)

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
    type = models.CharField('类别', choices={('eat', '饮食'), ('other', '其他')}, max_length=10)
    note = models.TextField('备注', max_length=256, null=True, blank=True)
    bill_id = models.ForeignKey(
        'BillModel',
        on_delete=models.CASCADE,
        related_name='day_detail',
        verbose_name='总账',
        db_column='bill_id',
        default=BillModel.objects.first() and BillModel.objects.first().id
    )

    class Meta:
        ordering = ['-date', '-id']
        db_table = 'tb_day_detail'
        verbose_name = '日记账'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return formats.date_format(self.date)


class SalaryDayModel(models.Model):
    day = models.IntegerField('发薪日')
    start_date = models.DateField('开始时间', default=timezone.localdate, unique=True)
    end_date = models.DateField('结束时间', null=True, blank=True)
    company = models.CharField('在职公司', max_length=256)

    class Meta:
        ordering = ['-start_date']
        db_table = 'tb_salary_day'
        verbose_name = '发薪日'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{formats.date_format(self.start_date)}-{self.company}"