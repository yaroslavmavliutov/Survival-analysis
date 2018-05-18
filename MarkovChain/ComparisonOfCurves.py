import matplotlib.pyplot as plt
from MarkovChain.BuildingChain import *

def VisualizationCurve(mass, num, count, number):
    #name = 'degree' + str(num)
    stan = [['>38°C', '37-38°C', '<37°C'],
            ['слизово-гнійне мокротіння', 'слизове мокротіння', 'мокротіння нема'],
            ['сегментна локалізація', 'часткова локалізація', 'локалізація відсутня'],
            ['без динаміки', 'часткове розсмоктування', 'повне розсмоктування'],
            ['важкий стан', 'стан середньої важкості', 'стабільний стан']]
    if number == 0:
        name = stan[count - 2][num] + '. Без противірусного препарату'
    elif number == 1:
        name = stan[count - 2][num] + '. З противірусним препаратом'
    plt.figure(num)
    plt.title('Криві виживання')
    plt.xlabel('Дні госпіталізації')
    plt.ylabel('Ймовірність стану')
    plt.plot(mass[1], mass[0], label=name)
    plt.legend(loc='upper right')
    plt.grid(True)


def comparisonbuildingcurves(number):
    data_tem, count = pars(number)

    #[[without], [with]]
    Data = []
    Data.append(data_tem[(data_tem['Противірусний препарат Х'] == 0)])
    Data.append(data_tem[(data_tem['Противірусний препарат Х'] == 1)])

    for index, data in enumerate(Data):
        Vectors, massive_unique = ArrayParameter(data)
        try: Vectors.transpose()[0] = first_stan
        except: pass
        Y, X = FunctionCalculationCurves(Vectors, massive_unique)
        for i in range(0, massive_unique.size):
            VisualizationCurve([Y[i], X], i, count, index)
        first_stan = Vectors.transpose()[0]

    plt.show()

def main():
    print('2 - Криві температури, 3 - Характеру мокроти, '
          '4 - Локалізація НП, 5 - Рентгенодинаміка, 6 - Загальний стан')
    num = int(input("number: "))
    try:
        comparisonbuildingcurves(num)
    except:
        pass

if __name__ == '__main__':
    main()