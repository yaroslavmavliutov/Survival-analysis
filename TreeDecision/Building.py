from Parsing.ParsingData import pars

from sklearn.tree import *
from sklearn.cross_validation import train_test_split
from subprocess import call

def main():
    dataset = pars()
    y = (dataset['Вірусний агент']).as_matrix()
    del dataset['Вірусний агент']
    X = dataset.as_matrix()

    # ДЕРЕВО

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

    clf_gini = DecisionTreeClassifier(criterion="gini",
                                       min_samples_leaf=1,
                                       max_depth=None,
                                       max_features=None, max_leaf_nodes=None,
                                       min_impurity_split=1e-07,
                                       min_samples_split=2, min_weight_fraction_leaf=0.0,
                                       presort=False, random_state=None, splitter='best')
    clf_gini = clf_gini.fit(X_train, y_train)

    export_graphviz(clf_gini.tree_, out_file='tree.dot', feature_names=['x[0]', 'x[1]', 'x[2]', 'x[3]', 'x[4]', 'x[5]', 'x[6]', 'x[7]'])
    call(['dot', '-T', 'png', 'tree.dot', '-o', 'tree.png'])




if __name__ == '__main__':
    main()