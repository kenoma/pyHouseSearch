x<-read.csv(file.choose(),sep=';', row.names=NULL,dec=',')
summary(x)
model <- lm(Price ~ Square + Rooms + Floor + MaxFloor + Type, data = x)
predicted.cost <- predict(model, x)
actual.price <- x$Price
plot(predicted.cost, actual.price)
sorted <- sort(predicted.cost / actual.price, decreasing = TRUE)
ord <- order( - sorted)
x[ord[1:30],]$Link

