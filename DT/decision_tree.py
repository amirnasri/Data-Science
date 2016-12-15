import numpy as np

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


    def gini_impurity(self, X, y):
        class_counts = decision_tree.counts(y, self.classes)
        n_classes = len(self.classes)
        for i, c in enumerate(class_counts):
            g += float(c)/n_classes * (m - c)



    def select_feature(self, X, y):
        gi = self.gini_impurity(X, y)
        for j in range(self.m):
            x = X[:, j]
            x_unique = np.unique(x)
            #TODO: check if improvement possible
            thresholds = np.linspace(x_unique.min(), x_unique.max(), self.max_step_split)

    def fit(self, X, y):
        self.m, self.n = X.shape
        self.classes = np.unique(y)
