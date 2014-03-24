# class_file should contain one array containing genre. e.g. ["romance", "fiction"]
#
# load genre files
import numpy
genreBI = numpy.loadtxt("SVM-BI.txt", delimiter=',', dtype="int_")
genreSP = numpy.loadtxt("SVM-SP.txt", delimiter=',', dtype="int_")
genreFN = numpy.loadtxt("SVM-FN.txt", delimiter=',', dtype="int_")
genreGD = numpy.loadtxt("SVM-GD.txt", delimiter=',', dtype="int_")
genreHI = numpy.loadtxt("SVM-HI.txt", delimiter=',', dtype="int_")
genreHR = numpy.loadtxt("SVM-HR.txt", delimiter=',', dtype="int_")
genreMI = numpy.loadtxt("SVM-MI.txt", delimiter=',', dtype="int_")
genreRG = numpy.loadtxt("SVM-RG.txt", delimiter=',', dtype="int_")
genreRM = numpy.loadtxt("SVM-RM.txt", delimiter=',', dtype="int_")
genreSF = numpy.loadtxt("SVM-SF.txt", delimiter=',', dtype="int_")

# final data array
Y_train = []

# loop over each file and save the class
for x in genreBI:
	if (x == 1):
		Y_train.append("BI")
	else:
		Y_train.append("0")

pos = -1
for x in genreSP:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "SP"

pos = -1
for x in genreFN:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "FN"

pos = -1
for x in genreGD:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "GD"

pos = -1
for x in genreHI:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "HI"

pos = -1
for x in genreHR:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "HR"

pos = -1
for x in genreMI:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "MI"

pos = -1
for x in genreRG:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "RG"

pos = -1
for x in genreRM:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "RM"

pos = -1
for x in genreSF:
	pos = pos + 1
	if (x == 1):
		Y_train[pos] = "SF"

numpy.save("Y_train", Y_train)

# FINISH: ************************************************************************************