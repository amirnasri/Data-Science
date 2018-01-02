rm(list=ls())

set.seed(3523)

library(caret)
library(AppliedPredictiveModeling)

data(concrete)

inTrain = createDataPartition(concrete$CompressiveStrength, p = 3/4)[[1]]

training = concrete[ inTrain,]

testing = concrete[-inTrain,]

set.seed(325)
library("e1071")

clf = svm(CompressiveStrength~., training)
pred = predict(clf, testing)

print(mean((pred - testing$CompressiveStrength)^2)^.5)