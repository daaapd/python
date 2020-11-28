import string
f = open('1.txt','r',encoding='UTF8')
text=f.read()
f.close()
#print(text)
# 1 задание
text_not_punkt=text.replace(',','').replace('.','').replace('!','').replace('?','').replace('«','').replace('«','')\
    .replace('»','').replace('—','')
#print(text_not_punkt)
# Задача 2
list_text=text_not_punkt.split()
#print(list_text)
#Задание 3
lower_list=list(map(lambda x:x.lower(),list_text))
print(lower_list)
#Задание 3
set_text=set(lower_list)
#print(type(set_text),set_text)
#Задание 3
dict_temp = {}
for element in set_text:
    #print(element,lower_list.count(element))
    dict_temp[element]=lower_list.count(element)
#print(dict_temp)
#Задание 4
list_d=list(dict_temp.items())
list_d.sort(key=lambda i:i[1],reverse=True)
print(list_d[:5])

#Задание 5
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
#print(lower_list[0])
normal_list = list(map(lambda x: morph.parse(x[0])[0].normal_form, lower_list))
print(normal_list)


