import os, sys, re
import shutil
import plistlib

# rawEPubFolder = sys.argv[1]
pickoutFolder = sys.argv[1]
# epubPath = "/Users/leicheng/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"
genrePath = "/Users/leicheng/workspace/academic/2014Spring/CSC578D/project/tGenre/"
# epubPath = 

# scan folders in a directory
def scanFolders():	
	epubFullPathList = [os.path.join(epubPath, name) for name in os.listdir(epubPath) if os.path.isdir(os.path.join(epubPath, name))]
	# for name in epubFullPathList:
	# 	print name

	return epubFullPathList

# genre path
def genrePathFetcher():
	genreList = [os.path.join(genrePath, name) for name in os.listdir(genrePath) if os.path.isdir(os.path.join(genrePath, name))]
	return genreList

# epub path
def epubPathFetcher():
	allEPubs = []
	genreList = genrePathFetcher()
	for genre in genreList:
		epublist = [os.path.join(genre, name) for name in os.listdir(genre) if os.path.isdir(os.path.join(genre, name))]
		allEPubs = allEPubs + epublist

	return allEPubs

# parse iTunesMetadata.plist
def obtainMetadata(metadata):
	return plistlib.readPlist(metadata)

# pick out htmls and save in dest directory
# epubname: like ../BI/111111111.epub
def picker(epubname, htmlList):
	if not os.path.exists(epubname):
		os.makedirs(epubname)
	for html in htmlList:
		htmlBasename = os.path.basename(html)
		shutil.copyfile(html, os.path.join(epubname, htmlBasename))
		# print os.path.join(epubname, htmlBasename)

# pickManager
def pickManager():
	bookCnt = 0
	# epubFullPathList = scanFolders()
	epubFullPathList = epubPathFetcher()

	for epubPath in epubFullPathList:
		metadata = obtainMetadata(os.path.join(epubPath, "iTunesMetadata.plist"))
		language = unicode(metadata["primaryLanguage"], errors='ignore')
		# genre = unicode(metadata["genre"], errors='ignore')
		genre = epubPath.replace(genrePath,'')[:2]
		if language == "en":
			# create destination epub path
			destGenrePath = os.path.join(pickoutFolder, genre)
			epubBasename = os.path.basename(epubPath)
			destEpubPath = os.path.join(destGenrePath, epubBasename)
			# print destEpubPath
			# scan htmls in 
			htmlList = ScanContents(epubPath)
			# sace htmls
			picker(destEpubPath, htmlList)
			bookCnt += 1
			print genre, epubBasename
			print "bookCnt:", bookCnt


# scan all the content files for all books, and return an array of the content file list
def ScanContents(epubPath):
	contentList = []
	for dirname, subdirs, files in os.walk(epubPath):
		for fname in files:
			name, ext = os.path.splitext(fname)
			if ext == ".html" or ext == ".xhtml" or ext == ".htm":
				if "title" in name or "Title" in name or "cover" in name or "Cover" in name or "toc" in name or "copyright" in name or "disclaimer" in name or "tocConfig" in name:
					continue
				else:
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
	if len(sys.argv) < 2:
		print "........\nmiss arguments\n........"
		return

	# contentList = ScanContents(rawEPubFolder)
	# parseContents(contentList)

	# scanFolders()
	pickManager()
	

# where start to wrok
if __name__ == '__main__':
	main()	