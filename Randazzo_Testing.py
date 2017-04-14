import binascii
import string
import struct as s
import time

# open file
bf = open("./sample_data/B4 1 Victim Std.fsa", 'r')

'''
ABIF uses C-type Structs to store binary data
Python has a Struct module that can handle this:
    docs.python.org/3.0/library/struct.html
'''

# Python Struct Example, pulling the whole length all at once
start = time.clock()
print string.join(s.unpack('cccc', bf.read(4))).replace(" ", "")
print (time.clock() - start) * 100000, "ms"

bf.seek(0)  # reset iter

# Python Struct Example, one byte/char at a time
start = time.clock()
text = ''
for byte in range(0, 4):
    text += bf.read(1)
print text
print (time.clock() - start) * 100000, "ms"

bf.seek(0)

# Python's read(num_bytes) converts to strings the fastest
start = time.clock()
print bf.read(4)
print (time.clock() - start) * 100000, "ms"

bf.seek(0)
print

# TODO: Check file validity by comparing to 'ABIF'
print bf.read(4)  # Should print "ABIF"
print binascii.b2a_hex(bf.read(2))  # Version Number

''' Directory Structure, see Page 8 and 9 of ABIF spec '''
name = binascii.b2a_qp(bf.read(4))  # (SInt32) name
number = int(binascii.b2a_hex(bf.read(4)))  # (SInt32) tag number
element_type = bf.read(2)  # (SInt16) element type code
element_size = int(binascii.b2a_hex(bf.read(4)), 16)  # (SInt16) size in bytes of one element
num_elements = int(binascii.b2a_hex(bf.read(4)), 32)  # (SInt32) number of elements in item
data_size = int(binascii.b2a_hex(bf.read(4)), 32)  # (SInt32) size in bytes of item
data_offset = int(binascii.b2a_hex(bf.read(4)), 32)  # (SInt32) item's data, or offset in file
data_handle = int(binascii.b2a_hex(bf.read(4)), 32)  # (SInt32) reserved

print "--- Directory Structure ---"
print "name\t\t\t\t", name
print "tag number\t\t\t", number
print "element type\t\t", element_type
print "element size\t\t", element_size
print "number of elements\t", num_elements 
print "size in byte data\t", data_size
print "item data/offset\t", data_offset
print "reserved\t\t\t", data_handle
