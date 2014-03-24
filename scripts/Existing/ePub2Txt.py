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
		# nameList = re.findall('/(.*)\.epub', fullFilename, re.DOTALL)
		# filename = os.path.basename(nameList[0])
		# print filename

		basename = ""
		epubNames = re.findall('/(.*)\.epub', fullFilename, re.DOTALL)
		ibooksNames = re.findall('/(.*)\.ibooks', fullFilename, re.DOTALL)
		if len(epubNames) > 0:
			basename = os.path.basename(epubNames[0])
		elif len(ibooksNames) > 0:
			basename = os.path.basename(ibooksNames[0])

		# start to read contents from the file
		try:
			soup = BeautifulSoup(open(fullFilename))
			sp = BeautifulSoup(unicode(soup))
			textList = []
			for pTag in sp.find_all('p'):
				# print pTag
				# print pTag.string
				if len(pTag.text) > 0:					
					try:
						unicode_string = pTag.get_text()#unicode(pTag.string)
						txt = unicode_string.encode("utf-8", errors='replace')
						# txt = unicode(pTag.get_text(), errors='ignore')
						textList.append(txt)
						# print len(txt),"-->",txt
					except Exception, e:
						print 'start  *****************'
						# print len(pTag.text),":",pTag.text
						print "test \"\"   \'"
						print 'end    *****************'
						raise
						# pass
			
			if len(textList) > 0:
				saveContents(basename+".txt", textList)
			
		except Exception, e:
			print "....................."
			pass
			# raise e

# save parsed contents of each book in a specific direcoty with its genre name and ordered number
def saveContents(filename, contentsList):
	fullFilename = os.path.join(txtFileDir, filename)
	# print "fullFilename", fullFilename

	# try:
	fhandler = open(fullFilename, 'ab')
	for content in contentsList:
		try:
			fhandler.write(content+'\n')
			# print "content:", content
		except Exception, e:
			# print "ex start ##############"
			# print "content:", content
			# print "ex end  ##############"
			raise e		

	fhandler.close()


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
