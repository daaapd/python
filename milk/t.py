import sqlalchemy
from datetime import datetime,timedelta
from dateutil import parser
import random
import requests

# connect the database.  substitute the needed values.
engine = sqlalchemy.create_engine('mysql://readonlyuser:sdnv29b9nOASknc2eivn29bv@82.146.48.79/merch-server?charset=utf8mb4')
connect=engine.connect()
date_report= '03/12/2020'
#date_report=parser.parse(date_report)
#print(date_report)
#d=date_report.strftime('%d/%m/%Y')
#print(d)
from sqlalchemy import text,select
sql="select   FROM_UNIXTIME(ri.createdAt) as date_ \
        ,(select comment from reportItem ri2 where reportId=ri.reportId and productId=7310) as pointId\
        ,p.productId \
        ,p.title \
        ,ri.face \
        ,ri.price \
        ,ri.balance \
        ,r.latitude \
        ,r.longitude \
        ,rp.url \
        ,upper(st.title) store \
        ,sa.storeAddressid \
from product p \
join  reportItem ri on ri.productId=p.productId \
join  report r on r.reportId=ri.reportId and date(FROM_UNIXTIME(r.createdAt))=STR_TO_DATE('"+date_report+"', '%d/%m/%Y') \
join storeAddress sa on sa.storeAddressId=r.storeAddressId \
join store st on st.storeId = sa.storeId \
join (select rp1.reportId, GROUP_CONCAT(concat('http://mobile.salegroup-merch.ru/',f.url) ORDER BY rp1.reportid) as url \
        from reportPhoto rp1 \
        join file f on rp1.fileId=f.fileId \
        group by rp1.reportid) rp on ri.reportId=rp.reportId \
where upper(p.title) like '%MAKFA%'"

query_1=text(sql)

result_1=connect.execute(query_1)

mysql_list=list(result_1)
#print(mysql_list[1:4]['pointId'])
l=[]
for i in mysql_list:
    l.append(i['pointId'])
point=set(l)
#print(point)
forms = []
#pointId=set(mysql_list)
for p in point:
    list_prod = []
    for i in mysql_list:
        if i['pointId']==p:
            str=i['title']
            str = str[str.find('<') + 1:str.find('>')]
            dict_prod={'SKU': int(str),'Фейсинг':i['face'],'Цена': i['price'],'Остаток': i['balance']}
            list_prod.append(dict_prod)
            date=i['date_']
            Longitude=i['longitude']
            Latitude=i['latitude']
            photoList=i['url'].split(',')
            store=i['store']
            storeAddressid=i['storeAddressid']
    if store.find('ПЕРЕКРЕСТ') != -1:
        delta=random.randint(55, 100)
    elif store.find('ЛЕНТА') != -1:
        delta = random.randint(225, 235)
    else:
        delta = random.randint(40, 55)
    date_b=date-timedelta(minutes=delta)
    d_b=date_b.strftime('%d.%m.%Y')
    d_b_t = date_b.strftime('%H:%M')
    d_e = date.strftime('%d.%m.%Y')
    d_e_t = date.strftime('%H:%M')
    dict_point={'PointId': int(p),
                'LocalFormId': storeAddressid,
                'SimpleFields': {'Latitude': Latitude,
                                 'Longitude': Longitude,
                                 'Дата визита': d_b,
                                 'Время прихода': d_b_t,
                                 'Время ухода': d_e_t
                                 },
                'TableFields': {'Ассортимент in-out': list_prod
                                },
                'Photo': {'Фото ПОСЛЕ': photoList

                        }
                }
    forms.append(dict_point)
#print(mysql_list[1]['date_'].strftime('%H:%M'))
import json
import re

path = './upload/'
# filename = 'wub.csv'
now= datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
now = re.sub(r'[^A-zА-я0-9]', '', now)
filename = 'report' + now + '.json'
d = {
    'token': 'cb8fbb50-cce1-4a5d-b73d-0d1e953e6554',
        'forms': forms
        }

with open(path+filename, 'w',encoding='utf8') as f:
    json.dump(d, f,ensure_ascii=False)
headers = {'Content-type': 'application/json', 'token': 'cb8fbb50-cce1-4a5d-b73d-0d1e953e6554'}
url = 'http://upload.ofrs.su/UploadAggregatorsData.ashx'
#print(json.dumps(d, ensure_ascii=false))
#requests.p
#files = {'files': open(path+filename, 'rb')}
#r = requests.post(url, files=files, headers=headers)
print(json.dumps(d, ensure_ascii=False).encode('utf8'))
r = requests.post(url, data=json.dumps(d, ensure_ascii=False).encode('utf8'), headers=headers)
print(r)
r.encoding='utf-8'
print(r.text)
#s = json.dumps(r.text)
#s=str(r)
#print(s)
with open(path+'respon'+filename, 'wb') as fd:
    for chunk in r.iter_content(100):
        fd.write(chunk)