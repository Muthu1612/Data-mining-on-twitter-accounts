library(dplyr)
library(ggplot2)
library(caret)
library(Matrix)
library(kableExtra)

data<-read.csv("D:/WORK/Big Data Analytics/twitter.csv")
paste("NA values",sum(is.na(data)))
View(data)

library(caret)
#Train - Test split
set.seed(42)


partitione<-createDataPartition(y=data$Retweet,p=0.88,list=F)
testpart<-data[partitione,]
trainpart<-data[-partitione,]

model <- lm(Retweet~ Likes+Comments,data=trainpart)

summary(model)

plot(model)
#...
ggplot(data,aes(x=data$Likes,y=data$Retweet))+geom_point(aes(color=data$Comments))+geom_smooth(method="lm")
#...
pred<- model%>%predict(testpart)
tail(pred)


data.frame(R2=R2(pred,testpart$Retweet))



library(broom)
model.diagg.metrics <- augment(model)
head(model.diagg.metrics)


confint(model,conf.level=0.99)

plot(diff(log(data$Comments)))
plot(diff(diff(log(data$Likes))))

library(astsa)
library(tidyr)
library(viridis)
library(forecast)
library(tseries)

model1 <- auto.arima(data$Retweet)
model1

plot.ts(model1$residuals)
#The residual was high during the crash, indicating off trend values.

acf(ts(model1$residuals),main="ACF Residual")
acf(ts(model1$residuals),main="ACF Residuals")
pacf(ts(model1$residuals),main="PACF Residual")
#Checking residual values for correctness of data

#forecast
forect <- forecast(model1,level=c(95),h=60*6)
forect1<-forecast(model1,level=c(90),h=60*6)
plot(forect1)
#forecasting for next day (60 minutes * 6 hours)
plot(forect)

Box.test(model1$residuals,lag = 5,type = "Ljung-Box")
Box.test(model1$residuals,lag=4,type = "Ljung-Box")
#With Ljung Box test we can see that our standardized squared residuals does not reject the null hypothesis, confirming that we are not having autocorrelation between them.


