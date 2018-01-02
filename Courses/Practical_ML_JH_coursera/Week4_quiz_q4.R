rm(list=ls())

library(lubridate) # For year() function below

dat = read.csv("~/Downloads//gaData.csv")

training = dat[year(dat$date) < 2012,]

testing = dat[(year(dat$date)) > 2011,]

tstrain = ts(training$visitsTumblr)
fit = bats(tstrain)
f = forecast(fit, h=235, level = c(95))

print(mean((f$upper > testing$visitsTumblr) & (f$lower < testing$visitsTumblr)))
