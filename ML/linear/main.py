"""
Test module for Linear_reg class.

"""
import numpy as np
import matplotlib.pyplot as plt
from logistic_reg_regularization import logistic_reg
from sklearn.linear_model import LogisticRegression
 
 
clf_l1_LR = LogisticRegression(C=1, penalty='l1', tol=0.01)
 
 
log_reg = logistic_reg()
X, Y = log_reg.load_data(filename='ex2data1.txt')

# Plot the data
plt.plot(X[np.nonzero(Y == 0)[0], 0], X[np.nonzero(Y == 0)[0], 1], 'go')
plt.plot(X[np.nonzero(Y == 1)[0], 0], X[np.nonzero(Y == 1)[0], 1], 'x')

theta, J = log_reg.fit(X, Y)
x = np.linspace(min(X[:, 1]), max(X[:, 1]), 100)
y = (theta[0][0] + theta[1][0] * x) / -theta[2][0]

delta = 1
x_plot_range_low = 0.9 * np.min(X[:, 0])
x_plot_range_high = 1.1 * np.max(X[:, 0])
y_plot_range_low = 0.9 * np.min(X[:, 1])
y_plot_range_high = 1.1 * np.max(X[:, 1])

x = np.arange(x_plot_range_low, x_plot_range_high, delta)
y = np.arange(y_plot_range_low, y_plot_range_high, delta)

Z = np.zeros((len(y), len(x)))
for i in range(len(x)):
    for j in range(len(y)):
        Z[j, i] = log_reg.map_feature(np.r_[x[i], y[j]].reshape(1, -1)).dot(theta)

plt.contour(x, y, Z, [0])
plt.show()

