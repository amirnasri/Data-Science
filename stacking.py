import numpy as np
from sklearn.base import BaseEstimator

class StackingClassifier(BaseEstimator):
	def __init__(self, estimators, combiner):
		self.estimators = estimators
		self.n_estimators = len(estimators)
		self.combiner = combiner

	def fit(self, X, y):
		self.classes = sorted(np.unique(y))
		self.n_classes = len(self.classes)
		m, n = X.shape
		X_1 = np.zeros((m, self.n_classes - 1, self.n_estimators))
		for i, estimator in enumerate(self.estimators):
			estimator.fit(X, y)
			X_1[:, :, i] = estimator.predict_proba(X)[:, :-1]

		self.combiner.fit(X_1.reshape(m, -1, order='F'), y)

	def predict(self, X):
		m, n = X.shape
		X_1 = np.zeros((m, self.n_classes - 1, self.n_estimators))
		for i, estimator in enumerate(self.estimators):
			X_1[:, :, i] = estimator.predict_proba(X)[:, :-1]

		y_pred = self.combiner.predict(X_1.reshape(m, -1, order='F'))
		return y_pred
