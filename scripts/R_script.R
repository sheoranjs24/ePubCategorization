
# Load Data
#dataset <- read.table("/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-170+books/SVM2D.txt", sep=",", header=TRUE)
#genre <- read.table("/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-170+books/SVM-SP.txt", sep=",")

# Transpose data
#dataset1 <- t(dataset)
#genre1 <- t(genre)

# Make data-frame
#dataset2 <- as.data.frame(dataset1)
#dataset2$genre <- c(genre1)

# write correct matrix format to file for later use in python
#write.table(dataset1, file = "/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-170+books/training.txt", sep = ",")
#write.table(genre1, file = "/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-170+books/genre.txt", sep = ",")

# write correct data format in file for later use in R
#write.table(dataset2, file = "/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-170+books/train_frame.txt", sep = ",", col.names = F, row.names = F)

# read dataset from file
mydata <- read.table("/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-170+books/train_frameR.txt", sep=",", header=TRUE, nrows=175, comment.char = "")

# convert data into data-frame
mydataframe <- as.data.frame(mydata)

# Feature selection
weights <- information.gain(genre ~ ., mydataframe)
subset <- cutoff.k(weights, 2)
f <- as.simple.formula(weights, "genre")


