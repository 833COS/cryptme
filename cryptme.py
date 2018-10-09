#!/usr/bin/python3

"""
#Matt Hayes
#cryptme.py
#20170727
#
#Simple XOR encryption program.
#
#User provided passphrase is hashed to create a high degree of entropy; the hash 
#is rehashed against itself until it equals or exceeds the length of the message to be 
#encrypted.
#
#Version 3 - Uses SHA-512 hash.
#Breaks target file into chunks for faster processing of larger files. 
#Default 1 MB chunks. 
"""


#-------------------------------------------------------
#Import capabilities!
#-------------------------------------------------------
import sys  	#Accept command line arguments with sys.argv
import hashlib  #Hashing functions
import os		#Determine file size
#-------------------------------------------------------



#--------------------------------------------------------
#Usage function
#--------------------------------------------------------
def usage():
    print ("Usage: ")
    print ("./cryptme.py [-h]")
    print ("./cryptme.py [-i <target>] [-o <output>] [-p <passphrase>]")
    print ("")
    print ("Options:")
    print ("-h:  Display this menu.")
    print ("")
    print ("-i <target file to encrypt or decrypt>")
    print ("\tdefault:  User will be prompted for keyboard input.")
    print ("")
    print ("-o <file to create; result of encrypt or decrypt operation>")
    print ("\tdefault:  A file named \"result\" will be created in the local folder.")
    print ("")
    print ("-p <passphrase>")
    print ("\tdefault:  User will be prompted for keyboard input.")
    print ("")
    sys.exit()
#-------------------------------------------------------------




#-------------------------------------------------------
#Set default option switches!
#-------------------------------------------------------
target = "" #If not specified, prompt for keyboard input.
output = "result.file"
passPhrase = "" #Prompt for keyboard input.
ord_pass = []
#-------------------------------------------------------



#-------------------------------------------------------
#Parse the cmd line options
#-------------------------------------------------------
#Determine if the index (x) wraps around to [0].  If so, 
#no valid option was specified for the given switch.
#(sys.argv's index moves from last position to first)
x = 0
for arg in sys.argv:
    #Read the cmd line arguments for various options.
    if arg == "-h" or arg == "/h" or arg == "--help":
        usage()
    if arg == "-i" or arg == "/i":
        if sys.argv[x+1] == sys.argv[0]:
            usage()
        target = sys.argv[x+1]
    if arg == "-o" or arg == "/o":
        if sys.argv[x+1] ==sys.argv[0]:
            usage()
        output = sys.argv[x+1]
    if arg == "-p" or arg == "/p":
        if sys.argv[x+1] == sys.argv[0]:
            usage()
        passPhrase = sys.argv[x+1]
    x += 1
	
if len(sys.argv) < 2:
	usage()
#------------------------------------------------------


#------------------------------------------------------
#Begin entropy and encryption
#------------------------------------------------------
if passPhrase == "":
    #no passphrase or filepath was given...
    print ("")
    passPhrase = input("Enter the encryption passphrase:  ")

#Hash the passphrase to create maximum entropy.
pass_hash = hashlib.sha512(passPhrase.encode('utf-8')).hexdigest()
ph_copy = pass_hash		#Make a copy of the pw hash for processing


#Determine if the file is big enough to split into chunks.
chunkSize = (1 * 1024 * 1024)	#1 MB
index = 0
endPoint = os.path.getsize(target)

if endPoint <= chunkSize:	#If the file is smaller than 1 MB
	chunkSize = endPoint

#Set pw hash to proper length for XOR'ing against current chunkSize
print("Increasing entropy...  ")
while len(ph_copy) < chunkSize:
	ph_copy += hashlib.sha512(ph_copy.encode('utf-8')).hexdigest()

#Convert the extended hash to ord for processing
ord_pass = []
for l in ph_copy:
	ord_pass.append(ord(l))
print("Entropy achieved.\n\n")


#if endPoint > chunkSize:
print("Reading target file...")
file_target = open(target, "rb")	#Open target for reading bytes
file_target.seek(0)				#Start at the beginning
result = open(output, "ab")		#Open outfile for appending bytes
	
	
#Determine number of file chunks required for completion - 
#inform user of status during processing.
# x is the current part, of y total parts.
x = 0
y = int(endPoint / chunkSize)
if endPoint % chunkSize > 0:
	y += 1

while index < endPoint:		#Process 1 MB parts until EOF
	x += 1
	print("Processing part " + str(x) + " of " + str(y) + "...")
	index += chunkSize		#Update file index variable
	data = file_target.read(chunkSize)	#Read current 1 MB block
		
	#Process XOR on this chunk...
	xResult = bytearray(a^b for a,b in zip(ord_pass, data))
		
	#Append the result to output file
	result.write(xResult)
print(output + " complete!")
#-----------------------------------------------------------


#Cleanup at the end.
data = None
ph_copy = None
ord_pass = None
file_target.close()
result.close()