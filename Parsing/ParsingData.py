import pandas as pd

def pars():

    xls_file = pd.ExcelFile('/home/yaroslav/Projects/Python/Medical_models/Survival-analysis/Analysis/Data.xlsx')
    df = xls_file.parse('Вибірка 1')
    # value = int(input("вік "))
    # print(df.head())
    col_list = ['Вікова група', 'Температура тіла\nдо лікування', 'Характер мокроти\nдо лікування',
                'Загальний стан хворого\nдо лікування',
                'Локалізація НП\nдо лікування', 'Рентгенодинаміка\nдо лікування',
                'Вірусний агент']
    df = df[col_list]

    df = df[df['Вікова група'] == 1]

    return df

