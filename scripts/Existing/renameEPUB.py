#   
#   Peter Salomonsson
#   renameEPUB.py : utility
#   AA_NN.epub.zip -> AA-NN.epub
#   Input:  
#   Output: 
#   Version 1.0
#   16 March 2014
#   

import os, sys, string

        
def main():

    # Setup directory and file structure variables
    ePubPath = os.getcwd() + "\\Data files\\1rawepub\\"
    
    dirList = os.listdir(ePubPath)
    
    count = 0                       
    for file in dirList: 
        if file.find("_") == 2:
            newName = file[0:2]+"-"+file[3:(len(file)-4)]
            print newName
            os.rename(ePubPath+file, ePubPath+newName)

    print "done"        
    
if __name__ == '__main__':
    main()        