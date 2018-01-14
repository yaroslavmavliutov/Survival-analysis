# from sklearn import tree
# from sklearn.datasets import load_iris
# import graphviz


import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
import graphviz

def main():
    # iris = load_iris()
    # print(iris)
    # clf = tree.DecisionTreeClassifier()
    # clf = clf.fit(iris.data, iris.target)
    # dot_data = tree.export_graphviz(clf, out_file=None)
    # graph = graphviz.Source(dot_data)
    # graph.render("iris")
    # dot_data = tree.export_graphviz(clf, out_file=None,
    #                                 feature_names=iris.feature_names,
    #                                 class_names=iris.target_names,
    #                                 filled=True, rounded=True,
    #                                 special_characters=True)
    # graph = graphviz.Source(dot_data)


    balance_data = pd.read_csv(
        'https://archive.ics.uci.edu/ml/machine-learning-databases/balance-scale/balance-scale.data',
        sep=',', header=None)

    X = balance_data.values[:, 1:5]
    Y = balance_data.values[:, 0]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)


    # Decision Tree Classifier with criterion gini index
    clf_gini = DecisionTreeClassifier(criterion="gini", random_state=100,
                                      max_depth=3, min_samples_leaf=5)
    clf_gini = clf_gini.fit(X_train, y_train)
    dot_data = tree.export_graphviz(clf_gini, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("clf_gini")
    dot_data = tree.export_graphviz(clf_gini, out_file=None,
                                    filled=True, rounded=True,
                                    special_characters=True)

    # Decision Tree Classifier with criterion information gain
    clf_entropy = DecisionTreeClassifier(criterion="entropy", random_state=100,
                                         max_depth=3, min_samples_leaf=5)
    clf_entropy = clf_entropy.fit(X_train, y_train)
    dot_data = tree.export_graphviz(clf_entropy, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("clf_entropy")
    dot_data = tree.export_graphviz(clf_entropy, out_file=None,
                                    filled=True, rounded=True,
                                    special_characters=True)

    #print(clf_gini.predict([[4, 4, 3, 3]]))

    y_pred = clf_gini.predict(X_test)
    y_pred_en = clf_entropy.predict(X_test)









if __name__ == '__main__':
    main()



