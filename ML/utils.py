import numpy as np
from scipy.sparse import issparse
import time

def check_array(X):
	X = np.array(X)
	if X.dtype != np.float64:
		try:
			X = X.astype(np.float64)
		except ValueError:
			raise ValueError("Could not convert type of array to float.")
	return X

def check_fit_input(X, y, binary=False):
	X = check_array(X)
	y = check_array(y)
	if X.ndim != 2:
		raise TypeError("X must be a 2-dimensional array with shape=(n_samples, n_features). "
						"Received X with shape=%s" % str(X.shape))
	if y.ndim > 2 or (y.ndim == 2 and y.shape[1] != 1):
		raise TypeError("y must be an array of form shape=(n_samples,) or shape=(n_samples, 1). "
						"Received array of shape=%s" % str(y.shape))
	if X.shape[0] != y.shape[0]:
		raise TypeError("X and y must have same first dimension.")
	if y.ndim == 2:
		y = y.ravel()
	if binary and not set(np.unique(y)) <= set([0, 1]):
		raise TypeError("y must contain only binary values.")
	return X, y

def np_dot(x, y):
	if issparse(x) or issparse(y):
		return x * y
	else:
		return np.dot(x, y)

def timeit(method):
	def timed(*args, **kw):
		ts = time.time()
		result = method(*args, **kw)
		te = time.time()

		print('function %s finished in %2.2f seconds' % (method.__name__, te-ts))
		return result

	return timed