# Import data
read.table("file.dat", sep = "\t", header = TRUE, fileEncoding = "UTF-8", row.names = 1, quote = "", blank.lines.skip = FALSE, strip.white = TRUE, fill = TRUE, comment.char = "")
scan(file="ex.dat", what=list(x=0, y="", z=0), flush=TRUE)
read.fwf
read.xls
read.DIF("clipboard")

# Export data
cat("2 3 5 7", "11 13 17 19", file="ex.dat", sep="\n")
write()
write.table(mydata, file="mydatafile", sep=",", col.names = NA, eol = "\r\n", qmethod = "double", quote = FALSE, fileEncoding="latin1" )
write.csv(mydata, file="mydatafile")
write.matrix()    # MASS package
write.foreign()	# foreign package : export to SAS, SPSS and Stata


# Data types
class(mydata) # display data-type of mydata
is.matrix(mydata)  # check if of this type
as.matrix(mydata)	 # convert to this type