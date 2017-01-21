from sklearn import datasets
import numpy as np

from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from stacking import StackingClassifier
from sklearn.cross_validation import train_test_split
#import sys
#sys.path.append('/home/amir/git')
#from mlxtend.classifier import StackingClassifier

iris = datasets.load_iris()
X, y = iris.data[:, 1:3], iris.target
perm = np.random.permutation(X.shape[0])
X, y = X[perm], y[perm]

clf1 = KNeighborsClassifier(n_neighbors=1)
clf2 = RandomForestClassifier(random_state=1)
clf3 = GaussianNB()
lr = LogisticRegression()


sclf = StackingClassifier(estimators=[clf1, clf2, clf3], combiner=lr)
#sclf = StackingClassifier([clf1, clf2, clf3], lr, use_probas = True)
print('3-fold cross validation:\n')

n_sim = 50
scores = []
for i in range(n_sim):
	perm = np.random.permutation(X.shape[0])
	X_, y_ = X[perm], y[perm]
	score = []
	for clf, label in zip([clf1, clf2, clf3, sclf],
                      ['KNN',
                       'Random Forest',
                       'Naive Bayes',
                       'Stacking']):
		#print model_selection.cross_val_score(clf, X_, y_, cv=3, scoring='accuracy')
		score.append(model_selection.cross_val_score(clf, X_, y_, cv=3, scoring='accuracy').mean())
	scores.append(score)
        #print("Accuracy: %0.2f (+/- %0.2f) [%s]"
        #     % (scores.mean(), scores.std(), label))

#def scorer(estimator, X, y):
#	return (y == estimator.predict(X)).mean()

print np.array(scores).mean(axis=0)


#X_train, X_test, y_train, y_test = train_test_split(X, y)

#sclf.fit(X_train, y_train)
#print(sclf.predict(X_test) == y_test).mean()