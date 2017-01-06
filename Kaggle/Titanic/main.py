import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import KFold
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

def one_hot_encoder(df):
	for col in df.columns:
		col_data = df[col]
		if col_data.dtype != object:
			continue
		values = np.unique(col_data)
		for v in values:
			df[col + '_' + str(v)] = (df[col] == v).astype(int)
		del df[col]


def clean_data(df):
	columns = [c for c in df.columns if c not in ['Name', 'Ticket', 'Cabin']]
	df = df[columns]
	#df.Sex = map(lambda s: 1 if s == 'male' else 0, df.Sex)
	df.Age[df.Age.isnull()] = df.Age[~df.Age.isnull()].mean()
	df.Fare[df.Fare.isnull()] = df.Fare[~df.Fare.isnull()].mean()
	df.Embarked[df.Embarked.isnull()] = 'S'
	#Embarked_vals = np.unique(df.Embarked)
	# Sorting values may be better
	#Embarked_map = {i:j for i, j in zip(Embarked_vals, range(len(Embarked_vals)))}
	#df.Embarked = map(lambda k: Embarked_map[k], df.Embarked)
	#pd.to_pickle(df, 'df')
	one_hot_encoder(df)
	return df

def eval_classifier(clf, X, y):
	#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)
	perm = np.random.permutation(X.shape[0])
	X = X[perm]
	y = y[perm]
	score = []
	for train_index, test_index in KFold(n = X.shape[0], n_folds=3):
		X_train = X[train_index]
		y_train = y[train_index]
		X_test = X[test_index]
		y_test = y[test_index]
		sc = StandardScaler()
		sc.fit(X_train)
		X_train = sc.transform(X_train)
		clf.fit(X_train, y_train)
		y_pred = clf.predict(sc.transform(X_test))
		score.append(1 - np.abs(y_pred - y_test).mean())
	print score
	print np.mean(score)

def scorer(estimator, X, y):
	y_pred = estimator.predict(X)
	#assert sorted(np.unique(y_pred)) == [0, 1], \
	#	"prediction array contains values other than 0 and 1"
	return np.mean(y_pred == y)

def filter_df(df, items):
	columns = []
	for c in df.columns:
		include = False
		for i in items:
			if c.startswith(i):
				include = True
				break
		if include:
			columns.append(c)
	return df[columns]

df = clean_data(pd.read_csv('train.csv'))
X_train = df[[c for c in df.columns if c not in ['Survived', 'PassengerId']]].values
#X_train = filter_df(df, ['Sex', 'Pclass', 'Fare']).values
y_train = df.Survived.values

clf = RandomForestClassifier()
#clf = SVC(kernel='poly')
#clf = LogisticRegression()
sc = StandardScaler()
pl = Pipeline([('sc', sc), ('clf', clf)])
#pl = Pipeline([('clf', clf)])

param_grid = {}
#param_grid['clf__C'] = np.logspace(-1, 1, 3)
#param_grid['clf__gamma'] = range(1, 5)
param_grid['clf__n_estimators'] = [1, 2, 5, 10, 20, 40]
gs = GridSearchCV(pl, param_grid, scoring=scorer, verbose=True, n_jobs=4, cv = KFold(9))
gs.fit(X_train, y_train)
#eval_classifier(clf, X_train, y_train)
print gs.best_params_, gs.best_score_
print pd.DataFrame(gs.cv_results_)

'''
clf.fit(X_train, y_train)
df = clean_data(pd.read_csv('test.csv'))
#X_test = df.values

submit = pd.DataFrame({'PassengerId' : df.PassengerId, 'Survived' : clf.predict(df.values)})
submit.to_csv('submit.csv',index= False)
'''

