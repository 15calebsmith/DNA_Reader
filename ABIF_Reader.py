"""
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

from collections import namedtuple

import Output as out
import Read_Types as rf
import bitstruct as bs


# noinspection PyPep8Naming
class ABIF_Reader(object):
    """
    ABIF Reader object.
    Call read_file to parse a file and add its contents to this object's tag dictionary
    Call a write function to write the tag dictionary to a file
    """

    ABIF_Entry = namedtuple("dir_entry", "tag_name \
                                          tag_num \
                                          elem_type \
                                          elem_size \
                                          num_elem \
                                          data_size \
                                          data_offset")

    # Named Tuple to store extracted directory entry fields
    element_type_enum = {1: rf.read_byte,
                         2: rf.read_char,
                         3: rf.read_word,
                         4: rf.read_short,
                         5: rf.read_long,
                         7: rf.read_float,
                         8: rf.read_double,
                         10: rf.read_date,
                         11: rf.read_time,
                         12: rf.read_thumb,
                         13: rf.read_bool,
                         18: rf.read_pstring,
                         19: rf.read_cstring}

    # Supported Element Type Numbers
    SUPPORTED_ELEM_TYPES = (1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 18, 19)

    # Class Variables
    bf = None
    tag_dict = None
    dir_entry = None
    tag_counts = None

    def __init__(self):
        self.bf = 0
        self.tag_dict = {}
        self.dir_entry = self.ABIF_Entry
        self.tag_counts = {"UNSUPPORTED": 0, "TOTAL": 0}

    def handle_data(self, verbose=0):
        """
        Unpacks binary data of supported types and adds them to the tag dictionary
        :param verbose: Set to enable per-tag processing information
        :return: The tag dictionary from the file
        """

        file_counter = self.bf.tell()  # Store seek position before jumping
        self.bf.seek(self.dir_entry.data_offset)  # Jump to file offset where data begins

        if verbose:
            print "handle_data: Using", self.element_type_enum[self.dir_entry.elem_type].__name__

        new_data = []

        if self.dir_entry.elem_type == 1:  # byte
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_byte(self.bf.read(1)))

        elif self.dir_entry.elem_type == 2:  # char
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_char(self.bf.read(1)))

        elif self.dir_entry.elem_type == 3:  # word
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_word(self.bf.read(2)))

        elif self.dir_entry.elem_type == 4:  # short
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_short(self.bf.read(2)))

        elif self.dir_entry.elem_type == 5:  # long
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_long(self.bf.read(4)))

        elif self.dir_entry.elem_type == 7:  # float
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_float(self.bf.read(4)))

        elif self.dir_entry.elem_type == 8:  # double
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_double(self.bf.read(8)))

        elif self.dir_entry.elem_type == 10:  # long
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_date(self.bf.read(4)))

        elif self.dir_entry.elem_type == 11:  # long
            for item in range(0, self.dir_entry.num_elem, 1):
                new_data.append(rf.read_time(self.bf.read(4)))

        elif self.dir_entry.elem_type == 18:  # long
            new_data = rf.read_pstring(self.bf)
            # new_data = self.element_type_enum[18](self.bf)

        elif self.dir_entry.elem_type == 19:  # long
            new_data = self.element_type_enum[19](self.bf)

        try:
            self.tag_dict[self.dir_entry.tag_name] += new_data
        except KeyError:
            self.tag_dict[self.dir_entry.tag_name] = list()
            self.tag_dict[self.dir_entry.tag_name] += new_data

        self.bf.seek(file_counter)  # Return to previous file position

    def read_file(self, filename, verbose=0):
        """
        Reads tags out of a file and adds their data to the tag dictionary
        :param filename: Path to file to read
        :param verbose: Set to enable per-tag processing information
        :return: Dictionary of lists containing tag values
        """

        self.bf = open(filename, 'rb')
        print "Reading", filename

        # HEADER AREA ########################################################################

        # First 4 bytes = ABIF, next 2 bytes = Version Number
        buf = bs.unpack("t32s16", self.bf.read(6))
        if verbose:
            print "ABIF:         ", buf[0]
            print "Version:      ", buf[1]

        # Next 28 bytes are DirEntry struct
        buf = bs.unpack("t32s32s16s16s32s32s32s32", self.bf.read(28))
        if verbose:
            print "tdir:         ", buf[0]
            print "Number:       ", buf[1]
            print "Element Type: ", buf[2]
            print "Element Size: ", buf[3]
            print "Num Elements: ", buf[4]
            print "Data Size:    ", buf[5]
            print "Dir Offset:   ", buf[6]
            print "__________________________________"

        dir_count = buf[4]  # Number of directories in the file
        self.tag_counts["TOTAL"] += dir_count
        data_offset = buf[6]  # File position offset to the directory entries

        # Last 94 bytes are reserved (seek past and ignore)
        self.bf.seek(94, 1)

        # DIRECTORY AREA #####################################################################

        # Seek to the directory entry offset specified in the header
        self.bf.seek(data_offset)

        # Iterate through the directory entries
        for _ in range(dir_count):
            if verbose:
                print "Seek Pos:    ", self.bf.tell(),

            buf = bs.unpack("t32s32s16s16s32s32s32r32", self.bf.read(28))
            self.dir_entry = self.ABIF_Entry(tag_name=buf[0].encode('ascii', 'ignore'),
                                             tag_num=buf[1],
                                             elem_type=buf[2],
                                             elem_size=buf[3],
                                             num_elem=buf[4],
                                             data_size=buf[5],
                                             data_offset=buf[6])

            # File Statistics
            try:
                self.tag_counts[self.dir_entry.tag_name] += 1
            except KeyError:
                self.tag_counts[self.dir_entry.tag_name] = 1

            # TODO: Command line argument to allow user-defined data types (disabled by default)
            if self.dir_entry.elem_type not in self.SUPPORTED_ELEM_TYPES:
                if verbose:
                    print "SKIPPED [Unsupported Data Type]"
                    print "__________________________________"
                self.tag_counts["UNSUPPORTED"] += 1
                continue

            if verbose:
                print
                print "Tag Name:    ", self.dir_entry.tag_name
                print "Tag Number:  ", self.dir_entry.tag_num
                print "Element Type:", self.dir_entry.elem_type
                print "Element Size:", self.dir_entry.elem_size
                print "Num Elements:", self.dir_entry.num_elem
                print "Data Size:   ", self.dir_entry.data_size

            # If the data size <= 4, the data_offset field contains the value
            # Otherwise, treat data_offset as the offset in the file to the value
            if self.dir_entry.data_size > 4:
                if verbose:
                    print "Data Offset: ", self.dir_entry.data_offset
                self.handle_data(verbose)
            else:
                if verbose:
                    print "In-Field data values not yet supported. Raw value returned."  # TODO
                    print "__________________________________"
                    continue
                    # try:
                    #     self.tag_dict[self.dir_entry.tag_name] += self.dir_entry.data_offset
                    # except KeyError:
                    #     self.tag_dict[self.dir_entry.tag_name] = list()
                    #     self.tag_dict[self.dir_entry.tag_name] += self.dir_entry.data_offset

            if verbose:
                print "__________________________________"

        self.bf.close()
        print "\tDone reading", filename

        return self.tag_dict

    def write_xml(self, filename):
        if len(self.tag_dict) == 0:
            print "Write Error: No files have been processed yet."
            return
        out.write_xml(self.tag_dict, filename)

    def print_tags(self):
        """
        Prints tags and their values to console
        :return:
        """

        for key in self.tag_dict.keys():
            print key, "-------------------------------"
            for item in self.tag_dict[key]:
                print "\t", item

    def print_stats(self):
        """
        Prints tag statistics to console
        :return: None
        """

        num_processed = self.tag_counts["TOTAL"] - self.tag_counts["UNSUPPORTED"]
        print num_processed, "of", self.tag_counts["TOTAL"], "tags retrieved:"
        for key in self.tag_counts.keys():
            if len(key) == 4:
                print "\t", key + ":", self.tag_counts[key]
