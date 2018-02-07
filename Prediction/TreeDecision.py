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
    #dot_data = export_graphviz(clf_gini, out_file=None)
    #graph = graphviz.Source(dot_data)
    #graph.render("clf_gini")
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
    #dot_data = export_graphviz(clf_entropy, out_file=None)
    #graph = graphviz.Source(dot_data)
    #graph.render("clf_entropy")
    # dot_data = export_graphviz(clf_entropy, out_file=None,
    #                                 feature_names=['a', 'b', 'c', 'd', 'e', 'r', 't', 'y'],
    #                                 class_names=['0', '1', '2', '3', '4', '5', '6'],
    #                                 filled=True, rounded=True,
    #                                 special_characters=True)



    # ПРОГНОЗУЮ

    print('gini ', clf_gini.predict([[1, 2, 1, 1, 2, 5, 8, 10]]))
    print('entropy ', clf_entropy.predict([[1, 2, 1, 1, 2, 5, 8, 10]]))

    y_pred = clf_gini.predict(X_test)
    y_pred_en = clf_entropy.predict(X_test)

    print("gini Accuracy is ", accuracy_score(y_test, y_pred) * 100)
    print("entropy Accuracy is ", accuracy_score(y_test, y_pred_en) * 100)



if __name__ == '__main__':
    main()