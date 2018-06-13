from Parsing.ParsingData import *
from sklearn.tree import *
import matplotlib.pyplot as plt
import numpy as np

def predict(data):
    dataset = pars()
    y = (dataset['Вірусний агент']).as_matrix()
    del dataset['Вірусний агент']
    X = dataset.as_matrix()

    clf = DecisionTreeClassifier()
    clf = clf.fit(X, y)

    if float(data[0]) < 30:
        age = 1
    elif float(data[0]) >= 30 and float(data[0]) < 60:
        age = 2
    else:
        age = 3

    if float(data[1]) < 37:
        temp = 1
    elif float(data[1]) >= 37 and float(data[1]) < 38:
        temp = 1
    else:
        temp = 2

    if data[2] == 'Відсутнє':
        mokr = 0
    elif data[2] == 'Слизове':
        mokr = 1
    elif data[2] == 'Слизово-гнійне':
        mokr = 2
    else:
        mokr = 3

    if data[3] == 'Відсутня':
        lok = 0
    elif data[3] == 'Однобічна':
        lok = 1
    else:
        lok = 2

    if data[4] == 'Повне розсмоктування':
        rent = 1
    elif data[4] == 'Часткове розсмоктування':
        rent = 2
    elif data[4] == 'Динаміка відсутня':
        rent = 3
    else:
        rent = 4

    if data[5] == 'Стабільний':
        zag = 1
    elif data[5] == 'Середньої важкості':
        zag = 2
    else:
        zag = 3

    p = clf.predict_proba([[age, temp, mokr, zag, lok, rent]])[0]

    x = p.tolist()
    plt.bar(np.arange(len(x)), height=x)
    plt.xticks(np.arange(len(x)), ('Немає', 'Метапнев', 'Парагрип', 'Рино', 'Адено', 'Корона'))
    plt.ylabel('Ймовірність')
    plt.xlabel('Вірусний агент')
    plt.title('Прогнозування вірусного агента')
    plt.show()

def main():
    predict()

if __name__ == '__main__':
    main()