"""
Collection of functions that decodes a binary stream into its native type or C struct

Libraries in use:
https://pypi.python.org/pypi/bitstruct/
DOCS --> http://bitstruct.readthedocs.io/en/latest/

"""

# Note: Compile this file with into a .pyo file when complete (use -oo arg)
import types

import bitstruct as bs


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

    if isinstance(b_stream, types.IntType):
        return bs.unpack('s8', b_stream)[0]
    elif isinstance(b_stream, types.StringType):
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

    print len(b_stream)

    return bs.unpack('u16', b_stream)


def read_short(b_stream):
    """
    read_short()
    :param b_stream: 2 byte hex string
    :return: sint16
    """

    __name__ = "short"

    return bs.unpack('s16', b_stream)[0]


def read_long(b_stream):
    """
    :param b_stream: 4 byte hex string
    :return: tuple (SInt32)
    """

    __name__ = "long"

    return bs.unpack('s32', b_stream)[0]


def read_float(b_stream):
    """
    read_float()
    :param b_stream: 4 byte hex string
    :return: float
    """

    __name__ = "float"

    return bs.unpack('f32', b_stream)


def read_double(b_stream):
    """
    read_double()
    :param b_stream: 8 byte hex string
    :return: float64
    """

    __name__ = "double"

    return bs.unpack('f64', b_stream)[0]


def read_date(b_stream):
    """
    :param b_stream: 4 byte hex string
    :return: tuple (SInt16, UInt8, UInt8)
    """

    __name__ = "date"

    return bs.unpack('s16u8u8', b_stream)


def read_time(b_stream):
    """
    read_time()
    :param b_stream: 4 byte hex string
    :return: uint8 tuple (hour, minute, second, hsecond)
    """

    __name__ = "time"

    return bs.unpack('u8u8u8u8', b_stream)


# TODO: This one will need to be more rigorously tested against an actual pstring
def read_pstring(file_iter):
    """
    read_pstring()
    :param file_iter: an open, readable file iter at the start of a pstring
    :return: list containing a string of variable length
    """

    __name__ = "pstring"
    assert \
        isinstance(file_iter, file), \
        "read_pstring requires a file, got " + str(type(file_iter))

    pstr_len = bs.unpack('u8', file_iter.read(1))[0]  # read one byte to get the len of the Pascal string
    pascal_string = ""

    for i in range(0, pstr_len, 1):
        pascal_string += file_iter.read(1)

    # return a list to match the return type of stream-type conversion methods
    _l = [pascal_string]
    return _l


def read_cstring(file_iter):
    """
    read_cstring()
    :param file_iter: an open, readable file iter at the start of a cstring
    :return: list containing a string of variable length
    """

    __name__ = "cstring"
    assert \
        isinstance(file_iter, file), \
        "read_cstring requires a file, got " + str(type(file_iter))

    c_string = ""
    while True:
        char = bs.unpack('t8', file_iter.read(8))[0]
        if char == '\0':
            break
        c_string += char

    _l = [c_string]
    return _l


def read_thumb(b_stream):
    """
    read_thumb()
    :param b_stream: 10 byte hex string
    :return: tuple (d:int32, u:int32, c:uint8, n:uint8)
    """

    __name__ = "thumb"

    return bs.unpack('s32s32u8u8', b_stream)


def read_bool(b_stream):
    """
    read_bool()
    :param b_stream: 1 byte hex string
    :return: bool
    """

    __name__ = "bool"

    return bs.unpack('b8', b_stream)


def read_user():
    __name__ = "user"
    print "User-defined data types are not currently supported."
    pass
