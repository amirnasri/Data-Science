
rm(list = ls())

# Question 1
library(caret)
set.seed(125)
library(AppliedPredictiveModeling)
data(segmentationOriginal)
so = segmentationOriginal
#data_df = data.frame(diagnosis,predictors)
#inTrain = createDataPartition(so$Case)[[1]]
#training = so[ inTrain,]
#testing = so[-inTrain,]

training = so[so$Case=='Train',]
testing = so[so$Case=='Test',]

clf = train(x=training[,-3], y=training[,3], method='rpart')
plot(clf$finalModel,uniform=TRUE)
text(clf$finalModel, use.n=TRUE,all=TRUE,cex=.8)
