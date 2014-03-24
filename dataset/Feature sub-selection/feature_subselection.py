# Step 2 : Load data and run feature selection 
#########################################################
# Requirement:
# Y_train.txt or Y_train.npy: file containing an array of genere for documents. 
# e.g {"Doc1_Genre", "Doc2Genre", .., "Doc100Genre"}
#
# X_train.txt : file containing 2D array. Column = features; Rows = Document vector
# e.g.  { Doc1F1, Doc1F2, Doc1F3, .., Doc1Fn
#		  Doc2F1, Doc2F2, Doc2F3, .., Doc2Fn
#		  ...
#		  DocMF1, DocMF2, DocMF3, .., DocMFn}
# 
# X_features.txt : file containing list of features/words.
# e.g. { word1, word2, word3, ..., wordn}
##########################################################
# TO-DO:
# Change filenames to appropriate file_name and its path
# Change value of k to the desired number of features
##########################################################


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