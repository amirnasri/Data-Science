
rm(list=ls())

set.seed(3523)

library(AppliedPredictiveModeling)

data(concrete)

inTrain = createDataPartition(concrete$CompressiveStrength, p = 3/4)[[1]]

training = concrete[ inTrain,]

testing = concrete[-inTrain,]

set.seed(233)

con<-trainControl(method="cv",number=10)

#lda =  train(CompressiveStrength~ ., data=training, method='lasso', metric="RMSE",tuneLength = 10, trControl = con)

#lda_pred = predict(lda, subset(testing, select = -c(CompressiveStrength)))
#lda_rmse = mean((lda_pred - testing$CompressiveStrength)^2)^.5

lasso = enet(x=as.matrix(subset(training, select = -c(CompressiveStrength))), y=as.matrix(training$CompressiveStrength),lambda = 0)

plot.enet(lasso, xvar = 'step')


