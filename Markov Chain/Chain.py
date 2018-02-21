import pandas as pd
import numpy as np

def pars():

    xls_file = pd.ExcelFile('/home/yaroslav/Projects/Python/Medical_models/Survival-analysis/Data.xlsx')
    df = xls_file.parse('Вибірка 1')
    col_list_tem = ['Температура тіла\nдо лікування',
                    'Температура тіла\nчерез 3-7 діб',
                    'Температура тіла\nчерез 14 діб']
    col_list_all = ['Загальний стан хворого\nдо лікування',
                    'Загальний стан хворого\nчерез 3-7 діб',
                    'Загальний стан хворого\nчерез 14 діб']
    df_tem = df[col_list_tem]
    df_all = df[col_list_all]
    return df_tem, df_all

def main():
    data_tem, data_all = pars()


    Array_probability_all_first = np.zeros((2, 2))
    Array_probability_all_second = np.zeros((2, 2))

    Stan1_all_first = np.zeros((2, 1))
    Stan2_all_first = np.zeros((2, 1))
    Stan2_all_second = np.zeros((2, 1))
    for element in range(66, len(data_all)): # 66

        # 0 день
        if data_all.iloc[element][0] == 1:
            Stan1_all_first[1][0] = Stan1_all_first[1][0] + 1
        if data_all.iloc[element][0] == 2 or data_all.iloc[element][0] == 3:
            Stan1_all_first[0][0] = Stan1_all_first[0][0] + 1

        # 5 день
        if data_all.iloc[element][1] == 1:
            Stan2_all_first[1][0] = Stan2_all_first[1][0] + 1
        if data_all.iloc[element][1] == 2 or data_all.iloc[element][1] == 3:
            Stan2_all_first[0][0] = Stan2_all_first[0][0] + 1

        # 14 день
        if data_all.iloc[element][2] == 1:
            Stan2_all_second[1][0] = Stan2_all_second[1][0] + 1
        if data_all.iloc[element][2] == 2 or data_all.iloc[element][2] == 3:
            Stan2_all_second[0][0] = Stan2_all_second[0][0] + 1

    print(Stan1_all_first)
    print(Stan2_all_first)
    print(Stan2_all_second)


    Array_probability_tem_first = np.zeros((3, 3))
    Array_probability_tem_second = np.zeros((3, 3))

    Stan1_tem_first = np.zeros((3, 1))
    Stan2_tem_first = np.zeros((3, 1))
    Stan2_tem_second = np.zeros((3, 1))
    for element in range(66, len(data_all)):

        # 0 день
        if data_tem.iloc[element][0] == 0:
            Stan1_tem_first[2][0] = Stan1_tem_first[2][0] + 1
        if data_tem.iloc[element][0] == 1:
            Stan1_tem_first[1][0] = Stan1_tem_first[1][0] + 1
        if data_tem.iloc[element][0] == 2:
            Stan1_tem_first[0][0] = Stan1_tem_first[0][0] + 1

        # 5 день
        if data_tem.iloc[element][1] == 0:
            Stan2_tem_first[2][0] = Stan2_tem_first[2][0] + 1
        if data_tem.iloc[element][1] == 1:
            Stan2_tem_first[1][0] = Stan2_tem_first[1][0] + 1
        if data_tem.iloc[element][1] == 2:
            Stan2_tem_first[0][0] = Stan2_tem_first[0][0] + 1

        # 14 день
        if data_tem.iloc[element][2] == 0:
            Stan2_tem_second[2][0] = Stan2_tem_second[2][0] + 1
        if data_tem.iloc[element][2] == 1:
            Stan2_tem_second[1][0] = Stan2_tem_second[1][0] + 1
        if data_tem.iloc[element][2] == 2:
            Stan2_tem_second[0][0] = Stan2_tem_second[0][0] + 1
    print(Stan1_tem_first)
    print(Stan2_tem_first)
    print(Stan2_tem_second)

if __name__ == '__main__':
    main()