
# Question 4
rm(list = ls())

library(caret)
library(AppliedPredictiveModeling)
set.seed(3433)
data(AlzheimerDisease)
adData = data.frame(diagnosis,predictors)
inTrain = createDataPartition(adData$diagnosis, p = 3/4)[[1]]
training = adData[ inTrain,]
testing = adData[-inTrain,]

cols = character(0)
for (s in colnames(training)) {
        if (length(grep('^IL', s)) != 0) 
                cols = c(cols, s)
}

# Question 5

training_sub = training[cols]
testing_sub = testing[cols]
pca = preProcess(training_sub, method='pca', thresh=.8)
training_sub_pca = predict(pca, training_sub)
testing_sub_pca = predict(pca, testing_sub)
#browser()
glm = train(x=training_sub, y=training$diagnosis, method='glm')
glm_pca = train(x=training_sub_pca, y=training$diagnosis, method='glm')
#glm = train(training$diagnosis ~ ., data=training_sub, method='glm')
#glm_pca = train(training$diagnosis ~ ., data=training_sub_pca, method='glm')

test_pred = predict(glm, testing_sub)
test_pca_pred = predict(glm_pca, testing_sub_pca)
#train(y=training$diagnosis, x=training_sub_pca, method='glm')
#predict(glm, data=testing_sub_pca)

print(confusionMatrix(testing$diagnosis, test_pred))
print(confusionMatrix(testing$diagnosis, test_pca_pred))
