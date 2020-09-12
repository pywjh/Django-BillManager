# Django-BillManager
之前用Flask做了一个类似的，数据支持用的是csv文件，现在用Django做一个，数据库用的sqlite，方便使用



#####csv文件转数据库脚本
```python
import csv
from index.models import BillModel, DayDetailModel

bill_7 = BillModel.objects.get(date='2020-7-15')                                                                                                  

bill_7                                                                                                                                            
# <BillModel: 2020-07>

path = '/Users/wjh/Documents/project/ShangHaiBillManage/cost_record/2020/2020_7.csv'                                                              

with open(path, encoding='GBK') as f: 
    datas = [i for i in csv.DictReader(f) if i] 
                                                                                                                                                  

for i in datas: 
    i['date'] = f"2020-{i['date'].replace('_', '-')}" 
                                                                                                                                                  

for i in datas: 
    d = DayDetailModel() 
    d.date = i['date'] 
    d.name = i['name'] 
    d.amount = float(i['payment']) 
    d.type = i['type'] 
    d.note = i.get('note', '') 
    d.bill_id = bill_7 
    d.save() 
     
                                          
```