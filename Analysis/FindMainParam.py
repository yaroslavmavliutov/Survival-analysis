from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from Parsing.ParsingData import pars
from sklearn.linear_model import LogisticRegression

def main():
    dataset = pars()
    y = (dataset['Вірусний агент']).as_matrix()
    del dataset['Вірусний агент']
    X = dataset.as_matrix()

    model = ExtraTreesClassifier()
    model.fit(X, y)
    #display the relative importance of each attribute
    print(model.feature_importances_)

    model = LogisticRegression()
    #create the RFE model and select 3 attributes
    rfe = RFE(model, 3)
    rfe = rfe.fit(X, y)
    #summarize the selection of the attributes
    print(rfe.support_)
    print(rfe.ranking_)
    for i in range(len(dataset.columns.values)):
        if rfe.ranking_[i] == True:
            print(' :', dataset.columns.values[i])


if __name__ == '__main__':
    main()