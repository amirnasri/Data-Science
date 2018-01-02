
rm(list = ls())

# Question 1
library(caret)
set.seed(125)
library(AppliedPredictiveModeling)
library(pgmm)
data(olive)
olive = olive[,-1]
#data_df = data.frame(diagnosis,predictors)
inTrain = createDataPartition(olive$Area)[[1]]
training = olive[ inTrain,]
testing = olive[-inTrain,]


clf = train(Area ~ ., data=training, method='rpart')
newdata = as.data.frame(t(colMeans(olive)))
test_pred = predict(clf, newdata=newdata)

#test_pred = predict(glm, testing_sub)
#test_pca_pred = predict(glm_pca, testing_sub_pca)
#train(y=training$diagnosis, x=training_sub_pca, method='glm')
#predict(glm, data=testing_sub_pca)

#print(confusionMatrix(testing$diagnosis, test_pred))
#print(confusionMatrix(testing$diagnosis, test_pca_pred))
