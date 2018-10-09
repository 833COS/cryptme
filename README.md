cryptme.py
encryption script

20170727

Simple XOR encryption program.

User provided passphrase is hashed to create a high degree of entropy; the hash 
is rehashed against itself until it equals or exceeds the length of the message to be 
encrypted.

Version 3 - Uses SHA-512 hash.
Breaks target file into chunks for faster processing of larger files. 
Default 1 MB chunks. 
