
rm(list=ls())
library(caret)

library(gbm)

set.seed(3433)

library(AppliedPredictiveModeling)

data(AlzheimerDisease)

adData = data.frame(diagnosis,predictors)

inTrain = createDataPartition(adData$diagnosis, p = 3/4)[[1]]

training = adData[ inTrain,]

testing = adData[-inTrain,]

set.seed(62433)

gbm = train(diagnosis ~ ., data=training, method='gbm')
gbm_pred = predict(gbm, subset(testing, select = -c(diagnosis)))
gbm_acc = mean(gbm_pred == testing$diagnosis)


rf = train(diagnosis ~ ., data=training, method='rf')
rf_pred = predict(rf, subset(testing, select = -c(diagnosis)))
rf_acc = mean(rf_pred == testing$diagnosis)


lda = train(diagnosis ~ ., data=training, method='lda')
lda_pred = predict(lda, subset(testing, select = -c(diagnosis)))
lda_acc = mean(lda_pred == testing$diagnosis)

preds = data.frame(gbm_pred, rf_pred, lda_pred, testing$diagnosis)
stack = train(diagnosis ~., data=preds, method='rf')
stack_pred = predict(stack, subset(preds, select = -c(diagnosis)))
stack_acc = mean(stack_pred == testing$diagnosis)

