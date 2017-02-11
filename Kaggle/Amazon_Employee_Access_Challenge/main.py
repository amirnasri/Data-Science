import pandas as pd
import sys
from sklearn.linear_model import LogisticRegression
import numpy as np
sys.path.append('/home/amir/git/ds/')
import ML

from sklearn import metrics
def scoring(estimator, X, y):
    y_pred = estimator.predict_proba(X)[:, 1]
    fpr, tpr, thresholds = metrics.roc_curve(y, y_pred, pos_label=1)
    auc = metrics.auc(fpr,tpr)
    return metrics.roc_auc_score(y, y_pred)
    #return auc


df = pd.read_csv('train.csv')

X = df.values[:, 1:]
y = df.values[:, 0].ravel()

clf = LogisticRegression()
'''
features, score = ML.feature_selection.forward_gready_selector(clf, X, y, scoring = scoring)
print score
X = X[features]
'''
from sklearn.model_selection import KFold
import matplotlib.pyplot as plt



def check_binary(y):
    return np.all(map(check_binary_, y))


def confusion_matrix(y_true, y_pred, pos_lable = 1):
    actual_pos_index = (y_true == pos_lable)
    actual_neg_index = ~actual_pos_index

    # predictions for the actual positive values
    y_pred_actual_pos = y_pred[actual_pos_index]
    fn, tp = (y_pred_actual_pos != pos_lable).sum(), (y_pred_actual_pos == pos_lable).sum()

    # predictions for the actual negative values
    y_pred_actual_neg = y_pred[actual_neg_index]
    tn, fp = (y_pred_actual_neg != pos_lable).sum(), (y_pred_actual_neg == pos_lable).sum()

    return map(float, (fn, tp, tn, fp))


def precision_recall_score(y_true, y_pred, pos_lable = 1):
    fn, tp, tn, fp = confusion_matrix(y_true, y_pred, pos_lable)
    precision, recall = None, None
    try:
        precision = tp / (tp + fp)
    except ZeroDivisionError:
        pass
    try:
        recall = tp / (tp + fn)
    except ZeroDivisionError:
        pass
    return precision, recall


def roc_scores(y_true, y_pred, pos_lable = 1):
    fn, tp, tn, fp = confusion_matrix(y_true, y_pred, pos_lable)
    tpr, fpr = None, None
    try:
        tpr = tp / (tp + fn)
    except ZeroDivisionError:
        pass
    try:
        fpr = fp/(fp+tn)
    except ZeroDivisionError:
        pass
    return tpr, fpr
def plot_roc_curve(clf, X, y, pos_lable = 1, cv = None):
    if cv is None:
        cv = KFold().split(X)
    for train_ind, test_ind in cv:
        X_train, X_test = X[train_ind], X[test_ind]
        y_train, y_test = y[train_ind], y[test_ind]
    clf.fit(X_train, y_train)
    t_vec = np.linspace(0, 1, 100)
    y_pred_proba = clf.predict_proba(X_test)[:, 1]
    roc = np.zeros((len(t_vec), 2))
    for i, t in enumerate(t_vec):
        y_pred = (y_pred_proba > t).astype(int)
        tpr, fpr = roc_scores(y_test, y_pred, pos_lable)
        roc[i, 1] = tpr
        roc[i, 0] = fpr
    plt.plot(roc[:, 0], roc[:, 1])
    #plt.scatter([roc[len(t_vec)/2, 0]], [roc[len(t_vec)/2, 1]])
    #plt.scatter([roc[92, 0]], [roc[92, 1]])
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.grid(True)
    plt.show()
plot_roc_curve(clf, X, y)