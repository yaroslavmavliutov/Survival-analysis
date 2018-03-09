import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import math

from scipy.optimize import fsolve

def pars(number):

    xls_file = pd.ExcelFile('/home/yaroslav/Projects/Python/Medical_models/Survival-analysis/Data.xlsx')
    df = xls_file.parse('Вибірка 1')
    if number == 2:
        #3x3
        col_list_tem = ['Температура тіла\nдо лікування',
                        'Температура тіла\nчерез 3-7 діб',
                        'Температура тіла\nчерез 14 діб',
                        'Противірусний препарат Х']
        Pwithvaccine = [0.31, 0.4, 0.1, 0.28]
        Pwithoutvaccine = [0.33, 0.49, 1, 0.21]
    elif number == 3:
        #4x4
        col_list_tem = ['Характер мокроти\nдо лікування',
                        'Характер мокроти\nчерез 3-7 діб',
                        'Характер мокроти\nчерез 14 діб',
                        'Противірусний препарат Х']
        Pwithvaccine = [0.21, 0.1, 0.08, 0.04]
        Pwithoutvaccine = [0.36, 0.009, 0.07, 0.11]

    elif number == 4:
        #3x3
        col_list_tem = ['Локалізація НП\nдо лікування',
                        'Локалізація НП\nчерез 3-7 діб',
                        'Локалізація НП\nчерез 14 діб',
                        'Противірусний препарат Х']
        Pwithvaccine = [0.01, 0.01, 0.99, 0.42]
        Pwithoutvaccine = [0.01, 0.01, 0.12, 0.24]

    elif number == 5:
        #3x3
        col_list_tem = ['Рентгенодинаміка\nдо лікування',
                        'Рентгенодинаміка\nчерез 3-7 діб',
                        'Рентгенодинаміка\nчерез 14 діб',
                        'Противірусний препарат Х']
        Pwithvaccine = [0.3, 0.01, 0.99, 0.35]
        Pwithoutvaccine = [0.42, 0.01, 0.99, 0.24]

    df_tem = df[col_list_tem]
    return df_tem, Pwithvaccine, Pwithoutvaccine


def ArrayParameter(data_tem):
    del data_tem['Противірусний препарат Х']
    massive_unique = np.sort(pd.Series(data_tem.values.ravel()).unique())

    CountElements = massive_unique.size
    Stan_tem = np.zeros((CountElements, 3))
    for element in range(0, len(data_tem)):
        # 0 день
        for index, degree in enumerate(massive_unique):
            if data_tem.iloc[element][0] == degree:
                Stan_tem[np.where(massive_unique==degree)[0][0]][0] = Stan_tem[np.where(massive_unique==degree)[0][0]][0] + 1

        # 5 день
        for index, degree in enumerate(massive_unique):
            if data_tem.iloc[element][1] == degree:
                Stan_tem[np.where(massive_unique==degree)[0][0]][1] = Stan_tem[np.where(massive_unique==degree)[0][0]][1] + 1

        # 14 день
        for index, degree in enumerate(massive_unique):
            if data_tem.iloc[element][2] == degree:
                Stan_tem[np.where(massive_unique==degree)[0][0]][2] = Stan_tem[np.where(massive_unique==degree)[0][0]][2] + 1

    for i in range(0, CountElements):
        for j in range(0, 3):
            Stan_tem[i][j] = Stan_tem[i][j]/len(data_tem)

    return np.asarray(Stan_tem[::-1]), massive_unique


def FunctionCalculationCurves(stans, massive_unique, p):
    if len(massive_unique) == 3:

        loop1 = np.asarray([[1-p[0], 0, 0],
                            [p[0], 1-p[1], 0],
                            [0, p[1], 1]])
        loop2 = np.asarray([[1-p[2], 0, 0],
                            [p[2], 1-p[3], 0],
                            [0, p[3], 1]])
    elif len(massive_unique) == 4:

        loop1 = np.asarray([[1-p[0], 0, 0, 0],
                            [p[0], 1-p[1], 0, 0],
                            [0, p[1], 1-p[2], 0],
                            [0, 0, p[2], 1]])
        loop2 = np.asarray([[1-p[3], 0, 0, 0],
                            [p[3], 1-p[4], 0, 0],
                            [0, p[4], 1-p[5], 0],
                            [0, 0, p[5], 1]])

    # [1, 5, 14]
    Data = stans.transpose()[0]

    for i in range(2, 5):
        Data = np.append(Data, np.dot(np.linalg.matrix_power(loop1, i), stans.transpose()[0]))

    Data = np.append(Data, stans.transpose()[1])

    for j in range(6, 14):
        Data = np.append(Data, np.dot(np.linalg.matrix_power(loop2, j), stans.transpose()[1]))

    #Data = np.append(Data, stans.transpose()[2])

    Data = Data.reshape(13, massive_unique.size)

    Stan_tem = np.zeros((massive_unique.size, 13))
    for i in range(0, 13):
        for index, degree in enumerate(massive_unique):
            Stan_tem[index][i] = Data[i][index]
    return Stan_tem, [i for i in range(0, 13)]

def VisualizationCurve(mass):
    plt.figure(1)
    plt.plot(mass[1], mass[0], label='rate')
    plt.legend(loc='upper left')
    plt.grid(True)

def buildingcurvesfromprobably(number):
    data_tem, pWITH, pWITHOUT = pars(number)
    number = int(input("Пацієнти з противірусним - 1, без - 0: "))
    if number == 0:
        Data = data_tem[(data_tem['Противірусний препарат Х'] == 1)]
        p = pWITH
    elif number == 1:
        Data = data_tem[(data_tem['Противірусний препарат Х'] == 0)]
        p = pWITHOUT

    Vectors, massive_unique = ArrayParameter(Data)


    Y, X = FunctionCalculationCurves(Vectors, massive_unique, p)

    for i in range(0, massive_unique.size):
        VisualizationCurve([Y[i], X])
    plt.show()

def main():
    buildingcurvesfromprobably()

if __name__ == '__main__':
    main()