# Step 2 : Load data and run feature selection 
#load text file in python ------------
import numpy
Y_train = numpy.load("Y_train.npy")
X_features = numpy.loadtxt("X_features.txt", delimiter=',', dtype="str")
X_train = numpy.loadtxt("X_train.txt", delimiter=',', dtype="float")

# feature selection 
import sklearn
from sklearn import feature_selection
#myselector = feature_selection.SelectPercentile(score_func=feature_selection.chi2, percentile=50) # used 30 for 170
myselector = feature_selection.SelectKBest(score_func=feature_selection.chi2, k=5000)  # k = no of features needed
myfeatures = myselector.fit(X_train, Y_train)

# store selected features for later use (when we test new ebooks)
new_features = X_features [myselector.get_support(indices=True)] 
# save new features to file .npy extension
numpy.savetxt("final_features_5000.txt", new_features, fmt='%s', delimiter=',', newline='\n')

# new data based on selected features
new_X_train = myselector.transform(X_train)
# save new_training_data to file .npy extension
numpy.savetxt("new_X_train_5000.txt", new_X_train, fmt='%s', delimiter=',',newline='\n')