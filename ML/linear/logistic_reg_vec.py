import numpy as np
import matplotlib.pyplot as plt
    
    
class logistic_reg_vec:
    def predict(self, x, theta):
        return (1/(1 + np.exp(-x.dot(theta))))
    
    def cost_function(self, X, Y, theta):
        #print predict(X[1, :], theta)
        #sum = 0
        #for i in range(m):
        #    sum += Y[i][0] * np.log(self.predict(X[i, :], theta)) + (1 - Y[i][0]) * np.log(1 - self.predict(X[i, :], theta))
        #return -sum/m
        return np.average(Y * np.log(self.predict(X, theta)) + (1 - Y) * np.log(1 - self.predict(X, theta)), axis = 0)
       
    # Read data from file
    def load_data(self, filename):
        f = open(filename, 'r')
        data = []
        for line in f:
            row = line.strip().split(',')
            data.append(row)
        
        m = len(data)
        feature_num = len(data[0]) - 1
        X = np.zeros((m, feature_num + 1))
        Y = np.zeros((m, 1))
        for i in range(m):
            for j in range(feature_num):
                X[i][0] = 1
                X[i][j + 1] = float(data[i][j])
            Y[i] = float(data[i][-1])
            
        return X, Y
    
    # feature normalization
    def normalize_feature(self, X):
        X = X.copy()
        self.X_mean = np.reshape(np.average(X[:, 1:], axis = 0), (1, -1))
        X[:, 1:] -= self.X_mean
        self.X_sigma = np.reshape(np.average(X[:, 1:]**2, axis = 0)**0.5, (1, -1))
        X = X.dot(np.diag(np.r_[1, self.X_sigma.ravel()]**-1))
        print self.X_mean
        print self.X_sigma
        return X
     
    def theta_unnormalized(self, theta):
        theta_unnorm = np.zeros(theta.shape)
        theta_unnorm[1:, 0] = theta[1:, 0].T/self.X_sigma
        theta_unnorm[0][0] = theta[0][0] - np.sum(theta[1:] * self.X_mean * (self.X_sigma**-1))
        return theta_unnorm
        
    def gradient(self, X, Y, theta):
        m = X.shape[0]
        return 1/m * X.T.dot(Y - self.predict(X, theta))
    
    def fit(self, X, Y):
        m = X.shape[0]
        feature_num = len(X[0]) - 1
        iter_num = 100000
        theta = np.reshape([1, -1, 10], (3, 1))
        theta_temp = np.zeros((feature_num + 1, 1))
        alpha = .01
        h = range(m)
        J = range(iter_num)
        for k in range(iter_num):
            theta -= alpha * self.gradient(X, Y, theta)
            print self.gradient(X, Y, theta)
            J[k] = self.cost_function(X, Y, theta)
        
        xx = np.zeros((1, 3))
        xx[0, 1:] = (np.array([45, 85])-self.X_mean)/self.X_sigma
        xx[0, 0] = 1
        print self.predict(xx, theta)
        
        return theta, J
        
        
