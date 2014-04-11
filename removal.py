import os, sys, re


booksDir = sys.argv[1]

def detection(rootdir):
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

# main callee
def main():
	if len(sys.argv) < 3:
		print "........\nmiss arguments\n........"
		return


# where start to wrok
if __name__ == '__main__':
	main()