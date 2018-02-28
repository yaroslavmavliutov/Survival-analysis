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

def FunctionCalculationCurves(stans, flag):
    #with vaccine
    if flag == 1:
        loop1 = np.asarray([[0.63, 0, 0],
                            [0.37, 0.51, 0],
                            [0, 0.49, 1]])
        loop2 = np.asarray([[0.48, 0, 0],
                            [0.52, 0.7, 0],
                            [0, 0.3, 1]])
    elif flag == 0:
    #without vaccine
        loop1 = np.asarray([[0.69, 0, 0],
                            [0.31, 0.6, 0],
                            [0, 0.4, 1]])
        loop2 = np.asarray([[0.86, 0, 0],
                            [0.14, 0.57, 0],
                            [0, 0.43, 1]])

    # [1, 5, 14]
    Data = stans.transpose()[0]

    for i in range(2, 5):
        Data = np.append(Data, np.dot(np.linalg.matrix_power(loop1, i), stans.transpose()[0]))

    Data = np.append(Data, stans.transpose()[1])

    for j in range(6, 14):
        Data = np.append(Data, np.dot(np.linalg.matrix_power(loop2, j), stans.transpose()[1]))

    #Data = np.append(Data, stans.transpose()[2])

    Data = Data.reshape(13, 3)

    first_prob = []
    second_prob = []
    third_prob = []
    for i in range(0, 13):
        first_prob.append(Data[i][0])
        second_prob.append(Data[i][1])
        third_prob.append(Data[i][2])
    return [first_prob, second_prob, third_prob], [i for i in range(0, 13)]

def VisualizationCurve(mass):
    plt.figure(1)
    plt.plot(mass[1], mass[0], label='rate')
    plt.legend(loc='upper left')
    plt.grid(True)

def buildingcurvesfromprobably():
    data_tem = pars()
    Temperature_with_vaccine = data_tem[(data_tem['Противірусний препарат Х'] == 1)]
    Temperature_without_vaccine = data_tem[(data_tem['Противірусний препарат Х'] == 0)]


    Matrix = ArrayTemperature(Temperature_without_vaccine)
    Y, X = FunctionCalculationCurves(Matrix, 0)
    for i in range(0, 3):
        VisualizationCurve([Y[i], X])
    plt.show()

def main():
    buildingcurvesfromprobably()

if __name__ == '__main__':
    main()