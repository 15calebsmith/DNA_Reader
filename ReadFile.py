"""
Collection of functions that decodes a binary stream into its native type or C struct

Libraries in use:
https://pypi.python.org/pypi/bitstruct/
DOCS --> http://bitstruct.readthedocs.io/en/latest/

Libraries we may want to use:
https://github.com/scott-griffiths/bitstring

Notes from ABIF Doc:

Name
SInt32 name; // tag name
The name field is defined as an integer but this field should be treated as an array of
four 8-bit ASCII characters. Use printable ASCII characters in the range 0x21 to
0x7E, and it is appropriate to use an mnemonic abbreviation that is descriptive of the
data item.

Tag number
SInt32 number; // tag number
The number field can be any signed 32-bit integer, but it is customary to use
positive values only, beginning with 1. It is also customary to use values less than
1000.

Element type
SInt16 elementtype; // element type code
The elementtype indicates the type of data contained in the data item. New
applications writing ABIF files should only use codes for current data types. (See
"Current data types" on page 13.)

Element size
SInt16 elementsize; // size in bytes of one element
For all supported data types, the elementsize field is redundant, since the element
size for each type is uniquely defined by the specification. You may use or ignore
this field

Number of elements
SInt32 numelements; // number of elements in item
The numelements field gives the number of elements in the data item. Note that
for the string types, an "element" is an individual character, not the string itself.

Item's size
SInt32 datasize; // size in bytes of item
The datasize field gives the number of bytes in the data item.

Offset to item's location
SInt32 dataoffset; // item's data, or offset infile
For data items of size greater than 4 bytes, the dataoffset field contains the
offset to the data in the file. dataoffset field contains the data item itself. In this case,
the data bytes are stored beginning at the high-order byte of the 32-bit field.
"""

# Note: Compile this file with into a .pyo file when complete (use -oo arg)
import bitstruct as bs
import types

'''
Example using bitstruct to test read_bytes

bitstruct is a friendly wrapper for Python's struct module
Read the docs linked above; the module is very easy to learn!
'''
# I want to create the function for read_bytes. The ABIF file format specifies
# it as an UNSIGNED 8 bit integer.
my_uint8 = bs.pack('u8', 123)  # This will pack 123 as an unsigned, 8 bit int.
ovf = bs.pack('u8', -1)
print "CAUTION: -1 becomes", bs.unpack('u8', ovf)[0]  # bitstruct uses C-type data types, so -1 will become 255!
print bs.unpack('u8', my_uint8)[0]  # unpack always returns a tuple, [0] accesses first val


# April
def read_byte(b_stream):
    # Use assert to check if a valid data type was passed to the function
    # The compiler can remove asserts and docstrings later for optimization
    # See the 'types' module for hints
    assert \
        isinstance(b_stream, types.IntType) or \
        isinstance(b_stream, types.StringType), \
        "Assert: read_byte() was given an invalid type: " + str(type(b_stream))

    return bs.unpack('u8', b_stream)[0]


# Caleb
def read_char(c_stream):
    assert \
        isinstance(c_stream, types.IntType) or \
        isinstance(c_stream, types.StringType), \
        "Assert: read_char() was given an invalid type: " + str(type(c_stream))

    return bs.unpack('s8', c_stream)[0]
    #could also be bs.unpack('t8', c_stream)[0] if it is a ascii character

# Frank
def read_word():
    pass

# April
def read_short():
    pass

# Caleb
def read_long(l_stream):
    assert \
        isinstance(l_stream, types.IntType), \
        "Assert: read_long() was given an invalid type: " + str(type(l_stream))
    return bs.unpack('s16', l_stream)[0]

# Frank
def read_float():
    pass

# April
def read_double():
    pass

# Caleb
def read_date(date_stream):
    assert \
        isinstance(date_stream, types.IntType), \
        "Assert: read_date() was given an invalid type: " + str(type(date_stream))
    return bs.unpack('s16u8u8', date_stream)

# Frank
def read_time():
    pass

# Frank
def read_pstring():
    pass

# Caleb
def read_cstring(cstring_stream, chars):
    #quick loop for getting the format for how many chars to unpack
    fmt = ''
    for _ in range(chars):
        fmt = fmt + str('u8')
    fmt = fmt + 'p1'
    assert \
        isinstance(cstring_stream, types.IntType), \
        "Assert: read_cstring() was given an invalid type: " + str(type(cstring_stream))
    return bs.unpack(fmt, cstring_stream)

# Frank
def read_thumb():
    pass

# April
def read_bool():
    pass

# Hold off on worrying about this one; it's for user-defined data structs
def read_user():
    pass
