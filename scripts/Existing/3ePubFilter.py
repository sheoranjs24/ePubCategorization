#   
#   Peter Salomonsson
#   3ePubFilter.py : step 3 plain text file input TO text file output in various formats
#   Reads plain text files and filters various factors to create attribute set
#   Input:  plain text file
#   Output: plain text file: arff, SVM (one file for each class)
#   Version 1.3  - debugged threshold, BwW and screen output
#   19 March 2014
#   Reads plain Text files and transforms into word frequency text files 
#       WF (word freq) in a book 
#       tF ('the' freq) in a book [used to normalize WF]
#       nB total number of books
#       BwW total books with the word
#       IBF (inverse book frequency) = nB / BwW
#       table contains floats SQRT(WF/tF x IBF) values between 0 and 0.788
#   

import os, sys, string, json
from stemming import porter2

def filterNamesA(line, prePunctFlag, nameList):
    strippedLine = ""

    for word in line.split():
        punctFlag = 0
        lockFlag = 0
        for c in ".;:)}]>/\|-":    
            place = word.find(c)
            if place > -1:
                if place < (len(word)-1):
                    word = word[:place+1]+" "+word[place+1:]
                    word, punctFlag, nameList = filterNamesA(word, prePunctFlag, nameList)
                else:
                    punctFlag = 1
                    lockFlag = 1
            else:
                if lockFlag == 0: 
                    punctFlag = 0
        if word[0] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if prePunctFlag == 1: 
                strippedLine += " "+word
            else:
                nameList.append(filterPunctuation(word))
        else:
            strippedLine += " "+word
        prePunctFlag = punctFlag
        
    return strippedLine, prePunctFlag, nameList    

    
def filterNamesB(line, namesDic):
    strippedLine = ""

    for word in line.split():
        plainWord = filterPunctuation(word)
        if plainWord not in namesDic:
            strippedLine += " "+word
#        else:
#            print plainWord
        
    return strippedLine    

    
def loadStopwords(stopPathFile):
    stopwords = ""
    try:
        stopwordFile = open(stopPathFile)
        for line in stopwordFile:
            stopwords += line
        return stopwords    
    except IOError:   
        print "IOError loadStopwords"  

    
def filterStopwords(stopwords, line):
    strippedLine = ""
    for word in line.split():
        if stopwords.find(" "+word.lower()+" ") == -1:
            strippedLine += (" "+word)
    return strippedLine

    
def filterNumbers(line):
    return line.translate(string.maketrans("1234567890","          "))      # exchange numerics for space
    
    
def filterPunctuation(line):
    strippedLine = ''.join([i if ord(i) < 128 else ' ' for i in line])          # remove non-ascii characters
    strippedLine = strippedLine.translate(string.maketrans("-[]'","    "))      # exchange joining chars for space
    strippedLine = strippedLine.replace("'s "," ")                              # remove possessive and 's for is
    return strippedLine.translate(string.maketrans("",""), string.punctuation)  # remove punctuation

def stemmingLine(line):
    stemmedLine = ""
    for word in line.split():
        stemmedLine += (" "+porter2.stem(word))
    return stemmedLine


def filterBooks(IOdic, stateDic):
    dirList = os.listdir(IOdic["path"]["text"])
    if stateDic["debugState"] == 1: print dirList
    stopwords = loadStopwords(IOdic["path"]["stop"]+IOdic["fileIN"]["stop"])
    if stateDic["debugState"] == 1: print stopwords
    nameDic = {}

    count = 0                                                                           # progress counter
    totalCount = len(dirList)
    for file in dirList:                                                                # for each raw data book file
        count += 1                                                                      #   advance progress counter
        if (count % totalCount/10): print "names stage A book "+str(count)+" of "+str(len(dirList))                     #   display progress
        if stateDic["logState"] == 1:                                                   #   if logging then 
            logBook = open(IOdic["path"]["post"] + "logB-"+file,'w')                     #     open log file                 
            logBook.write("filtering book "+str(count)+" of "+str(len(dirList))+"\n")   #     write book count                 
        try:                                                                            #   try with raw book files input and pre-processed output data
            textBook = open(IOdic["path"]["text"] + file)                               #     open input file
            postBook = open(IOdic["path"]["post"] + file,'w')                           #     open output file                 
            prePunctFlag = 1
            for line in textBook:                                                       #     for each line in a textbook 
                if stateDic["debugState"] == 1: print line                              #       if debug then display line
                if stateDic["nameState"] == 1:                                          #       if names then remove identifiable names
                    line, prePunctFlag, newNames = filterNamesA(line, prePunctFlag, [])      #         remove identifiable names
                    for name in newNames:
                        if name not in nameDic: nameDic[name] = 1
                        else: nameDic[name] += 1
                postBook.write(line)                                                    #       write data to preProcessedBook output text file
                if stateDic["logState"] == 1:                                           #       if logging then
                    logBook.write("\n line written to file \n")                         #         write to log
            textBook.close()                                                            #     close text input file
            postBook.close()                                                            #     close post-processed output file
            if stateDic["logState"] == 1: logBook.close()                               #     if logState then close log file
        except IOError:                                                                 #   detect IO error  
            print "IOError preProcessBooks()"                                           #     notify of IO error

    count = 0                                                                           # progress counter
    for file in dirList:                                                                # for each raw data book file
        count += 1                                                                      #   advance progress counter
        if (count % totalCount/10): print "filtering book "+str(count)+" of "+str(len(dirList))                     #   display progress
        if stateDic["logState"] == 1:                                                   #   if logging then 
            logBook = open(IOdic["path"]["post"] + "log-"+file,'w')                     #     open log file                 
            logBook.write("filtering book "+str(count)+" of "+str(len(dirList))+"\n")   #     write book count                 
        try:                                                                            #   try with raw book files input and pre-processed output data
            textBook = open(IOdic["path"]["text"] + file)                               #     open input file
            postBook = open(IOdic["path"]["post"] + file,'w')                           #     open output file                 
            for line in textBook:                                                       #     for each line in a textbook 
                if stateDic["debugState"] == 1: print line                              #       if debug then display line
                if stateDic["nameState"] == 1:                                          #       if names then remove identifiable names
                    line = filterNamesB(line, nameDic)                                  #         remove identifiable names
                    if stateDic["debugState"] == 1: print line                          #         if debug then display line
                if stateDic["lowerState"] == 1:                                         #       if lower then make lower case
                    line = line.lower()                                                 #         convert line to lower case line
                    if stateDic["debugState"] == 1: print line                          #         if debug then display line
                if stateDic["punctuationState"] == 1:                                   #       if punctuation to be removed
                    line = filterPunctuation(line)                                      #         remove punctuation
                    if stateDic["debugState"] == 1: print line                          #         if debug then display line
                if stateDic["numberState"] == 1:                                        #       if numbers to be removed
                    line = filterNumbers(line)                                          #         remove numbers
                    if stateDic["debugState"] == 1: print line                          #         if debug then display line
                if stateDic["stopState"] == 1:                                          #       if stop words to be removed
                    line = filterStopwords(stopwords, line)                             #         remove stop words
                    if stateDic["debugState"] == 1: print line                          #         if debug then display line
                if stateDic["stemmingState"] == 1:                                      #       if words to be stemmed
                    line = stemmingLine(line)                                           #         stem words
                    if stateDic["debugState"] == 1: print line                          #         if debug then display line
                postBook.write(line)                                                    #       write data to preProcessedBook output text file
                if stateDic["logState"] == 1:                                           #       if logging then
                    logBook.write("\n line written to file \n")                         #         write to log
            textBook.close()                                                            #     close text input file
            postBook.close()                                                            #     close post-processed output file
            if stateDic["logState"] == 1: logBook.close()                               #     if logState then close log file
        except IOError:                                                                 #   detect IO error  
            print "IOError preProcessBooks()"                                           #     notify of IO error

            
def wordCount(IOdic, stateDic): 

    dirList = os.listdir(IOdic["path"]["post"])
    numFiles = len(dirList)
    if stateDic["debugState"] == 1: print dirList

    fileCount = -1
    bookCountList = []
    wordDic = {}
    print "\nraw word count"       
    for file in dirList:                                                    # for each pre-processed data book file
        fileCount += 1
        if (fileCount+1) % (numFiles/10) == 0: print "rwc book: "+str(fileCount+1)+" of "+str(numFiles)
        fileParts = file.split(".",1)[0].split("-")
        wordCountDic = {}                                                   # dictionary of word counts per book
        theCount = 0.0                                                      # count of 'the' contained in a book
        wordCount = 0.0                                                     # count of word contained in a book
        BwWdic ={}                                                          # count of books containing a word
        bookCountList.append([fileCount, fileParts[0], fileParts[1], wordCountDic, theCount, wordCount]) # without sub-genre
        try:                                                                #   try with pre-processed input data
            postBook = open(IOdic["path"]["post"] + file)                   #     open input file                 
            for postLine in postBook:                                       #     for each preline in a prebook 
                words = postLine.split()                                    #       list of words in line
                for word in words:                                          #       for each word in words
                    if word == "the":                                       #         if word ie 'the'
                        bookCountList[fileCount][4] += 1.0                  #           increment 'the' count
                    else:                                                   #         else
                        if word not in bookCountList[fileCount][3]:         #           if word not in book dictionary - without sub-genre
                            bookCountList[fileCount][3][word] = 1.0         #             add word to  book dictionary 
                        else:                                               #           else
                            bookCountList[fileCount][3][word] += 1.0        #             increment word count in book dic
                        wordDic[word] = 1        
                    bookCountList[fileCount][5] += 1.0                      #         increment total word count in book dic
            postBook.close()        
        except IOError:                                                     #   detect IO error  
            print "IOError wordCount()"                                     #     notify of IO error
    print "len word dic: "+str(len(wordDic))

    refWordCount = 0
    totalWordCount = len(wordDic)
    print "\ncalculate BwW"
    for refWord in wordDic:
        refWordCount+=1
        if (refWordCount % (totalWordCount/10)) == 0: print "BwW word: "+str(refWordCount)+" of "+str(totalWordCount)
        for book in bookCountList:
            if refWord in book[3]:
                if refWord not in BwWdic:
                    BwWdic[refWord] = 1.0
                else:
                    BwWdic[refWord] += 1.0
            else:
                book[3][refWord] = 0.0
    
    print "\nstart writing BwW count dic to json file"
    countFile = open(IOdic["path"]["count"]+IOdic["fileIO"]["BwW"],'w')                                     #  open output file                 
    json.dump(BwWdic, countFile)
    countFile.close()
    print "finished writing json dic len: "+str(len(BwWdic))

    tBwWdic = BwWdic.copy()
    if stateDic["wordThreshold"] > 0: 
        print "\nthreshold BwW remove all words with frequency below: "+str(stateDic["wordThreshold"])       
        for refWord in BwWdic:
            if BwWdic[refWord] < stateDic["wordThreshold"]:
                for book in bookCountList:
                    if book[3][refWord] > 0: book[5] -= 1
                    book[3].pop(refWord, None)
                    tBwWdic.pop(refWord, None)
    print "\nstart writing BwW count dic after threshold to json file"
    countFile = open(IOdic["path"]["count"]+"T"+IOdic["fileIO"]["BwW"],'w')                                     #  open output file                 
    json.dump(tBwWdic, countFile)
    countFile.close()
    print "finished writing json dic len: "+str(len(tBwWdic))
    BwWdic = tBwWdic.copy()
               
    print "\normalize wordcount"
    maxFactor = 0.0
    bookCount = 0
    totalBooks = len(bookCountList)
    for book in bookCountList:
        bookCount+=1
        if (bookCount % (totalBooks/10)) == 0: print "normalize book: "+str(bookCount)+" of "+str(len(dirList))
#        for word in book[5]:
#            if book[5][word] != 0.0:
#                book[5][word] = ((book[5][word]/book[6])*(len(bookCountList)/BwWdic[word]))**(0.5)
#                if book[5][word] > maxFactor:
#                    maxFactor = book[5][word]
        for word in book[3]:
            if book[3][word] != 0.0:
                if book[4] == 0: 
                    print book[1]+str(book[2])+" the: "+str(book[4])
                    book[4] = 1
                if BwWdic[word] == 0: 
                    print book[1]+str(book[2])+" BwW: "+word+" = "+str(BwWdic[word])
                    BwWdic[word] = 1
                book[3][word] = ((book[3][word]/book[4])*(len(bookCountList)/BwWdic[word]))**(0.5)
                if book[3][word] > maxFactor:
                    maxFactor = book[3][word]
#        aBookFile = open(countPathFile.replace(".", str(bookCount-1)+"."),'w')  #  open output file                 
#        json.dump(book, aBookFile)
#        aBookFile.close()
 
#        keyWordsFile = open(countPathFile.replace(".", "KWF."),'w')  #  open output file                 
#        for item in bookCountList[0][5]:
#            keyWordsFile.write(item+"\n")
#        keyWordsFile.close()
                                                                  
    print "\nmaxFactor: "+str(maxFactor)
    
    print "\nstart writing wordcount json file"
    countFile = open(IOdic["path"]["count"]+IOdic["fileIO"]["count"],'w')                                     #  open output file                 
    json.dump(bookCountList, countFile)
    countFile.close()
    print "finished writing json file"
            
    return bookCountList        


def checkIOstructure(IOdic):
    
    for path in IOdic["path"]:
        if not os.path.exists(IOdic["path"][path]):
            os.makedirs(IOdic["path"][path])

    for file in IOdic["fileIN"]:
        if IOdic["fileIN"][file] == "*.*":
            if len(os.listdir(IOdic["path"][file])) == 0:
                print "Error: cannot find any input files: "+IOdic["path"][file]+IOdic["fileIN"][file]
                return -1
        else:
            if not os.path.exists(IOdic["path"][file]+IOdic["fileIN"][file]): 
                print "Error: cannot find: "+IOdic["path"][file]+IOdic["fileIN"][file]
                return -2
    
    return 1

    
def loadBookCountList(IOdic):
    countFile = open(IOdic["path"]["count"]+IOdic["fileIO"]["count"])   #  open input file                 
    bookCountList = json.load(countFile)
    countFile.close()
    return bookCountList
        
            
def createWEKAarff(IOdic, bookCountList): 
   
        arffFile = open(IOdic["path"]["arff"]+IOdic["fileIO"]["arff"],'w')  #  open output file                 
        print "header" 
        arffFile.write("\n@relation book-genre\n\n")                        #  write data to preProcessedBook output text file
        class1List = ""
#        class2List = ""
        for bookLine in bookCountList:
#            if bookLine[3] not in class2List:
#                class2List += bookLine[3]+","
#        header = "@ATTRIBUTE instance NUMERIC\n@ATTRIBUTE class1 {" + class1List[:(len(class1List)-1)] + "}\n@ATTRIBUTE class2 {" + class2List[:(len(class2List)-1)] +"}\n"
            if bookLine[1] not in class1List:
                class1List += bookLine[1]+","
        header = "@ATTRIBUTE instance NUMERIC\n@ATTRIBUTE class1 {" + class1List[:(len(class1List)-1)] + "}\n"
        wordDic = {}
        for wordKey in bookCountList[0][3]:
            header += "@ATTRIBUTE " + wordKey + " NUMERIC\n"
            wordDic[wordKey] = 1
        arffFile.write(header+"\n")                             #            write data to preProcessedBook output text file
        print "bookLine"
        arffFile.write("\n@DATA\n")                             #            write data to preProcessedBook output text file
        lineCount = 0
        totalLines = len(bookCountList)
        for book in bookCountList:
            lineCount += 1
            if (lineCount % (totalLines/10)) == 0: print "bookLine: " + str(lineCount)+" of "+str(totalLines)
            fileLine = str(book[0]) + "," + book[1]
#            for wordKey in bookCountList[0][3]:
            for wordKey in wordDic:
                fileLine += "," + str(book[3][wordKey])
            arffFile.write(fileLine+"\n")                        #            write data to preProcessedBook output text file
        arffFile.close()
        
        
def createSVM(IOdic, bookCountList): 
   
        SVM2Dfile = open(IOdic["path"]["SVM"]+IOdic["fileIO"]["SVM2D"],'w')  #  open output file
        
        header = ""
        for bookLine in bookCountList:
            header += str(bookLine[0])+","
        header = header[:-1]
        SVM2Dfile.write(header+"\n")    
        wordCount = 0
        totalWords = len(bookCountList[0][3])
        for word in bookCountList[0][3]:
            wordCount += 1
            if (wordCount % (totalWords/10)) == 0: print "word: "+str(wordCount)+" of "+str(totalWords)
            line = ""
            for bookLine in bookCountList:
                line += str(bookLine[3][word])+","
            line = line[:-1]    
            SVM2Dfile.write(line+"\n")    
        SVM2Dfile.close()
        
        classList = []
        for bookLine in bookCountList:
            aClass = bookLine[1]
            if aClass not in classList:
                classList.append(aClass)
                SVM1Dfile = open(IOdic["path"]["SVM"]+"SVM-"+aClass+".txt",'w')  #  open output file
                line = ""
                for aBook in bookCountList:
                    if aBook[1] == aClass:
                        line += "1,"
                    else:
                        line += "0,"
                line = line[:-1]
                SVM1Dfile.write(line+"\n")    
                SVM1Dfile.close()
                
            
        
def main():

    # Setup directory and file structure variables
    IOdic = {}
    pathDic = {}
    fileINdic = {}
    fileIOdic = {}
    pathDic["text"] = os.getcwd() + "\\Data files\\2preePub2txt\\"
#    pathDic["text"] = os.getcwd() + "\\Data files\\2preePub2txtTest\\"
    fileINdic["text"] = "*.*"
    pathDic["post"] = os.getcwd() + "\\Data files\\3ePubFiltered\\"
    pathDic["stop"] = os.getcwd() + "\\Data files\\stopwords\\"
#    fileINdic["stop"] = "stopwordsmysql.txt"
#    fileINdic["stop"] = "stopwordspbjs.txt"
    fileINdic["stop"] = "stopwordspbjsrm.txt"
    pathDic["count"] = os.getcwd() + "\\Data files\\4ePubwordcount\\"
    fileIOdic["count"] = "wordcount.txt"
    fileIOdic["BwW"] = "BwWcount.txt"
    pathDic["training"] = os.getcwd() + "\\Data files\\5ePubtraining\\"
    pathDic["arff"] = pathDic["training"] + "\\weka\\"
    fileIOdic["arff"] = "wekaRaw.arff"
    pathDic["SVM"] =  pathDic["training"] + "\\SVM\\"
    fileIOdic["SVM2D"] = "SVM2D.txt"
    IOdic["path"] = pathDic
    IOdic["fileIN"] = fileINdic
    IOdic["fileIO"] = fileIOdic
    
    # Set up the options to use in processing the books
    stateDic = {}
    stateDic["filterState"] = 0             # 0 = Off, 1 = On  
    stateDic["nameState"] = 1               # 0 = Off, 1 = On  remove names
    stateDic["lowerState"] = 1              # 0 = Off, 1 = On  make all lower case
    stateDic["punctuationState"] = 1        # 0 = Off, 1 = On  removal of punctuation
    stateDic["numberState"] = 1             # 0 = Off, 1 = On  removal of numbers
    stateDic["stopState"] = 1               # 0 = Off, 1 = On  removal of stop words
    stateDic["stemmingState"] = 1           # 0 = Off, 1 = On  stemming words

    stateDic["wordCountState"] = 1          # 0 = Off, 1 = On
    stateDic["wordThreshold"] = 3           # words with count lower than threshold across all books are ignored
    
    stateDic["formatFilesState"] = 1        # 0 = Off, 1 = On  
    
    stateDic["debugState"] = 0              # 0 = Off, 1 = On  print statements active
    stateDic["logState"] = 0                # 0 = Off, 1 = On  log file active
    
   
    if checkIOstructure(IOdic) == 1:

        # Commence book processing
        if stateDic["filterState"] == 1: 
            filterBooks(IOdic, stateDic)
    
        if stateDic["wordCountState"]  == 1: 
            wordCountList = wordCount(IOdic, stateDic)
            print "\ninst book len(dic) theCount wordCount"
            totalWords = len(wordCountList)
            for bookCount in xrange(totalWords): 
                if  (bookCount % (totalWords/10)) == 0: 
                    print ("%4d %s-%s %7d %6.0f %8.0f" % (bookCount, wordCountList[bookCount][1], wordCountList[bookCount][2], len(wordCountList[bookCount][3]), wordCountList[bookCount][4], wordCountList[bookCount][5]) )
#                    print("%4d %s-%s " % (bookCount, wordCountList[bookCount][1], wordCountList[bookCount][2]) )
        if stateDic["formatFilesState"] == 1:
            print "\nreading json bookCountList file"
            bookCountList = loadBookCountList(IOdic)
            print "\nformatting arff file"
            createWEKAarff(IOdic, bookCountList)
            print "\nformatting SVM files"
            createSVM(IOdic, bookCountList)

    print "\ndone"        
    
if __name__ == '__main__':
    main()        