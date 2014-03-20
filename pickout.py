import os, sys, re
import shutil

rawEPubFolder = sys.argv[1]
pickoutFolder = sys.argv[2]

# scan all the content files for all books, and return an array of the content file list
def ScanContents(rootdir):
	contentList = []
	for dirname, subdirs, files in os.walk(rootdir):
		for fname in files:
			name, ext = os.path.splitext(fname)
			if ext == ".html" or ext == ".xhtml" or ext == ".htm":
				contentList.append(os.path.join(dirname, fname))

	return contentList

# parse contents in each html file
def parseContents(contentList):
	for fullFilename in contentList:
		basename = ""
		epubNames = re.findall('/.*\.epub', fullFilename, re.DOTALL)
		ibooksNames = re.findall('/.*\.ibooks', fullFilename, re.DOTALL)
		if len(epubNames) > 0:
			basename = os.path.basename(epubNames[0])
		elif len(ibooksNames) > 0:
			basename = os.path.basename(ibooksNames[0])

		# the basename of the content file(xxx.html/htm/xhtml)
		htmlBasename = os.path.basename(fullFilename)
		# print htmlName

		if len(basename) > 0:
			# create dest epub folder name by contatinating pickoutFolder and epubName together
			destFolder = os.path.join(pickoutFolder, basename)
			if not os.path.exists(destFolder):
				os.makedirs(destFolder)

			# create the full name of the content file in the destination folder
			fullHtmlFilename = os.path.join(destFolder, htmlBasename)
			# exactly copy file
			shutil.copyfile(fullFilename, fullHtmlFilename)


# main callee
def main():
	if len(sys.argv) < 3:
		print "........\nmiss arguments\n........"
		return

	contentList = ScanContents(rawEPubFolder)
	parseContents(contentList)
	

# where start to wrok
if __name__ == '__main__':
	main()	