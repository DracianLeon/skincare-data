data <- read.csv("data/all_products.csv",  header=TRUE, encoding="UTF-8")
head(data)

# Drop URL
data <- data[, -c(6)]
# Make prices numeric
data$Price <- as.numeric(sub("C\\$", "", data$Price))

# Check out data
summary(data$Concern)
summary(data$Category)
summary(data$Price)

hist(data$Price, labels=TRUE)
expensive <- data[data$Price > 300,]
expensive[, c("Product", "Price")]

# Fix prices from non-standard sizes
data[1183,]$Price <- 390

library(data.table)
data[data$Product %like% "Ancienne", ] # Creme Ancienne
data[c(711, 725, 1726, 1737),]$Price <- 187

data[c(624, 1663, 1667),]$Price <- 230 # Creme de la mer

data$Category <- factor(data$Category)
data$Concern <- factor(data$Concern)

# Create range variable
low <- data[data$Price <= 30, ]
mid <- data[data$Price > 30 & data$Price <= 50, ]
high <- data[data$Price > 50, ]

# TODO create range variable here

# Shuffle + split data
data <- data[sample(nrow(data)), ]

set.seed(123)
test_size <- floor(0.7 * nrow(data))
train_idx <- sample(seq_len(nrow(data)), size=test_size)

train <- data[train_idx, ]
test <- data[-train_idx, ]

library(caret)

# Predict price using category, concern?
# Predict concern using price, category, brand?
# PLot residuals, cluster data
res <- train(Price ~ 
             Concern + 
             Category + 
             Brand, 
             data=train, method="lm", trControl=trainControl(method="cv",number=10))

res
model <- res$finalModel
summary(model)
