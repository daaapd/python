import xlrd, xlwt
#открываем файл
rb = xlrd.open_workbook('./upload/Макфа-Перекресток(97).xlsx')

#выбираем активный лист
sheet = rb.sheet_by_index(0)
#получаем список значений из всех записей
vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
print(vals)




str = '<23>Макароны для теста'
str = str[str.find('<')+1:str.find('>')]
print(str)
import json
filename='test_json.json'
d = {
    'token': 'cb8fbb50-cce1-4a5d-b73d-0d1e953e6554',
    'forms': [{'LocalFormId':1,
               'PointId':1,
               'SimpleFields':{'Latitude':500,
                               'Longitude':500,
                               'Дата визита':'31.01.2000',
                               'Время прихода':'12:30',
                                'Комментарий': 'текст',
                                'Время ухода': '12:30',
                                'Присутствие стойки_СС': 'true',
                                'Кол-во фото': 'текст'
                                },
               'TableFields':{'Ассортимент in-out:':{'SKU': 1,
                                                    'Фейсинг': 500,
                                                    'Цена': 500,
                                                    'Цена промо': 500,
                                                    'Остаток': 500,
                                                    'Причина отсутствия': 1
                                                    }

                            }
               }
              ]
}

with open(filename, 'w') as f:
    json.dump(d, f,ensure_ascii=False)