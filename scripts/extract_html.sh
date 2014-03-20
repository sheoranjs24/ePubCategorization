#!/bin/sh
#------------------------------------------------------------
# This script extracts html files from a epub folder
# usage: <script_name> <epub folder path> <extracted files path>
# 
# Implementation : 
# a) Find files having name matching the pattern '.html, .htm, .xhtml'
# for each such file : copy them in new location
#
# Results :
# let source_path = /users/jyoti/ePubs  and destination = /users/jyoti/htmls
# The files will be saved in destination with same directory structure. 
# i.e. destination will have directory structure as : /users/jyoti/htmls/<source_Path directory>
#------------------------------------------------------------

# check arguments : if less than 2 or argument is not a directory then exit
if [ "$#" -ne 2 ] || ! [ -d "$1" ] || ! [ -d "$2" ] ; then
	echo "wrong arugments."  >&2
	echo "useage: <script> <source path> <destination path>"
	exit 1
fi

echo "source path: $1"
echo "destination path: $2"
echo "copying has started ..."

source_path=$1
destination=$2

# Add -v to cpio. argument is only to print file names on stdout; 
find $source_path -type f -iname "*.html" -o -iname "*.xhtml" -o -iname "*.htm" | cpio -p -d $destination/

