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

    p = clf.predict_proba([[data[0], data[1], data[2], data[5], data[3], data[4]]])[0]

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