from scipy import fromfile
from numpy import *
import matplotlib.pyplot as plt
    
if (__name__ == '__main__'):
    
    f = open('ex1data2.txt', 'r')
    x = [];
    m = 0                           #number of samples
    
    for line in f:
        r = line.strip().split(',')
        x.append(r)
        m = m + 1
    feature_num = len(x[0]) - 1
    X = zeros((m, feature_num + 1))
    Y = zeros((m, 1))
    for j in range(m):
        X[j][0] = 1                 #intercept term
        for k in range(feature_num):
            X[j][k + 1] = float(x[j][k])    
        Y[j][0] = float(x[j][feature_num])
    
    # feature normalization
    X[:, 1:] = X[:, 1:] - (sum(X[:, 1:], axis = 0)/m)
    power_col = ((sum(X[:, 1:]**2, axis = 0)/m)**0.5)
    X = X.dot(diag(r_[1, power_col]**-1))
    
    # optimal theta using normal equations
    theta = linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
    J = (X.dot(theta)-Y).T.dot(X.dot(theta)-Y)
    
    print theta
    print J
    
    plt.plot(X[:, 1], Y, 'x')
    plt.plot(X[:, 1], X.dot(theta))
    #plt.show()
    
    # Gradient descent (vertor version)
    alpha = 0.000001
    iter_num = 10000
    J = zeros((1, iter_num))
    theta = zeros((feature_num + 1, 1))
    for i in range(iter_num):
        theta = theta - alpha * (X.T.dot(X.dot(theta)-Y))
        J[0][i] = (X.dot(theta)-Y).T.dot(X.dot(theta)-Y)
    
    print theta
    print J
    
    
    # Gradient descent (scalar version)
    alpha = 0.000001
    iter_num = 10000
    J = zeros((1, iter_num))
    theta = zeros((feature_num + 1, 1))
    theta_temp = zeros((feature_num + 1, 1))
    for iter in range(iter_num):
        for j in range(feature_num + 1):
           sum = 0
           for i in range(m):
                sum = sum + (Y[i][0] - theta.T.dot(X[i])) * X[i][j]
           theta_temp[j][0] = theta[j][0] + alpha * sum
        theta = theta_temp.copy()
        
    print theta
        
            
            
            

