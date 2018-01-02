rm(list=ls())

library(doMC)
library(caret)
library(gbm)

registerDoMC(cores = 3)

setwd('~/Dropbox/Courses/Practical_ML_JH_coursera/Project/')
training = read.csv('pml-training.csv')
testing = read.csv('pml-testing.csv')

train_rm_na = training[, colSums(is.na(training)) == 0]

factor_cols = colnames(train_rm_na)[sapply(train_rm_na, class) == 'factor']
non_factor_cols = colnames(train_rm_na)[sapply(train_rm_na, class) != 'factor']

cols = character(0)
for (c in factor_cols) {
        x = summary(train_rm_na[,c])
        if (class(names(x)[1]) != "character" || names(x)[1] != '')
            cols = c(cols, c)
}

cols_total = c(cols, non_factor_cols)
#cols_total = c("X",   "cvtd_timestamp",              "classe" )
cols_total = cols_total[which((cols_total != "X") & (cols_total != "cvtd_timestamp") & (cols_total != "new_window"))]

# Shuffle train data
#train_rm_na = train_rm_na[sample(dim(train_rm_na)[1]),]

# Use a fraction of training data for training 
# to reduce processing time
inTrain = createDataPartition(train_rm_na$classe, p = .1)[[1]]
train = train_rm_na[inTrain, cols_total]
#train_rm_classe = train[cols_total[which(cols_total != "classe")]]


inTrain = createDataPartition(train$classe)[[1]]
train_set = train[inTrain,]
validation_set = train[-inTrain,]

#tc = trainControl(method="cv")
clf = train(x=train_set[which(cols_total != "classe")], y=train_set$classe, method='rf')
# #clf = train(classe ~ ., data=train, method='rf', trControl=tc)
train_pred = predict(clf, train_set)
validation_pred = predict(clf, validation_set)
train_cm = confusionMatrix(train_pred, train_set$classe)
validation_cm = confusionMatrix(validation_pred, validation_set$classe)




# Train final model
test = testing[cols_total[which(cols_total != "classe")]]
clf = train(x=train[which(cols_total != "classe")], y=train$classe, method='rf')
#clf = train(classe ~ ., data=train, method='rf', trControl=tc)
train_pred = predict(clf, train)
test_pred = predict(clf, test)

train_cm = confusionMatrix(train_pred, train$classe)
#test_cm = confusionMatrix(test_pred, testing$classe)


