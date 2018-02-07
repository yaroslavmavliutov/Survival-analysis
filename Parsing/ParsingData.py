import pandas as pd

def pars():

    xls_file = pd.ExcelFile('/home/yaroslav/Projects/Python/Medical_models/Survival-analysis/Data.xlsx')
    df = xls_file.parse('Вибірка 1')
    # value = int(input("вік "))
    # print(df.head())
    col_list = ['Вікова група', 'Температура тіла\nдо лікування', 'Характер мокроти\nдо лікування',
                'Поширенність процесу\nдо лікування', 'Загальний стан хворого\nдо лікування',
                'Рівень лейкоцитів\nдо лікування', 'Лейкоцитарні зміни\nдо лікування',
                'Рівень ШОЕ\nдо лікування', 'Вірусний агент']
    df = df[col_list]
    return df

