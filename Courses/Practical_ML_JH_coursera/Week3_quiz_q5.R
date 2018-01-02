
rm(list = ls())
library(ElemStatLearn)
data(vowel.train)
data(vowel.test)

vowel.train['y'] = factor(vowel.train$y)
vowel.test['y'] = factor(vowel.test$y)

set.seed(33833)

clf = train(x=vowel.train[,-1], y=vowel.train[,1], method='rf')
varImp(clf)