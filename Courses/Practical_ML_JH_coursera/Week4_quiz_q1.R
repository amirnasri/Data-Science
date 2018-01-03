
rm(list=ls())
library(ElemStatLearn)
data(vowel.train)
data(vowel.test)


set.seed(33833)
train = vowel.train
test = vowel.test


train['y'] = as.factor(train$y)
test['y'] = as.factor(test$y)

rf = train(x=subset(train, select=-c(y)), y=train$y, method='rf')
pred_rf_test = predict(rf, subset(test, select=-c(y)))
rf_cm = confusionMatrix(pred_rf_test, test$y)

gbm = train(x=subset(train, select=-c(y)), y=train$y, method='gbm')
pred_gbm_test = predict(gbm, subset(test, select=-c(y)))
gmb_cm = confusionMatrix(pred_gbm_test, test$y)

ind = (pred_gbm_test == pred_rf_test)
print(mean(pred_rf_test[ind] == test$y[ind]))