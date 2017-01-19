x<-read.csv(file.choose(),sep=';')
summary(x)
x<-read.csv(file.choose(),sep=';', row.names=NULL)
summary(x)
summary(x$Price)
x<-read.csv(file.choose(),sep=';', row.names=NULL)
summary(x$Price)
summary(x)
x<-read.csv(file.choose(),sep=';', row.names=NULL)
summary(x)
summary(Price)
summary(x$Price)
x<-read.csv(file.choose(),sep=';', row.names=NULL,dec=',')
summary(x$Price)
summary(x$Price)
summary(x)
summary(x$Square,x$Price)
plot(x$Square,x$Price)
length(unique(x$ID))
length(x$ID)
x<-read.csv(file.choose(),sep=';', row.names=NULL,dec=',')
summary(x)
x<-read.csv(file.choose(),sep=';', row.names=NULL,dec=',')
summary(x)
x<-read.csv(file.choose(),sep=';', row.names=NULL,dec=',')
summary(x)
length(unique(x$ID))
length(x$ID)
model <- lm(Price ~ Square + Rooms + Floor + MaxFloor + Type, data = x)
coef(model)
predicted.cost <- predict(model, x)
actual.price <- x$price
plot(predicted.cost, actual.price)
par(new=TRUE, col="red")
dependency <- lm(predicted.cost, actual.price)
dependency <- lm(predicted.cost, actual.price)
actual.price <- x$Price
dependency <- lm(predicted.cost, actual.price)
x$Price
predicted.cost
plot(predicted.cost, actual.price)
par(new=FALSE, col="black")
plot(predicted.cost, actual.price)
dependency <- lm(predicted.cost, actual.price)
sorted <- sort(predicted.cost / actual.price, decreasing = TRUE)
sorted[0:10]
plot(x$Rooms,x$Price)
plot(x$Rooms,x$Price)
plot(x$Square,x$Price)
plot(x$Square,x$Price)
plot(log(x$Square),x$Price)
plot(x$Square,x$Price)
plot(x$Square,x$Rooms)
x[sorted <- sort(predicted.cost / actual.price, decreasing = TRUE)]
x[402,]
x[464,]
x[341,]
x[445,]
x[sorted <- sort(predicted.cost / actual.price, decreasing = TRUE)]
x[14,]
sorted[0:100]
x[495,]
x[413,]
x[528,]
x[355,]
