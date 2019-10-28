import lab3dataget as td
import math
import sys
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

def plot_it(x,y,xlabl = '',ylabl = '',sign = 'o'):
    plt.plot(x,y,sign)
    plt.xlabel(xlabl)
    plt.ylabel(ylabl)
    plt.show()

# td.downloads(sys.argv[0])
# Команда ниже выдает словарь основанный по ОИК округа который нужен. Ключи - строка соответствующая номеру ОИК. Нужный округ определяется ключевой фразой.
# task 1) Процент голосов за кандидатов от явки
#      2) аномальные выбросы и магические числа
#      3) явка от количества избирателей на участке
#      4) явка от количества избирательных участков

# list for analisis
count_of_uik = []
count_of_people = []
visit = []

name = "Красногвард"

# take data
names = td.get_table_name()
if any(list(map(lambda a: name in a, names['municipal']))):# area/ округ
    data_set_of_oik = td.get_area_site(name)
    for key in data_set_of_oik:
        data = data_set_of_oik[key]
        separation_line = next(x for x in range(len(data.iloc[:,2])) if type(data.iloc[x,0]) != str)+1
        count_of_uik.append(len(data.iloc[0,:]) - 2)
        visit.append(np.array(td.ls2f(data.iloc[9,2:])))
        count_of_people.append(np.array(td.ls2f(data.iloc[1,2:])))
elif any(list(map(lambda a: name in a, names['admin']))):
    data_set_of_oik = td.get_district_site(name)
    for kes in data_set_of_oik:
        for key in data_set_of_oik[kes]:
            data = data_set_of_oik[kes][key]
            separation_line = next(x for x in range(len(data.iloc[:,2])) if type(data.iloc[x,0]) != str)+1
            count_of_uik.append(len(data.iloc[0,:]) - 2)
            visit.append(np.array(td.ls2f(data.iloc[9,2:])))
            count_of_people.append(np.array(td.ls2f(data.iloc[1,2:])))
visit_OIK = list(map(lambda a,b: a.sum()/b.sum(), visit, count_of_people))
visit_UIK = list(map(lambda a,b: a/b, visit, count_of_people))
three = [reduce((lambda a,b: list(a)+list(b)),list(count_of_people)),reduce((lambda a,b: list(a)+list(b)),list(visit_UIK))]
four = [count_of_uik, visit_OIK]
plot_it(three[0],three[1])
plot_it(four[0],four[1])
