from Parsing.ParsingData import *
from sklearn.tree import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    dataset = pars()
    y = (dataset['Вірусний агент']).as_matrix()
    del dataset['Вірусний агент']
    X = dataset.as_matrix()

    clf = DecisionTreeClassifier()
    clf = clf.fit(X, y)

    # ПРОГНОЗУЮ
    # ['Вікова група', 'Температура тіла\nдо лікування', 'Характер мокроти\nдо лікування',
    #  'Загальний стан хворого\nдо лікування',
    #  'Локалізація НП\nдо лікування', 'Рентгенодинаміка\nдо лікування']

    p = clf.predict_proba([[2, 1, 1, 1, 1, 3]])[0]

    x = p.tolist()
    plt.bar(np.arange(len(x)), height=x)
    plt.xticks(np.arange(len(x)), ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
    plt.ylabel('Ймовірність')
    plt.xlabel('Вірусний агент')
    plt.title('Прогнозування вірусного агента')
    plt.show()

if __name__ == '__main__':
    main()