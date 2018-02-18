import pandas as pd
import numpy as np

def pars():

    xls_file = pd.ExcelFile('/home/yaroslav/Projects/Python/Medical_models/Survival-analysis/Data.xlsx')
    df = xls_file.parse('Вибірка 1')
    col_list = ['Загальний стан хворого\nдо лікування',
                'Загальний стан хворого\nчерез 3-7 діб']
    df = df[col_list]
    return df

def main():
    data = pars()
    Array_probability1 = np.zeros((3, 3))
    for element in range(0, len(data)):
            if data.iloc[element][0] == 1 and data.iloc[element][1] == 1:
                Array_probability1[0][0] = Array_probability1[0][0] + 1
            if data.iloc[element][0] == 1 and data.iloc[element][1] == 2:
                Array_probability1[0][1] = Array_probability1[0][1] + 1
            if data.iloc[element][0] == 1 and data.iloc[element][1] == 3:
                Array_probability1[0][2] = Array_probability1[0][2] + 1
            if data.iloc[element][0] == 2 and data.iloc[element][1] == 1:
                Array_probability1[1][0] = Array_probability1[1][0] + 1
            if data.iloc[element][0] == 2 and data.iloc[element][1] == 2:
                Array_probability1[1][1] = Array_probability1[1][1] + 1
            if data.iloc[element][0] == 2 and data.iloc[element][1] == 3:
                Array_probability1[1][2] = Array_probability1[1][2] + 1
            if data.iloc[element][0] == 3 and data.iloc[element][1] == 1:
                Array_probability1[2][0] = Array_probability1[2][0] + 1
            if data.iloc[element][0] == 3 and data.iloc[element][1] == 2:
                Array_probability1[2][1] = Array_probability1[2][1] + 1
            if data.iloc[element][0] == 3 and data.iloc[element][1] == 3:
                Array_probability1[2][2] = Array_probability1[2][2] + 1
    Array_probability1[0][0] = 1
    Array_probability1[0][1] = 0
    Array_probability1[0][2] = 0
    sum1 = Array_probability1[1][0] + Array_probability1[1][1] + Array_probability1[1][2]
    Array_probability1[1][0] = Array_probability1[1][0]/sum1
    Array_probability1[1][1] = Array_probability1[1][1]/sum1
    Array_probability1[1][2] = Array_probability1[1][2]/sum1
    sum2 = Array_probability1[2][0] + Array_probability1[2][1] + Array_probability1[2][2]
    Array_probability1[2][0] = Array_probability1[2][0]/sum2
    Array_probability1[2][1] = Array_probability1[2][1]/sum2
    Array_probability1[2][2] = Array_probability1[2][2]/sum2
    print(Array_probability1)
    print(np.linalg.matrix_power(Array_probability1, 2))
if __name__ == '__main__':
    main()