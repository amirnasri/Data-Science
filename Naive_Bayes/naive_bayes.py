import numpy as np
from sklearn.naive_bayes import BernoulliNB as BernoulliNB_SK
from sklearn.naive_bayes import MultinomialNB as MultinomialNB_SK
from sklearn.utils import check_random_state
import time
from utils import Utils

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('function %s finished in %2.2f seconds' % (method.__name__, te-ts))
        return result

    return timed

class MultinomialNB(object):
    def __init__(self, alpha=1):
        self.alpha = alpha

    def fit(self, X, y):
        X, y = Utils.check_fit_input(X, y, binary=True)
        m, n = X.shape

        Y = np.array([1 - y, y])

        # Calculate number of occurances for each feature for y={0, 1}
        # X_count is an array of shape (2, n) where aij is the number of
        # occurances for feature j given y=i.
        X_count = Y.dot(X)

        # Calculate total number of feature occurances for y={0, 1}
        # Y_count.shape = (2, )
        Y_count = Y.sum(axis=1).astype(np.float)

        X_count_smoothed = X_count + self.alpha
        Y_count_smoothed = Y_count + self.alpha

        Phi_X = np.diag(X_count_smoothed.sum(axis=1) ** -1).dot(X_count_smoothed)
        self.Phi_X_log = np.log(Phi_X)
        self.Phi_Y_log = np.log(Y_count_smoothed / Y_count_smoothed.sum())

    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis = 1)

    def predict_proba(self, X):
        # X.shape = (m, n), Phi_X_log.shape = (2, n)
        log_prob = X.dot(self.Phi_X_log.T) + self.Phi_Y_log

        # log probabilities above are not normalized but are
        # enough to make a decision regarding class of y.
        # But for some algorithms such as multi-class classifiers,
        # we need to provide the actual probabilities as well.
        # We use some numerical tricks since directly exponentiating
        # log_prob will lead to numerical problems.
        prob_diff = np.exp(log_prob[:, 0] - log_prob[:, 1])
        prob = np.zeros(log_prob.shape)
        prob[:, 0] = 1 / (1 + prob_diff ** -1)
        prob[:, 1] = 1 / (1 + prob_diff)
        return prob


class BernoulliNB(object):
    def __init__(self, alpha = 1):
        self.alpha = alpha

    @timeit
    def fit(self, X, y):
        X, y = Utils.check_fit_input(X, y, binary=True)
        m, n = X.shape

        Y = np.array([1 - y, y])
        # Calculate number of occurances for each feature for y={0, 1}
        # X_count is an array of shape (2, n) where aij is the number of
        # occurances for feature j given y=i.
        X_count = Y.dot(X)
        Y_count = Y.sum(axis=1).astype(np.float)

        X_count_smoothed = X_count + self.alpha
        Y_count_smoothed = Y_count + 2 * self.alpha

        Phi_X = np.diag(Y_count_smoothed**-1).dot(X_count_smoothed)

        self.Phi_X_y0_log = np.log(np.c_[1 - Phi_X[0, :], Phi_X[0, :]])
        self.Phi_X_y1_log = np.log(np.c_[1 - Phi_X[1, :], Phi_X[1, :]])
        self.Phi_Y_log = np.log((Y_count + 1)/(Y_count.sum()+2))

    @timeit
    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis = 1)

    def predict_proba(self, X):
        m = X.shape[0]
        metric = np.zeros((m, 2))
        # p(X\y = 0) p(y=0) , p(X\y = 1) p(y=1)
        metric[:, 0] = (1 - X).dot(self.Phi_X_y0_log[:, 0]) + X.dot(self.Phi_X_y0_log[:, 1]) + self.Phi_Y_log[0]
        metric[:, 1] = (1 - X).dot(self.Phi_X_y1_log[:, 0]) + X.dot(self.Phi_X_y1_log[:, 1]) + self.Phi_Y_log[1]
        return metric


@timeit
def sklearn_BNB(X, y):
    clf = MultinomialNB_SK(alpha=1,  fit_prior=False)
    clf.fit(X, y)

    # print X
    print "Error rate: %f" % (y != clf.predict(X)).mean()

if __name__ == '__main__':

    m = 3000
    n = 500
    rs = check_random_state(seed=None)

    X = rs.randint(2, size=(m, n))
    y = rs.randint(2, size=(m,))
    print("========== Start =========")
    print("BernouliNB:")
    clf = BernoulliNB()
    clf.fit(X, y)
    y_pred = clf.predict(X)
    print("Error rate: %f" % (y.reshape(y_pred.shape) != y_pred).mean())

    print("MultinomialNB:")
    clf = MultinomialNB()
    clf.fit(X, y)
    y_pred = clf.predict(X)
    print("Error rate: %f" % (y.reshape(y_pred.shape) != y_pred).mean())

    sklearn_BNB(X, y)


