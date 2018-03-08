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
        col_list_tem = ['Температура тіла\nдо лікування',
                        'Температура тіла\nчерез 3-7 діб',
                        'Температура тіла\nчерез 14 діб',
                        'Противірусний препарат Х']
        Pwithvaccine = [0.37, 0.49, 0.52, 0.3]
        Pwithoutvaccine = [0.31, 0.4, 0.14, 0.43]
    elif number == 3:
        col_list_tem = ['Характер мокроти\nдо лікування',
                        'Характер мокроти\nчерез 3-7 діб',
                        'Характер мокроти\nчерез 14 діб',
                        'Противірусний препарат Х']

    elif number == 4:
        col_list_tem = ['Локалізація НП\nдо лікування',
                        'Локалізація НП\nчерез 3-7 діб',
                        'Локалізація НП\nчерез 14 діб',
                        'Противірусний препарат Х']

    elif number == 5:
        col_list_tem = ['Поширенність процесу\nдо лікування',
                        'Поширенність процесу\nчерез 3-7 діб',
                        'Поширенність процесу\nчерез 14 діб',
                        'Противірусний препарат Х']

    elif number == 6:
        col_list_tem = ['Рентгенодинаміка\nдо лікування',
                        'Рентгенодинаміка\nчерез 3-7 діб',
                        'Рентгенодинаміка\nчерез 14 діб',
                        'Противірусний препарат Х']

    elif number == 7:
        col_list_tem = ['Рівень ШОЕ\nдо лікування',
                        'Рівень ШОЕ\nчерез 3-7 діб',
                        'Рівень ШОЕ\nчерез 14 діб',
                        'Противірусний препарат Х']

    elif number == 8:
        col_list_tem = ['Загальний стан хворого\nдо лікування',
                        'Загальний стан хворого\nчерез 3-7 діб',
                        'Загальний стан хворого\nчерез 14 діб',
                        'Противірусний препарат Х']
        
    df_tem = df[col_list_tem]
    return df_tem, Pwithvaccine, Pwithoutvaccine

def ArrayTemperature(data_tem):
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
    for i in range(0, 3):
        for j in range(0, 3):
            Stan_tem[i][j] = Stan_tem[i][j]/len(data_tem)

    return np.asarray(Stan_tem)

def ArrayParameter(data_tem):

    massive_unique = np.sort(pd.Series(data_tem.values.ravel()).unique())
    CountElements = massive_unique.size
    Stan_tem = np.zeros((CountElements, CountElements))
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

# def equations(p):
#     # Stan0 = np.asarray([Stans[k][0] for k in range(0, len(Stans))])
#     # Stan1 = np.asarray([Stans[k][1] for k in range(0, len(Stans))])
#     Stan0 = [0.84, 0.13, 0.03]
#     Stan1 = [0.13, 0.24, 0.63]
#     x, y = p
#     return (Stan0[0]*pow(1-x,5) - Stan1[0], Stan0[0]*(x*(pow(x-1,4)+(y-1)*(pow(x,3)+(y-4)*pow(x,2)+(pow(y,2)-4*y+6)*x+pow(y,3)-4*pow(y,2)+6*y-4))) + Stan0[1]*pow(1-y,5) - Stan1[1],
#             -Stan0[0]*x*y*(pow(x,3)+(y-5)*pow(x,2)+(pow(y,2)-5*y+10)*x+pow(y,3)-5*pow(y,2)+10*y-10) + Stan0[1]*y*(pow(y,4)-5*pow(y,3)+10*pow(y,2)-10*y+5)+Stan0[2] - Stan1[2])

def ProbabilityMatrix(Stans):
    Stan0 = np.asarray([Stans[k][0] for k in range(0, len(Stans))])
    Stan1 = np.asarray([Stans[k][1] for k in range(0, len(Stans))])
    # print(Stan0)
    # print(Stan1)

    # x, y = fsolve(equations)
    # print(equations((x, y)))

    # print(Stan0.transpose())
    # print(Stan1.transpose())
    # print(np.linalg.solve(Stan0.transpose(), Stan1))

    matrix1 = np.zeros((3, 3))
    matrix2 = np.zeros((3, 3))

    return matrix1, matrix2



def FunctionCalculationCurves(stans, flag, massive_unique, p):
    #with vaccine
    if flag == 1:
        # loop1 = np.asarray([[0.63, 0, 0],
        #                     [0.37, 0.51, 0],
        #                     [0, 0.49, 1]])
        # loop2 = np.asarray([[0.48, 0, 0],
        #                     [0.52, 0.7, 0],
        #                     [0, 0.3, 1]])
        loop1 = np.asarray([[1-p[0], 0, 0],
                            [p[0], 1-p[1], 0],
                            [0, p[1], 1]])
        loop2 = np.asarray([[1-p[2], 0, 0],
                            [p[2], 1-p[3], 0],
                            [0, p[3], 1]])
    elif flag == 0:
    #without vaccine
        # loop1 = np.asarray([[0.69, 0, 0],
        #                     [0.31, 0.6, 0],
        #                     [0, 0.4, 1]])
        # loop2 = np.asarray([[0.86, 0, 0],
        #                     [0.14, 0.57, 0],
        #                     [0, 0.43, 1]])
        loop1 = np.asarray([[1-p[0], 0, 0],
                            [p[0], 1-p[1], 0],
                            [0, p[1], 1]])
        loop2 = np.asarray([[1-p[2], 0, 0],
                            [p[2], 1-p[3], 0],
                            [0, p[3], 1]])

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
    #ProbMatr_firstloop, ProbMatr_secondloop = ProbabilityMatrix(Vectors)

    Y, X = FunctionCalculationCurves(Vectors, number, massive_unique, p)

    for i in range(0, massive_unique.size):
        VisualizationCurve([Y[i], X])
    plt.show()

def main():
    buildingcurvesfromprobably()

if __name__ == '__main__':
    main()