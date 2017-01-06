from sklearn.cross_validation import KFold
#import sklearn
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.base import clone

class Stacking(BaseEstimator):
	def __init__(self, estimators, combiner):
		self.estimators = estimators
		self.n_estimators = len(estimators)
		self.combiner = combiner

	def fit(self, X, y):
		self.classes = sorted(np.unique(y))
		self.n_classes = len(self.classes)
		#self.clfs = [clone(estimator) for estimator in self.estimators]
		m, n = X.shape
		X_1 = np.zeros((m, self.n_classes - 1, self.n_estimators))
		#l = []
		for i, estimator in enumerate(self.estimators):
			estimator.fit(X, y)
			X_1[:, :, i] = estimator.predict_proba(X)[:, :-1]
			#l.append(estimator.predict_proba(X))

		#X_1 = np.concatenate(l, axis = 1)
		#print "X_1.shape= " + repr(X_1.shape)

		self.combiner.fit(X_1.reshape(m, -1, order='F'), y)
		#print self.combiner.coef_, self.combiner.intercept_

	def predict(self, X):
		m, n = X.shape
		X_1 = np.zeros((m, self.n_classes - 1, self.n_estimators))
		for i, estimator in enumerate(self.estimators):
			X_1[:, :, i] = estimator.predict_proba(X)[:, :-1]

		y_pred = self.combiner.predict(X_1.reshape(m, -1, order='F'))
		#print "y_pred= " + repr(y_pred)
		return y_pred
