/* 
Step 0 : ------------
1) convert ePub to text file by extracting data
2) Remove eBooks not in english
3) Remove audio eBooks
4) remove ebooks with only one chapter

Data : text file containing bag of words (array of words)

Process step 1 : Pre-process data : ------------
1) remove names from the text file
2) remove punctuations
3) remove stop words
 self.stopwords = nltk.corpus.stopwords.words("english")
 tokens = [w for w in tokens if not w in self.stopwords]

4) filter suffixes, etc.
 self.stemmer = nltk.PorterStemmer()
 tokens = [self.stemmer.stem(w) for w in tokens]
 
when to scale/normalize words ??????


Step 2: Feature Extraction : ------------  [ scipy.sparse ]
0) (tokenization, counting and normalization) is called the Bag of Words
1) word-count matrix
1.1) Normalize with "the"
docs[tip.text]['tf'][token] = tokens.count(word) / float(tokens.count("the"))
2) word-TFIDF matrix
3) dictionary of tokens

n-gram ????

//feature extraction : dictionary
def word_features(words):
  return dict((word, True) for word in words)
or
sklearn.feature_extractionDictVectorizer
or
sklearn.feature_extraction.text
CountVectorizer : token-count matrix
or ---
tf_transformer = sklearn.feature_extraction.text.TfidfTransformer(use_idf=True).fit(X) # norm="l2": sparse matrix, [n_samples, n_features]
X = tf_transformer.transform(X)
or
TfidfVectorizer : token-TFIDF matrix
fit() : construct token dictionary given dataset
transform() : generate numerical matrix
vectorizer = TfidfVectorizer(min_df=1) # min_df=1 or 0.01, max_features=None
vectorizer.fit_transform(corpus)  #input: iteratable documents_Set; output: matrix[n_samples, n_features]

//-----


Step 3: Feature selection : ------------
1) calculate info-gain OR CHI

sklearn.feature_selection.chi2(X, y) # X = matrix{samples, features}, Y{class-labels}

/ R : sklearn.feature_selection.chi2
information.gain(formula, data)

weights <- chi.squared(Class~., HouseVotes84)  #or information.gain()
print(weights)
subset <- cutoff.k(weights, 5)
f <- as.simple.formula(subset, "Class")
print(f) 
*/


Step 4: Train and test : ------------
1) Prepare for classification
2) Feed into SVM , NB, SOM ?

//import scikit : SVM 
vec = Vectorizer(analyzer)
features = vec.fit_transform(list_of_documents)
clf = sklearn.svm.LinearSVC(C=100).fit(features, labels)

sklearn.grid_search # for C and gamma

clf2 = picklel.loads(pickle.dumps(clf))
predicted_labels = clf2.predict(features_of_new_docs)
//-----

// NBC
neg_examples = [(features(reviews.words(i)), 'neg') for i in neg_ids]
pos_examples = [(features(reviews.words(i)), 'pos') for i in pos_ids]
train_set = pos_examples + neg_examples

clf = sklearn.naive_bayes.MultinomialNB()
clf.fit(X,Y)


classifier.show_most_informative_features()
//------

// Nearest Neighbour
n_neighbors = 11
weights = 'uniform'
weights = 'distance'
clf = sklearn.neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
clf.fit(X_train, y_train)

y_predicted = clf.predict(X_test)


Step 5: Evaluate : ------------
sklearn.metrics.classification_report(y_test, y_predicted, target_names=y_names)
sklearn.metrics.confusion_matrix(y_test, y_predicted)

sklearn.metrics.precision_score
recall_score
f1_score

matPlotlib.pyplot


Step 6: K-fold validation (Optional):  ------------
sklearn.cross_validation.KFold()
train_index
test_index

*/

