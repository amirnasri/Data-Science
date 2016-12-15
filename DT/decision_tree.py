import numpy as np
import bisect
class decision_tree(object):
    def __init__(self, max_step_split = 5):
        self.max_step_split = max_step_split

    @staticmethod
    def asndarray(a):
        if isinstance(a, np.ndarray):
            return a
        return np.ndarray(a)

    @staticmethod
    def counts(a, values = None):
        values = decision_tree.asndarray(values)
        if values is None:
            values = np.unique(values)
        counts = np.zeros(values.shape)
        for index, v in np.ndenumerate(values):
            counts[index] = (v == a).sum()
        return counts


    def gini_impurity(X, y):
        classes = len(np.unique(y))
        class_counts = decision_tree.counts(y, classes).astype(float)
        n_classes = len(classes)
        return (class_counts/n_classes * (1 - class_counts/n_classes)).sum()

    @staticmethod
    def split(X, y, j, thresholds):
        m, n = X.shape
        indexes = map(lambda a: bisect.bisect_left(thresholds, a), X[:, j])
        for i in range(len(thresholds) + 1):
            sub_index = (i == indexes)
            yield X[sub_index, :], y[sub_index, :], prob

    def select_feature(self, X, y):
        gi = self.gini_impurity(X, y)
        for j in range(self.m):
            x = X[:, j]
            x_unique = np.unique(x)
            #TODO: check if improvement possible
            thresholds = np.linspace(x_unique.min(), x_unique.max(), self.max_step_split)
            gi_children = 0
            for Xc, yc, prob in decision_tree.split(X, y, j, thresholds):
                gi_children += prob * decision_tree.gini_impurity(Xc, yc)
            gi_gain = gi - gi_children


    def fit(self, X, y):
        self.m, self.n = X.shape
        self.classes = np.unique(y)
        self.n_classes = len(self.classes)
