import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

def pars():

    xls_file = pd.ExcelFile('/home/yaroslav/Projects/Python/Medical_models/Survival-analysis/Data.xlsx')
    df = xls_file.parse('Вибірка 1')
    col_list_tem = ['Температура тіла\nдо лікування',
                    'Температура тіла\nчерез 3-7 діб',
                    'Температура тіла\nчерез 14 діб',
                    'Противірусний препарат Х']
    df_tem = df[col_list_tem]
    return df_tem

def ProbabilityArrayTemperature(data_tem):
    Stan_tem = np.zeros((3, 3))
    for element in range(0, len(data_tem)):

        # 0 день
        if data_tem.iloc[element][0] == 0:
            Stan_tem[2][0] = Stan_tem[2][0] + 1
        if data_tem.iloc[element][0] == 1:
            Stan_tem[1][0] = Stan_tem[1][0] + 1
        if data_tem.iloc[element][0] == 2:
            Stan_tem[0][0] = Stan_tem[0][0] + 1

        # 5 день
        if data_tem.iloc[element][1] == 0:
            Stan_tem[2][1] = Stan_tem[2][1] + 1
        if data_tem.iloc[element][1] == 1:
            Stan_tem[1][1] = Stan_tem[1][1] + 1
        if data_tem.iloc[element][1] == 2:
            Stan_tem[0][1] = Stan_tem[0][1] + 1

        # 14 день
        if data_tem.iloc[element][2] == 0:
            Stan_tem[2][2] = Stan_tem[2][2] + 1
        if data_tem.iloc[element][2] == 1:
            Stan_tem[1][2] = Stan_tem[1][2] + 1
        if data_tem.iloc[element][2] == 2:
            Stan_tem[0][2] = Stan_tem[0][2] + 1
    return Stan_tem

def frange(start, stop, step):
    opt = start
    while opt < stop:
        yield opt
        opt += step

def Approximately(Mass):
    x = np.asarray([1, 5, 14])
    y = np.asarray(Mass[1])

    arr1 = np.polyfit(x, np.sqrt(y), 1)  # y ≈ exp(arr[0]) * exp(arr[1] * x) = const * exp(arr[1] * x)
    x_range = [i for i in frange(min([1, 5, 14]), max([1, 5, 14]), 1)]
    fun = [math.sqrt(arr1[1] * i) for i in x_range]

    # # Обмежую y зверху одиницею
    # while fun[len(fun) - 1] < 1:
    #     x_range.append(max(x_range) + 0.1)
    #     fun.append(math.exp(arr1[1]) * math.exp(arr1[0] * (max(x_range) + 0.1)))
    # # якщо y > 1, то видаляю цей елемент
    # for i in range(len(fun) - 1, 0, -1):
    #     if fun[i] > 1:
    #         del fun[i]
    #         del x_range[i]
    #     else:
    #         continue

    return fun, x_range

def VisualizationCurve(mass):
    plt.figure(1)
    plt.plot(mass[1], mass[0], label='lol')
    plt.legend(loc='upper left')
    plt.grid(True)

def main():
    data_tem = pars()
    Temperature_with_vaccine = data_tem[(data_tem['Противірусний препарат Х'] == 1)]
    Temperature_without_vaccine = data_tem[(data_tem['Противірусний препарат Х'] == 0)]

    #VisualizationCurve(ProbabilityArrayTemperature(data_tem))
    #VisualizationCurve(ProbabilityArrayTemperature(Temperature_with_vaccine))
    Matrix = ProbabilityArrayTemperature(Temperature_without_vaccine)
    y, x = Approximately(Matrix)
    VisualizationCurve([y, x])
    VisualizationCurve([Matrix[1], [1,5,14]])
    plt.show()

if __name__ == '__main__':
    main()