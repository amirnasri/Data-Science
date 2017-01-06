from sklearn.preprocessing import StandardScaler  
from sklearn.decomposition import PCA           
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from sklearn.svm import SVC
from sklearn.cross_validation import  cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import Imputer


def scorer(y, y_):
	return np.abs(y - y_).mean()

def plot_learning_curve(clf, X, y, test_sizes = np.linspace(0.1, 1, 10), scorer = None):
	m, n = X.shape
	train_len = .7* m
	X_train, y_train = X[:train_len], y[:train_len]
	X_test, y_test = X[train_len:], y[train_len:]
	train_score = []
	test_score = []
	test_sizes_ = [np.round(i) for i in (train_len * test_sizes)]
	for s in test_sizes_:
		X_, y_ = X_train[:s* train_len], y_train[:s* train_len]
		clf.fit(X_, y_)
		train_score.append(scorer(y_, clf.predict(X_)))
		test_score.append(scorer(y_test, clf.predict(X_test)))
	plt.plot(test_sizes_, train_score)
	plt.plot(hold=True)
	plt.plot(grid=True)
	plt.plot(test_sizes_, test_score, 'r')
	plt.plot(test_sizes_,  [scorer(np.zeros(y_test.shape), y_test)] * len(test_sizes_), 'm--')

	plt.show()

print os.getcwd()
if not os.path.isfile('X_s.npy'):
	#df = pd.read_csv('train_v2.csv')
	X = np.genfromtxt('train_v2.csv', delimiter=',')

	imp = Imputer(missing_values=np.nan, strategy='mean', axis=0)
	#df = df.dropna(axis = 0)

	df = df[df.columns[df.dtypes != 'O']]

	sc = StandardScaler()
	X_s = sc.fit_transform(df.values[:, :-1])
	X_s = X_s[:, X_s.var(axis = 0) != 0]
	y = df.values[:, -1]
	pca = PCA(n_components=5)
	pca.fit(X_s)
	X_s = pca.transform(X_s)
	perm = np.random.permutation(X_s.shape[0])
	print('saving data')
	np.save('X_s', X_s[perm])
	np.save('y', y[perm])
else:
	print('loading data')
	X_s = np.load('X_s.npy')
	y = np.load('y.npy')

y = y.ravel()
clf = SVC()

#clf = RandomForestClassifier(n_estimators=10)

plot_learning_curve(clf, X_s[:1000], y[:1000], scorer=scorer)
#clf.fit(X_s[:1000], y[:1000])
#print cross_val_score(clf, X_s[:1000], y.ravel()[:1000], scoring=lambda y1, y2: np.abs(y1-y2).mean())
#y_pred = clf.predict(X_s[:1000])
#plt.plot(pca.explained_variance_ratio_)
#plt.yscale('log')
#plt.grid(True)
#plt.show()

