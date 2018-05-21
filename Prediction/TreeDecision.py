from Parsing.ParsingData import *
from sklearn.tree import *
import matplotlib.pyplot as plt
import numpy as np

def predict():
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

    age = input('Вікова група(1: 18-30, 2: 31-60, 3: >61): ')
    temp = input('Температура(0: <37°C, 1: 37-38°C, 3: >38°C): ')
    mokrora = input('Характер мокроти(0: нема, 1: слизова, 2: слизово-гнійна, 3: гнійна): ')
    zagaln = input('Загальний стан(1: задовільний, 2: середній, 3: важкий): ')
    lokal = input('Локалізація(0: нема, 1: однобічна, 2: двобічна): ')
    rentgen = input('Рентгенодинаміка(1: повне розсмоктування, 2: часткове, 3: без динаміки, 4: від\'ємна динаміка): ')

    p = clf.predict_proba([[age, temp, mokrora, zagaln, lokal, rentgen]])[0]

    x = p.tolist()
    plt.bar(np.arange(len(x)), height=x)
    plt.xticks(np.arange(len(x)), ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))
    plt.ylabel('Ймовірність')
    plt.xlabel('Вірусний агент')
    plt.title('Прогнозування вірусного агента')
    plt.show()

def main():
    predict()

if __name__ == '__main__':
    main()