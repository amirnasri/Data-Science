from scipy import sparse
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import LabelBinarizer
import numpy as np

def forward_gready_selector(clf, X, y, n_features = None, scoring = None):
	l = []
	lb = LabelBinarizer(sparse_output=True)
	X_binarized = [lb.fit_transform(c) for c in X.T]
	good_features = []
	results = []
	n = X.shape[1]
	if n == 0:
		raise ValueError("Array X cannot be empty.")
	if n_features is None:
		n_features = n
	if (n_features > n) or (n_features <= 0):
		raise ValueError(
			"n_feature cannot be non-positive or larger that the number of features in the input array X. Received %s." % str(
				n_features))

	if 0 < n_features < 1:
		n_features = np.ceil(n * n_features)

	last_score, score = None, 0
	while len(good_features) < n_features:
		scores = []
		for f in range(X.shape[1]):
			if f not in good_features:
				curr_features = list(good_features) + [f]
				X_sub = sparse.hstack([X_binarized[i] for i in curr_features]).tocsr()
				score = cross_val_score(clf, X_sub, y, scoring=scoring).mean()
				scores.append((f, score))
		best_f, best_score = max(scores, key=lambda x: x[1])

		if last_score is not None and best_score <= last_score:
			break

		good_features.append(best_f)
		results.append((best_f, best_score))

		last_score = best_score

	best_features = map(lambda x: x[0], results)
	best_score = results[-1][1]
	return best_features, best_score
