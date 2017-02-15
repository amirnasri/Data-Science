import abc

class BaseClassifier(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fit(self, X, y):
        """
        Fit the classifier to data provided in X and y
        :param X: array-like of shape (m, n)
            Array of m data samples each containing n features.
        :param y: array-like of shape (m,)
            Array of target class values for the m data samples.
        """
        return

    @abc.abstractmethod
    def predict_proba(self, X):
        """
        Fit the classifier to data provided in X and y
        :param X: array-like of shape (m, n)
            Array of m data samples each containing n features.
        :return: array-like of shape (m,)
            Array of class probabilities.
        """
        return