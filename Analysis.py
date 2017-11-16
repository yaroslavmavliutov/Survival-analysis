import xlrd
from itertools import takewhile
from collections import Counter
import math
import numpy
import matplotlib.pyplot as plt

def load_data(name_file, age, virus):
    time_bed_days = [] # час, кількість ліжко/днів
    workbook = xlrd.open_workbook(name_file, on_demand=True)
    print(workbook.sheet_names())
    page = input('?: ')
    sheet = workbook.sheet_by_name(page)
    for i in range(sheet.ncols):
        if sheet.cell_value(0, i) == 'Вікова група':
            column_AGE = i # вибірка по віку
        if sheet.cell_value(0, i) == 'Противірусний препарат Х':
            column_VIRUS = i # вибірка по прийманню препаратів
        if sheet.cell_value(0, i) == 'Кількість ліжко/днів':
            col_len = len(sheet.col_values(i)) # кількість рядків в стовпчику
            for _ in takewhile(lambda x: not x, reversed(sheet.col_values(i))):
                col_len -= 1
            for k in range(col_len):
                 # обмежуємо вибірку за параметрами
                if sheet.cell_value(k, column_AGE) == age and sheet.cell_value(k, column_VIRUS) == virus:
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
    #print("Function_distribution: ", Function_distribution)
    Survival_function = []
    for i in range(0, len(Function_distribution)):
        Survival_function.append(1 - Function_distribution[i])
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
    return [1]+Survival_function, [0]+karman2, [0.1*Risk_function2[0]]+Risk_function2, [0]+karman


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

def Approximately_e(X_Array, Y_Array):
    x = numpy.asarray(X_Array)
    y = numpy.asarray(Y_Array)

    arr1 = numpy.polyfit(x, numpy.log(y), 1)    # y ≈ exp(arr[0]) * exp(arr[1] * x) = const * exp(arr[1] * x)
    x_range = [i for i in range(min(X_Array), max(X_Array))]
    fun = [math.exp(arr1[1])*math.exp(arr1[0]*i) for i in x_range]
    return fun, x_range

def main():
    for i in range(0, 1):
        age = float(input("age(1-3): "))
        virus = float(input("virus(0-1): "))
        time = load_data("Data.xlsx", age, virus)
        name = 'Age: ' + str(age) + ', Vaccine: ' + str(virus)
        s, karman, h, karman1 = kaplan_mayer(time)
        if s == [0] and karman == [0]:
            continue
        name_s = name + ', Area: ' + str(toFixed(sum(s), 3))

        plt.figure(1)
        plt.plot(karman1, s, label=name_s)
        plt.legend(loc='upper right')

        plt.figure(2)
        f, xr = Approximately_e(karman, h)
        #plt.plot(karman, h, 'o', label=name, markersize=10)
        plt.plot(xr, f, linewidth=2, label=name)
        plt.legend(loc='upper left')
        plt.grid(True)

    plt.show()



if __name__ == '__main__':
    main()