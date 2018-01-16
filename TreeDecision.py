import numpy as np
import urllib.request
from sklearn import preprocessing
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from ParsingData import pars

from sklearn.metrics import *
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import *
from sklearn.cross_validation import train_test_split

import graphviz

def main():
    dataset = pars()
    y = (dataset['Вірусний агент']).as_matrix()
    del dataset['Вірусний агент']
    X = dataset.as_matrix()

    #model = ExtraTreesClassifier()
    #model.fit(X, y)
    # display the relative importance of each attribute
    #print(model.feature_importances_)

    #model = LogisticRegression()
    # create the RFE model and select 3 attributes
    #rfe = RFE(model, 3)
    #rfe = rfe.fit(X, y)
    # summarize the selection of the attributes
    #print(rfe.support_)
    #print(rfe.ranking_)

    #normalized_X = preprocessing.normalize(X)


    # fit a CART model to the data
    # model = DecisionTreeClassifier()
    # model = model.fit(X, y)
    # #print(model)
    # # make predictions
    # expected = y
    # predicted = model.predict(X)
    # # summarize the fit of the model
    # #print(metrics.classification_report(expected, predicted))
    # #print(metrics.confusion_matrix(expected, predicted))
    #
    # dot_data = export_graphviz(model, out_file=None)
    # graph = graphviz.Source(dot_data)
    # graph.render("bakteria")
    #
    # dot_data = export_graphviz(model, out_file=None,
    #                      feature_names=['a', 'b', 'c', 'd', 'e', 'r', 't', 'y'],
    #                      class_names=['0', '1', '2', '3', '4', '5', '6'],
    #                      filled=True, rounded=True,
    #                      special_characters=True)



    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
    #
    # # Decision Tree Classifier with criterion gini index
    clf_gini = DecisionTreeClassifier(criterion="gini",
                                       min_samples_leaf=1,
                                       max_depth=None,
                                       max_features=None, max_leaf_nodes=None,
                                       min_impurity_split=1e-07,
                                       min_samples_split=2, min_weight_fraction_leaf=0.0,
                                       presort=False, random_state=None, splitter='best')
    clf_gini = clf_gini.fit(X_train, y_train)
    dot_data = export_graphviz(clf_gini, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("clf_gini")
    # dot_data = export_graphviz(clf_gini, out_file=None,
    #                            feature_names=['a', 'b', 'c', 'd', 'e', 'r', 't', 'y'],
    #                            class_names=['0', '1', '2', '3', '4', '5', '6'],
    #                                 filled=True, rounded=True,
    #                                 special_characters=True)
    # Decision Tree Classifier with criterion information gain
    clf_entropy = DecisionTreeClassifier(criterion="entropy",
                                         min_samples_leaf=1,
                                         max_depth=None,
                                         max_features=None, max_leaf_nodes=None,
                                         min_impurity_split=1e-07,
                                         min_samples_split=2, min_weight_fraction_leaf=0.0,
                                         presort=False, random_state=None, splitter='best')
    clf_entropy = clf_entropy.fit(X_train, y_train)
    dot_data = export_graphviz(clf_entropy, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("clf_entropy")
    # dot_data = export_graphviz(clf_entropy, out_file=None,
    #                                 feature_names=['a', 'b', 'c', 'd', 'e', 'r', 't', 'y'],
    #                                 class_names=['0', '1', '2', '3', '4', '5', '6'],
    #                                 filled=True, rounded=True,
    #                                 special_characters=True)



    # ПРОГНОЗУЮ
    print(clf_gini.predict([[1, 2, 1, 1, 2, 5, 8, 10]]))

    y_pred = clf_gini.predict(X_test)
    y_pred_en = clf_entropy.predict(X_test)

    print("Accuracy is ", accuracy_score(y_test, y_pred) * 100)

    from subprocess import call

    export_graphviz(clf_gini.tree_, out_file='tree.dot', feature_names=['a', 'b', 'c', 'd', 'e', 'r', 't', 'y'])
    call(['dot', '-T', 'png', 'tree.dot', '-o', 'tree.png'])




if __name__ == '__main__':
    main()