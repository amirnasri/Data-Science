from sklearn.preprocessing import StandardScaler  
from sklearn.decomposition import PCA           
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def save_np_arrays(folder, array_names, arrays):
	assert type(array_names) == list or type(array_names) == tuple, \
		"expected type list or tuple, got %s" % array_names.__class__.__name__
	assert type(arrays) == list or type(arrays) == tuple, \
		"expected type list or tuple, got %s" % arrays.__class__.__name__

	print("saving numpy arrays %s" % ", ".join(array_names))
	for name, a in zip(array_names, arrays):
		np.save(os.path.join(folder, name), a)
	print("arrays saved successfully\n")

def load_np_arrays(folder, array_names):
	assert type(array_names) == list or type(array_names) == tuple, \
		"expected type list or tuple, got %s" % array_names.__class__.__name__

	print("loading numpy arrays %s" % ", ".join(array_names))
	l = []
	for name in array_names:
		try:
			l.append(np.load(os.path.join(folder, name + ".npy")))
		except IOError:
			l.append(None)
	print("arrays loaded\n")
	return l

if __name__ == '__main__':
	X_s, y = load_np_arrays('data', ['X_s', 'y'])
	if X_s is None or y is None:
		df = pd.read_csv('train_v2.csv')
		df = df.dropna(axis = 0)
		df = df[df.columns[df.dtypes != 'O']]
		sc = StandardScaler()
		X_s = sc.fit_transform(df.values[:, :-1])
		X_s = X_s[:, X_s.var(axis = 0) != 0]
		y = df.values[:, -1].reshape(-1, 1)
		save_np_arrays('data', ['X_s', 'y'], [X_s, y])


	'''
	pca = PCA()
	pca.fit(X_s)

	plt.plot(pca.explained_variance_ratio_)
	plt.yscale('log')
	plt.grid(True)
	plt.show()
	'''
