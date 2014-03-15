from sklearn import svm
from pprint import pprint
import json, os, sys, string
import operator

# create universal words dictionary

def createUniDict(filename):
	jsonData = open(filename)
	datasets = json.load(jsonData)
	# pprint(datasets[0][5])
	# pprint(len(datasets))

	uniDict = {}
	for subset in datasets:
		# the word dict is located in the 5th position
		for word in subset[5]:
			wcount = subset[5][word]
			# pprint(subset[5][word])
			if word in uniDict:
				uniDict[word] += wcount
			else:
				uniDict[word] = wcount

	jsonData.close()

	# pprint(len(uniDict))
	sorted_x = sorted(uniDict.iteritems(), key=operator.itemgetter(1))
	# pprint(sorted_x)

	for item in sorted_x:
		type(item)

	return uniDict

# extract word frequency dict from the preprocessing data
def extractIndivWFDict(filename):
	pass


def main():
	createUniDict(sys.argv[1])


if __name__ == '__main__':
	main()