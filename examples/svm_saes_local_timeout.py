from __future__ import division, print_function, with_statement

from sklearn import svm
from sklearn import datasets
from sklearn import cross_validation

from orges.core import param
from orges.core.main import optimize
from orges.optimizer.saes import SAESOptimizer
from orges.plugins.print import PrintPlugin


@param.float("C", interval=[0.1, 100])
@param.float("gamma", interval=[0, 100])
def f(C, gamma):
    iris = datasets.load_iris()

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        iris.data, iris.target, test_size=0.4, random_state=0)

    clf = svm.SVC(C=C, gamma=gamma)

    clf.fit(X_train, y_train)

    return -clf.score(X_test, y_test)


if __name__ == '__main__':
    print(optimize(f, timeout=5, optimizer=SAESOptimizer(),
                   plugins=[PrintPlugin()]))