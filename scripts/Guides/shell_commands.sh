
# select column 2
#right now I have this line, and it worked until I had whitespace in the second field.
svn status | grep '\!' | gawk '{print $2;}' > removedProjs

#will print all but very first column:
cat somefile | awk '{$1=""; print $0}'    
#will print all but two first columns:
cat somefile | awk '{$1=$2=""; print $0}'