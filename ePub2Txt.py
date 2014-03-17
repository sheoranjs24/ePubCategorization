import os, sys, re
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit

booksDir = sys.argv[1]
txtFileDir = sys.argv[2]


# scan all the content files for all books, and return an array of the content file list
def ScanContents(rootdir):
	contentList = []
	for dirname, subdirs, files in os.walk(rootdir):
		for fname in files:
			name, ext = os.path.splitext(fname)
			# print name, ext
			if ext == ".html" or ext == ".xhtml" or ext == ".htm":
				# print os.path.join(dirname, fname)
				contentList.append(os.path.join(dirname, fname))

	# print contentList
	return contentList

# parse contents in each html file
def parseContents(contentList):
	for fullFilename in contentList:
		# print fullFilename
		nameList = re.findall('/(.*)\.epub', fullFilename, re.DOTALL)
		filename = os.path.basename(nameList[0])
		# print filename

		# start to read contents from the file
		soup = BeautifulSoup(open(fullFilename))
		# print soup.original_encoding
		soup.encode("utf-8")
		pTagList = soup.find_all('p')
		textList = []
		for pTag in pTagList:
			if len(pTag.get_text()) > 0:
				try:
					txt = pTag.get_text().decode("utf-8")
					textList.append(txt)
					# print txt
				except Exception, e:
					print 'except'
					pass
		
		if len(textList) > 0:
			saveContents(filename+".txt", textList)

# save parsed contents of each book in a specific direcoty with its genre name and ordered number
def saveContents(filename, contentsList):
	fullFilename = os.path.join(txtFileDir, filename)
	# print "fullFilename", fullFilename

	try:
		fhandler = open(fullFilename, 'a')
		for content in contentsList:
			fhandler.write(content+'\n')

		fhandler.close()
	except Exception, e:
		raise e


# main callee
def main():
	if len(sys.argv) < 3:
		print "........\nmiss arguments\n........"
		return

	contentList = ScanContents(booksDir)
	parseContents(contentList)
	

# where start to wrok
if __name__ == '__main__':
	main()
