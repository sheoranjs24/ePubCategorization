#***********************************************************
# Step 1 : Format data as per Python SVM format
# Load Data in R ---------
dataset <- read.table("/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-500+books/SVM2D.txt", sep=",", header=TRUE)

# Transpose data
dataset1 <- t(dataset)
nrow(dataset1)
ncol(dataset1)

# write correct data format in file for later use in R
write.table(dataset1, file = "/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-500+books/X_train.txt", sep = ",", col.names = F, row.names = F)

# select feature names from WEKA data file ------------
grep "@ATTRIBUTE" wekaRaw.arff | gawk '{print $2;}' > features.txt
# delete first 2 lines after this

# Open data in R ------------
mydata <- read.table("/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-500+books/features.txt")
# Transform data
mydata1 <- t(mydata)
# write data in file
write.table(mydata1, file = "/Users/sheoranjs24/Projects/ePubCategorization/dataset/SVM/SVM-500+books/X_features.txt", sep = ",", col.names = F, row.names = F)

# Create genre Y_train.txt from python script

# matrix : (n_docs, m_features)
# 1D-row matrix : (n_docs_genre)
# 1D-col matrix : (m_features)

#***********************************************************
# Step 2 : Load data and run feature selection 
#load text file in python ------------
X_train = numpy.loadtxt("X_train.txt", delimiter=',', dtype="float")
Y_train = numpy.load("Y_train.npy")
X_features = numpy.loadtxt("X_features.txt", delimiter=',', dtype="str")

# feature selection 
import sklearn
from sklearn import feature_selection
myselector = feature_selection.SelectPercentile(score_func=feature_selection.chi2, percentile=50) # used 30 for 170
myfeatures = myselector.fit(X_train, Y_train)

# store selected features for later use (when we test new ebooks)
new_features = X_features [myselector.get_support(indices=True)] 
# save new features to file .npy extension
numpy.save("final_features", new_features)

# new data based on selected features
new_X_train = myselector.transform(X_train)
# save new_training_data to file .npy extension
numpy.save("new_X_train", new_X_train)

##***********************************************************
# Step 3 : Run SVM and save svm to file 
# SVM 
import sklearn.svm
clf = sklearn.svm.LinearSVC(C=100).fit(new_X_train, Y_train)
# save result to file for later use
import pickle
#pickle.dump(clf, trained_str)  # copy SVM to string
from sklearn.externals import joblib
joblib.dump(clf, "trained_SVM.pkl")

##***********************************************************
# Step 4 : Test SVM
# test new book 
#clf2 = pickle.loads(trained_str)
clf2 = joblib.load("trained_SVM.pkl")
#clf2 = pickle.loads(pickle.dumps(clf))  # strings

predicted_genre = clf2.predict(features_of_new_docs)
print predicted_genre

##***********************************************************
# Step 5 : Evaluate SVM























