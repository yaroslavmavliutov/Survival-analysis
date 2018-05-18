import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wolframalpha as wf
import re

def pars(number):

    xls_file = pd.ExcelFile('/home/yaroslav/Projects/Python/Medical_models/Survival-analysis/Data.xlsx')
    df = xls_file.parse('Вибірка 1')
    if number == 2:
        #3x3
        col_list_tem = ['Температура тіла\nдо лікування',
                        'Температура тіла\nчерез 3-7 діб',
                        'Температура тіла\nчерез 14 діб',
                        'Противірусний препарат Х']
    elif number == 3:
        #4x4
        col_list_tem = ['Характер мокроти\nдо лікування',
                        'Характер мокроти\nчерез 3-7 діб',
                        'Характер мокроти\nчерез 14 діб',
                        'Противірусний препарат Х']

    elif number == 4:
        #3x3
        col_list_tem = ['Локалізація НП\nдо лікування',
                        'Локалізація НП\nчерез 3-7 діб',
                        'Локалізація НП\nчерез 14 діб',
                        'Противірусний препарат Х']


    elif number == 5:
        #3x3
        col_list_tem = ['Рентгенодинаміка\nдо лікування',
                        'Рентгенодинаміка\nчерез 3-7 діб',
                        'Рентгенодинаміка\nчерез 14 діб',
                        'Противірусний препарат Х']

    elif number == 6:
        #3x3
        col_list_tem = ['Загальний стан хворого\nдо лікування',
                        'Загальний стан хворого\nчерез 3-7 діб',
                        'Загальний стан хворого\nчерез 14 діб',
                        'Противірусний препарат Х']

    df_tem = df[col_list_tem]
    return df_tem, number


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

def FindTransitionMatrix_P(stan):

    client = wf.Client("YLJ24P-8TRXGTQA9H")  # app_ID is the app id

    first_loop = "({{1-x, 0, 0}, {x, 1-y, 0}, {0, y, 1}}^5)*{{" + str(stan.transpose()[0][0]) + "}, {" + str(stan.transpose()[0][1]) + \
    "}, {" + str(stan.transpose()[0][2]) + "}}= {{" + str(stan.transpose()[1][0]) +"}, {"+ str(stan.transpose()[1][1]) + "}, {" + str(stan.transpose()[1][2]) + \
    "}}"
    res_first = client.query(first_loop)
    answer_first = next(res_first.results).text
    ans1 = re.findall(r'\d+[.]\d+|\d+', answer_first)

    sec_loop = "({{1-x, 0, 0}, {x, 1-y, 0}, {0, y, 1}}^5)*{{" + str(stan.transpose()[1][0]) + "}, {" + str(
        stan.transpose()[1][1]) + \
                 "}, {" + str(stan.transpose()[1][2]) + "}}= {{" + str(stan.transpose()[2][0]) + "}, {" + str(
        stan.transpose()[2][1]) + "}, {" + str(stan.transpose()[2][2]) + \
                 "}}"
    res_sec = client.query(sec_loop)
    answer_sec = next(res_sec.results).text
    ans2 = re.findall(r'\d+[.]\d+|\d+', answer_sec)
    return [[float(ans1[0]), float(ans1[1])], [float(ans2[0]), float(ans2[1])]]

def FunctionCalculationCurves(stans, massive_unique):

    p = FindTransitionMatrix_P(stans)

    if len(massive_unique) == 3:

        loop1 = np.asarray([[1-p[0][0], 0, 0],
                            [p[0][0], 1-p[0][1], 0],
                            [0, p[0][1], 1]])
        loop2 = np.asarray([[1-p[1][0], 0, 0],
                            [p[1][0], 1-p[1][1], 0],
                            [0, p[1][1], 1]])

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

def VisualizationCurve(mass, num, count, number):
    #name = 'degree' + str(num)
    stan = [['>38°C', '37-38°C', '<37°C'],
            ['слизово-гнійне мокротіння', 'слизове мокротіння', 'мокротіння нема'],
            ['сегментна локалізація', 'часткова локалізація', 'локалізація відсутня'],
            ['без динаміки', 'часткове розсмоктування', 'повне розсмоктування'],
            ['важкий стан', 'стан середньої важкості', 'стабільний стан']]
    name = stan[count-2][num]
    if number == 0:
        plt.figure(1)
        plt.title('Криві виживання із врахуванням ПП')
        plt.xlabel('Дні госпіталізації')
        plt.ylabel('Ймовірність стану')
        plt.plot(mass[1], mass[0], label=name)
        plt.legend(loc='upper right')
        plt.grid(True)
    elif number == 1:
        plt.figure(2)
        plt.title('Криві виживання без врахуванням ПП')
        plt.xlabel('Дні госпіталізації')
        plt.ylabel('Ймовірність стану')
        plt.plot(mass[1], mass[0], label=name)
        plt.legend(loc='upper right')
        plt.grid(True)


def buildingcurvesfromprobably(number):
    data_tem, count = pars(number)
    #number = int(input("Пацієнти з противірусним - 0, без - 1: "))
    for number in range(0, 2):
        if number == 0:
            Data = data_tem[(data_tem['Противірусний препарат Х'] == 1)]
            s = 'З противірусним апаратом'
        elif number == 1:
            Data = data_tem[(data_tem['Противірусний препарат Х'] == 0)]
            s = 'Без противірусного апарату'

        Vectors, massive_unique = ArrayParameter(Data)
        print(s)
        print(massive_unique)
        print(Vectors)


        Y, X = FunctionCalculationCurves(Vectors, massive_unique)

        for i in range(0, massive_unique.size):
            VisualizationCurve([Y[i], X], i, count, number)

    plt.show()

def main():

    buildingcurvesfromprobably()

if __name__ == '__main__':
    main()