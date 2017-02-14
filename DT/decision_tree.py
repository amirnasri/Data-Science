import numpy as np
import bisect

class Node:
    def __init__(self):
        self.feature = None
        self.threshold = None
        self.left = None
        self.right = None

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
        if values is None:
            values = np.unique(a)
        else:
            values = decision_tree.asndarray(values)
        counts = np.zeros(values.shape)
        for index, v in np.ndenumerate(values):
            counts[index] = (v == a).sum()
        return counts

    @staticmethod
    def gini_impurity(y):
        m = len(y)
        classes = np.unique(y)
        class_counts = decision_tree.counts(y, classes).astype(float)
        n_classes = len(classes)
        return (class_counts/m * (1 - class_counts/m)).sum()

    @staticmethod
    def get_splits(x, thresholds):
        for i, t in enumerate(thresholds):
            le_index = np.where(x <= t)
            g_index = np.where(x > t)
            yield le_index, g_index
        '''
        indexes = map(lambda a: bisect.bisect_left(thresholds, a), X[:, j])
        for i in range(len(thresholds) + 1):
            sub_index = (i < indexes)
            prob = sub_index.mean()
            yield X[sub_index, :], y[sub_index, :], prob
        '''

    '''
        Iterate through the features and find the one
        that has a split leading to the maximum Gini impurity
        gain.

        Returns: tuple
            Tuple of best feature index and best split threshold for that feature.

    '''

    def select_feature(self, X, y):
        #gi = self.gini_impurity(X, y)
        m, n = X.shape
        # Gini impurities for best splits on the n features
        gi_gain_threshold = np.zeros((n, 2))
        # Arrays of threshold vectors for the n features
        thresholds_vec = np.zeros((n,), dtype=np.object)
        for j in range(n):
            x = X[:, j]
            x_unique = np.unique(x)
            #TODO: check if improvement possible
            thresholds = np.linspace(x_unique.min(), x_unique.max(), self.max_step_split)
            thresholds_vec[j] = thresholds
            gi_gain_splits = np.zeros(thresholds.shape)
            for k, (le_index, g_index) in enumerate(decision_tree.get_splits(x, thresholds)):
                gi_gain_splits[k] = float(len(le_index))/m * decision_tree.gini_impurity(y[le_index]) \
                            + float(len(g_index))/m * decision_tree.gini_impurity(y[g_index])
            index_best = np.argmin(gi_gain_splits)
            gi_gain_threshold[j, :] = [gi_gain_splits[index_best], thresholds[index_best]]
        print gi_gain_threshold
        j_best = np.argmin(gi_gain_threshold[:, 0])
        return j_best, gi_gain_threshold[j_best, 1]

    def build_tree(self, root, X, y):
        if len(np.unique(y)) == 1:
            root.is_leaf = True
            root.class_ = np.unique(y)[0]
            return

        j, threshold = self.select_feature(X, y)
        print j
        root.feature = j
        root.threshold = threshold
        x = X[:, j]
        le_index = np.where(x <= threshold)
        g_index = np.where(x > threshold)
        print le_index, g_index
        if len(le_index) > 0:
            X_left, y_left = X[le_index], y[le_index]
            left = Node()
            self.build_tree(left, X_left, y_left)
        if len(g_index) > 0:
            X_right, y_right = X[g_index], y[g_index]
            right = Node()
            self.build_tree(right, X_right, y_right)

    def fit(self, X, y):
        self.classes = np.unique(y)
        self.n_classes = len(self.classes)
        self.root = Node()
        self.build_tree(self.root, X, y)

if __name__ == '__main__':
    dt = decision_tree()
    m, n = 5, 4
    X = np.random.rand(m, n)
    y = np.random.randint(2, size=(m, ))
    #print dt.select_feature(X, y)
    print X
    print y
    dt.fit(X, y)