
rm(list = ls())
library(ElemStatLearn)
data(SAheart)
set.seed(8484)
train = sample(1:dim(SAheart)[1],size=dim(SAheart)[1]/2,replace=F)
trainSA = SAheart[train,]
testSA = SAheart[-train,]

set.seed(13234)
cols = c('age', "tobacco",   "ldl",    "typea",     "obesity",   "alcohol")
train_X = trainSA[cols]
train_y = (trainSA$chd)
test_X = testSA[cols]
test_y = (testSA$chd)
#clf = train(Area ~ ., data=training, method='rpart')
#newdata = as.data.frame(t(colMeans(olive)))
#test_pred = predict(clf, newdata=newdata)

missClass = function(values,prediction){sum(((prediction > 0.5)*1) != values)/length(values)}

clf = train(x=train_X, y=train_y, method='glm', family='binomial')
pred_train = predict(clf, train_X)
pred_test = predict(clf, test_X)

train_missclass = missClass(train_y, pred_train)
test_missclass = missClass(test_y, pred_test)

