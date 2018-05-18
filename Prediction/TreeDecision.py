from Parsing.ParsingData import *
from sklearn.metrics import *
from sklearn.tree import *
from sklearn.cross_validation import train_test_split

def main():
    dataset = pars()
    y = (dataset['Вірусний агент']).as_matrix()
    del dataset['Вірусний агент']
    X = dataset.as_matrix()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    # Decision Tree Classifier with criterion gini index
    clf_gini = DecisionTreeClassifier(criterion="gini",
                                       min_samples_leaf=1,
                                       max_depth=None,
                                       max_features=None, max_leaf_nodes=None,
                                       min_impurity_split=1e-07,
                                       min_samples_split=2, min_weight_fraction_leaf=0.0,
                                       presort=False, random_state=None, splitter='best')
    clf_gini = clf_gini.fit(X_train, y_train)

    # ПРОГНОЗУЮ

    print('gini ', clf_gini.predict([[1, 2, 1, 1, 2, 5, 8, 10]]))

    y_pred = clf_gini.predict(X_test)
    print("Accuracy is ", accuracy_score(y_test, y_pred) * 100)



if __name__ == '__main__':
    main()