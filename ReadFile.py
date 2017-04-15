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
from collections import namedtuple


# Named Tuple to store extracted directory entry fields
ABIF_Entry = namedtuple("dir_entry", "tag_name \
                                      tag_num \
                                      elem_type \
                                      elem_size \
                                      num_elem \
                                      data_size \
                                      data_offset")


def handle_data(_dir_entry, _VERBOSE=0):
    """
    Calls the correct function based on the given element type
    CAUTION: handle_data does not reset the seek position...
    It is the responsibility of the calling function to save the old seek position
    :param _file_iter: The file reader
    :param _elem_type: Enum'd data type
    :param _data_offset: The absolute file position offset to where the data resides
    :param _VERBOSE: optional print for debugging, says which function is called
    :return: the data value
    """

    if _VERBOSE:
        print "handle_data: Jumping to", element_type_enum[_dir_entry.elem_type].__name__

    _dir_entry.file_iter.seek(_dir_entry.data_offset)
    return element_type_enum[_dir_entry.data_offset]()

def read_byte(b_stream):
    """
    read_byte()
    :param b_stream: 1 byte hex string
    :return: uint8
    """
    __name__ = "byte"
    assert \
        isinstance(b_stream, types.IntType) or \
        isinstance(b_stream, types.StringType), \
        "read_byte() was given an invalid type: " + str(type(b_stream))

    return bs.unpack('u8', b_stream)[0]


# TODO: more testing on this is needed because ABIF description is somewhat ambiguous
def read_char(b_stream):
    """
    read_char()
    :param b_stream: 1 byte hex string
    :return:
    """

    __name__ = "char"
    assert \
        isinstance(b_stream, types.IntType) or \
        isinstance(b_stream, types.StringType), \
        "read_char() was given an invalid type: " + str(type(b_stream))

    assert \
        1 == len(b_stream), \
        "read_char() requires 1 byte, got " + str(len(b_stream))

    if (isinstance(b_stream, types.IntType)):
        return bs.unpack('s8', b_stream)[0]
    elif (isinstance(b_stream, types.StringType)):
        return bs.unpack('t8', b_stream)[0]


def read_word(b_stream):
    """
    read_word()
    :param b_stream: 2 byte hex string
    :return: uint16
    """

    __name__ = "word"
    assert \
        isinstance(b_stream, types.StringType), \
        "read_byte() was given an invalid type: " + str(type(b_stream))
    assert \
        2 == len(b_stream), \
        "read_byte() requires 2 bytes, got " + str(len(b_stream))

    print len(b_stream)

    return bs.unpack('u16', b_stream)


def read_short(b_stream):
    """
    read_short()
    :param b_stream: 2 byte hex string
    :return: sint16
    """

    __name__ = "short"
    assert \
        isinstance(b_stream, types.IntType), \
        "read_short() was given an invalid type: " + str(type(b_stream))

    assert \
        2 == len(b_stream), \
        "read_short() requires 2 bytes, got " + str(len(b_stream))

    return bs.unpack('s16', b_stream)[0]


def read_long(b_stream):
    """
    :param b_stream: 4 byte hex string
    :return: tuple (SInt32)
    """

    __name__ = "long"
    assert \
        isinstance(b_stream, types.IntType), \
        "read_long() was given an invalid type: " + str(type(b_stream))

    assert \
        4 == len(b_stream), \
        "read_long() requires 4 bytes, got " + str(len(b_stream))

    return bs.unpack('s16', b_stream)[0]


def read_float(b_stream):
    """
    read_float()
    :param b_stream: 4 byte hex string
    :return: float
    """

    __name__ = "float"
    assert \
        isinstance(b_stream, types.StringType), \
        "read_float() was given an invalid type: " + str(type(b_stream))
    assert \
        4 == len(b_stream), \
        "read_float() requires 4 bytes, got " + str(len(b_stream))

    return bs.unpack('f32', b_stream)


def read_double(b_stream):
    """
    read_double()
    :param b_stream: 8 byte hex string
    :return: float64
    """

    __name__ = "double"
    assert \
        isinstance(b_stream, types.StringType), \
        "read_double() was given an invalid type: " + str(type(b_stream))
    assert \
        8 == len(b_stream), \
        "read_double() requires 8 bytes, got " + str(len(b_stream))

    return bs.unpack('64f', b_stream)[0]


def read_date(b_stream):
    """
    :param b_stream: 4 byte hex string
    :return: tuple (SInt16, UInt8, UInt8)
    """

    __name__ = "date"
    assert \
        isinstance(b_stream, types.IntType), \
        "read_date() was given an invalid type: " + str(type(b_stream))

    assert \
        4 == len(b_stream), \
        "read_date() requires 4 bytes, got " + str(len(b_stream))

    return bs.unpack('s16u8u8', b_stream)


def read_time(b_stream):
    """
    read_time()
    :param b_stream: 4 byte hex string
    :return: uint8 tuple (hour, minute, second, hsecond)
    """

    __name__ = "time"
    assert \
        isinstance(b_stream, types.StringType), \
        "read_float() was given an invalid type: " + str(type(b_stream))
    assert \
        4 == len(b_stream), \
        "read_time() requires 4 bytes, got " + str(len(b_stream))

    return bs.unpack('u8u8u8u8', b_stream)


# TODO: This one will need to be more rigorously tested against an actual pstring
def read_pstring(file_iter):
    """
    read_pstring()
    :param file_iter: an open, readable file iter at the start of a pstring
    :return: string of variable length
    """

    __name__ = "pstring"
    assert \
        isinstance(file_iter, file), \
        "read_pstring requires a file, got  " + str(type(file_iter))

    pstr_len = bs.unpack('u8', file_iter.read(1))[0]  # read one byte to get the len of the Pascal string
    pascal_string = ""

    for i in range(0, pstr_len, 1):
        pascal_string += file_iter.read(1)

    return pascal_string


# TODO: This one will need to be more rigorously tested against an actual cstring
def read_cstring(b_stream, chars):
    '''
    :param b_stream: stream of variable length defined by chars
    :param chars: number of chars in string
    :return: string of variable length
    '''

    __name__ = "cstring"
    #quick loop for getting the format for how many chars to unpack
    fmt = ''
    for _ in range(chars):
        fmt = fmt + str('u8')
    fmt = fmt + 'p1'
    assert \
        isinstance(b_stream, types.IntType), \
        "read_cstring() was given an invalid type: " + str(type(b_stream))

    assert \
        1 == len(b_stream), \
        "read_cstring() requires 1 byte, got " + str(len(b_stream))

    return bs.unpack(fmt, b_stream)


def read_thumb(b_stream):
    """
    read_thumb()
    :param b_stream: 10 byte hex string
    :return: tuple (d:int32, u:int32, c:uint8, n:uint8)
    """

    __name__ = "thumb"
    assert \
        isinstance(b_stream, types.StringType), \
        "read_thumb() was given an invalid type: " + str(type(b_stream))
    assert \
        10 == len(b_stream), \
        "read_thumb() requires 10 bytes, got " + str(len(b_stream))

    return bs.unpack('s32s32u8u8', b_stream)


def read_bool(b_stream):
    """
    read_bool()
    :param b_stream: 1 byte hex string
    :return: bool
    """

    __name__ = "bool"
    assert \
        isinstance(b_stream, types.IntType), \
        "read_bool() was given an invalid type: " + str(type(b_stream))
    assert \
        1 == len(b_stream), \
        "read_bool() requires 1 byte, got " + str(len(b_stream))
    return bs.unpack('b1', b_stream)


# Hold off on worrying about this one; it's for user-defined data structs
def read_user():
    __name__ = "user"
    pass


element_type_enum = {1: read_byte,
                     2: read_char,
                     3: read_word,
                     4: read_short,
                     5: read_long,
                     7: read_float,
                     8: read_double,
                     10: read_date,
                     11: read_time,
                     12: read_thumb,
                     13: read_bool,
                     18: read_pstring,
                     19: read_cstring}
