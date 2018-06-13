import xlrd
from itertools import takewhile
from MarkovChain.BuildingChain import *
from MarkovChain.ComparisonOfCurves import comparisonbuildingcurves
from collections import Counter
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from Prediction.TreeDecision import predict


def load_data_age(name_file, age, virus, temp, mokrota, rentgeno, lokaliz, zagaln, num):
    time_bed_days = [] # час, кількість ліжко/днів
    workbook = xlrd.open_workbook(name_file, on_demand=True)
    sheet = workbook.sheet_by_name('Вибірка 1')
    for i in range(sheet.ncols):
        if sheet.cell_value(0, i) == 'Вікова група':
            column_AGE = i # вибірка по віку
        if sheet.cell_value(0, i) == 'Противірусний препарат Х':
            column_VIRUS = i # вибірка по прийманню препаратів

        if sheet.cell_value(0, i) == 'Температура тіла\nдо лікування':
            column_temp = i # вибірка по прийманню препаратів
        if sheet.cell_value(0, i) == 'Характер мокроти\nдо лікування':
            column_mokrota = i # вибірка по прийманню препаратів
        if sheet.cell_value(0, i) == 'Рентгенодинаміка\nдо лікування':
            column_rentgeno = i # вибірка по прийманню препаратів
        if sheet.cell_value(0, i) == 'Локалізація НП\nдо лікування':
            column_lokaliz = i # вибірка по прийманню препаратів
        if sheet.cell_value(0, i) == 'Загальний стан хворого\nдо лікування':
            column_zagaln = i # вибірка по прийманню препаратів

        if sheet.cell_value(0, i) == 'Кількість ліжко/днів':
            col_len = len(sheet.col_values(i)) # кількість рядків в стовпчику
            for _ in takewhile(lambda x: not x, reversed(sheet.col_values(i))):
                col_len -= 1
            for k in range(col_len):
                 # обмежуємо вибірку за параметрами
                if num == 1:
                    if sheet.cell_value(k, column_AGE) == age and sheet.cell_value(k, column_temp) == temp:
                        time_bed_days.append(sheet.cell_value(k, i))
                elif num == 0:
                    if sheet.cell_value(k, column_VIRUS) == virus:

                        time_bed_days.append(sheet.cell_value(k, i))
    #del time_bed_days[0]
    #print("Time: ", time_bed_days)
    return time_bed_days

def kaplan_mayer(time):
    if len(time) <= 1:
        return [0], [0], [0], [0]
    time.sort()
    mine = min(time)
    maxe = max(time)
    karman = [i for i in range(int(mine), int(maxe+1))] # карман - від мінімального до максимального
    c = Counter(time)
    Frequency_count_bed_days = [c[i] for i in karman] # частота кожного з показників ліжко/дня
    Frequency_percent = [i/sum(Frequency_count_bed_days) for i in Frequency_count_bed_days] # частота у відсотках
    #print("Frequency_percent: ", Frequency_percent)
    Function_distribution = [] # функція щільності
    for i in range(0, len(Frequency_percent)):
        if i != 0:
            Function_distribution.append(Frequency_percent[i] + Function_distribution[i-1])
        else:
            Function_distribution.append(Frequency_percent[i])
    if Function_distribution[len(Function_distribution) - 1] > 1:
        Function_distribution[len(Function_distribution) - 1] = 1
    #print("Function_distribution: ", Function_distribution)
    Survival_function = [(1 - i) for i in Function_distribution]
    # for i in range(0, len(Function_distribution)):
    #     Survival_function.append(1 - Function_distribution[i])
    Risk_function = [(Function_distribution[i+1] - Function_distribution[i])/Survival_function[i] for i in range(0, len(Function_distribution) - 1)]
    #print("Risk: ", Risk_function)
    #del karman[len(karman) - 1]  # щоб розмірності співпадали
    Risk_function2 = []  # в 2 видалимо всі 0
    karman2 = []
    for i in range(0, len(Risk_function)):
        if Risk_function[i] != 0:
            Risk_function2.append(Risk_function[i])
            karman2.append(karman[i+1])
    #return Survival_function, karman, Smoothing(Risk_function)
    return [0.99]+Survival_function, [0]+karman2, [0.1*Risk_function2[0]]+Risk_function2, [0]+karman


# def Smoothing(list):
#     for i in range(0, len(list)):
#         if list[i] == 0:
#             if i == 0:
#                 continue
#             if i == len(list) - 1:
#                 list[i] = list[i-1]
#             for j in range(1, i+1):
#                 if list[i-j] != 0:
#                     a = list[i-j]
#                     break
#                 else:
#                     a=0
#             for j in range(1, len(list) - i):
#                 if list[i + j] != 0:
#                     b = list[i+j]
#                     break
#                 else:
#                     pass
#             list[i] = (a+b)/2
#     return list

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

def frange(start, stop, step):
    opt = start
    while opt < stop:
        yield opt
        opt += step

def Approximately_e(X_Array, Y_Array):
    x = np.asarray(X_Array)
    y = np.asarray(Y_Array)

    arr1 = np.polyfit(x, np.log(y), 1)    # y ≈ exp(arr[0]) * exp(arr[1] * x) = const * exp(arr[1] * x)
    x_range = [i for i in frange(min(X_Array), max(X_Array), 0.1)]
    fun = [math.exp(arr1[1])*math.exp(arr1[0]*i) for i in x_range]

    # Обмежую y зверху одиницею
    while fun[len(fun) - 1] < 1:
        x_range.append(max(x_range) + 0.1)
        fun.append(math.exp(arr1[1]) * math.exp(arr1[0] * (max(x_range) + 0.1)))
    # якщо y > 1, то видаляю цей елемент
    for i in range(len(fun) - 1, 0, -1):
        if fun[i] > 1:
            del fun[i]
            del x_range[i]
        else:
            continue

    return fun, x_range

def New_Survive_fun(Y_Array, X_Array):
    for i in range(len(Y_Array) - 1, 0, -1):
        if Y_Array[i] == 0:
            del Y_Array[i]
            del X_Array[i]
        else:
            continue

    x = np.asarray(X_Array)
    y = np.asarray(Y_Array)

    arr1 = np.polyfit(x, np.log(abs((1/y) - 1)), 1)
    x_range = [i for i in frange(0, max(X_Array), 0.01)]
    fun = [1/( 1 + math.exp(arr1[1]) * math.exp(arr1[0] * i)) for i in x_range]

    while fun[len(fun) - 1] > 0.01:
        x_range.append(max(x_range) + 0.01)
        fun.append(1/( 1 + math.exp(arr1[1]) * math.exp(arr1[0] * (max(x_range) + 0.01))))
    for i in range(len(fun) - 1, 0, -1):
        if fun[i] < 0:
            del fun[i]
            del x_range[i]
        else:
            continue

    # порахуємо h
    # H = [(1 - fun[i + 1] / fun[i]) for i in range(0, len(fun) - 1)]
    # print(H)
    return fun, x_range


def main(num1, num, data):
    #print('1 - Побудова кривих, 2 - Розподіл, 3 - Отримати прогноз вірусного агента')
    #num = int(input("number: "))

    if num1 == 1:
        # вік, температура
        # print('0 - Загальне одужання')
        # print('1 - Загальне одужання в залежності від віку, 2 - Динаміка температури, 3 - Динаміка характеру мокроти, ')
        # print('4 - Динаміка локалізації НП, 5 - Динаміка рентгенодинаміки, 6 - Динаміка загального стану')
        # print('7 - Порівняти криві температури, 8 - Порівняти криві характеру мокроти, 9 - Порівняти криві локалізації НП,')
        # print('10 - Порівняти криві рентгенодинаміки, 11 - Порівняти криві загального стану')
        #num = int(input("number: "))
        if num == 0:
            for virus in range(0, 2):
                #namefile = "Data.xlsx"
                # name_a = ''
                age = 100
                if virus == 0:
                    # print('Противірусний препарат відсутній')
                    name_v = 'Терапія 1'
                    time = load_data_age(data[0], age, virus, 0, 0, 0, 0, 0, num)
                elif virus == 1:
                    # print('Противірусний препарат наявний')
                    name_v = 'Терапія 2'
                    time = load_data_age(data[1], age, virus, 0, 0, 0, 0, 0, num)
                # name = 'Age: ' + str(age) + ', Vaccine: ' + str(virus)
                # name = 'Противірусний апарат: ' + str(virus)
                name = name_v
                s, karman, h, karman1 = kaplan_mayer(time)
                if s == [0] and karman == [0]:
                    continue

                f, xr = Approximately_e(karman, h)

                new_s, new_x = New_Survive_fun(s, karman1)
                plt.figure(1)
                if virus == 0:
                    save_s = new_s
                # plt.plot(karman1, s, label=name_s)
                plt.title('Криві одужання')
                plt.xlabel('Дні госпіталізації')
                plt.ylabel('Ймовірність залишитися в стаціонарі')
                plt.plot(new_x, new_s, label=name)
                plt.legend(loc='upper right')

                del new_x[len(new_x) - 1]
                #plt.figure(2)
                #plt.title('')
                # plt.plot(karman, h, 'o', label=name, markersize=10)
                #plt.plot(xr, f, linewidth=2, label=name)
                #plt.legend(loc='upper left')
                plt.grid(True)
                if virus == 1:
                    sum1 = 0
                    sum2 = 0
                    for i in range(1, len(new_s)):
                        di0 = (new_s[i-1] - new_s[i])*10
                        di1 = (save_s[i - 1] - save_s[i])*10

                        ti0 = (new_s[i-1])*10
                        ti1 = (save_s[i-1])*10

                        ni0 = (new_s[i])*10
                        ni1 = (save_s[i])*10

                        sum1 = sum1 + (di0 - ti0*(di0+di1)/(ti0+ti1))
                        sum2 = (ti1*ti0*(di0+di1)*(ni0+ni1))/((ti0+ti1)*(ti0+ti1)*((ti0+ti1)))
                    #print(sum1*sum1)
                    #print(sum2)

        elif num == 1:
            # age = float(input("age(1-3): "))
            # virus = float(input("virus(0-1): "))
            namefile = "Data.xlsx"
            age = 2
            virus = 0
            if float(data[0]) < 30:
                age = 1
            elif float(data[0]) >= 30 and float(data[0]) < 60:
                age = 2
            else: age = 3

            if float(data[1]) < 37:
                temp = 1
            elif float(data[1]) >= 37 and float(data[1]) < 38:
                temp = 1
            else: temp = 2

            if data[2] == 'Відсутнє':
                mokr = '0'
            elif data[2] == 'Слизове':
                mokr = '1'
            elif data[2] == 'Слизово-гнійне':
                mokr = '2'
            else: mokr = '3'

            if data[3] == 'Відсутня':
                lok = '0'
            elif data[3] == 'Однобічна':
                lok = '1'
            else: lok = '2'

            if data[4] == 'Повне розсмоктування':
                rent = '1'
            elif data[4] == 'Часткове розсмоктування':
                rent = '2'
            elif data[4] == 'Динаміка відсутня':
                rent = '3'
            else: rent = '4'

            if data[5] == 'Стабільний':
                zag = 1
            elif data[5] == 'Середньої важкості':
                zag = 2
            else: zag = 3

            time = load_data_age(namefile, age, virus, temp, mokr, rent, lok, zag, num)
            # name = 'Age: ' + str(age) + ', Vaccine: ' + str(virus)
            #name = 'Противірусний апарат: ' + str(virus)
            #name = name_a + '. ' + name_v
            name = 'Крива одужання'
            s, karman, h, karman1 = kaplan_mayer(time)
            if s == [0] and karman == [0]:
                pass

            new_s, new_x = New_Survive_fun(s, karman1)
            plt.figure(1)
            # plt.plot(karman1, s, label=name_s)
            plt.title('Криві одужання')
            plt.xlabel('Дні госпіталізації')
            plt.ylabel('Ймовірність залишитися в стаціонарі')
            plt.plot(new_x, new_s, label=name)
            plt.legend(loc='upper right')

            del new_x[len(new_x) - 1]
            plt.grid(True)
        elif num in (2, 3, 4, 5, 6):
            # try: buildingcurvesfromprobably(num)
            # except: pass
            buildingcurvesfromprobably(num)
        elif num in (7, 8, 9, 10, 11):
            try: comparisonbuildingcurves(num-5)
            except: pass
    elif num1 == 2:
        predict()
    plt.show()



if __name__ == '__main__':
    main()