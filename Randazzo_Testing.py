from collections import namedtuple

import bitstruct as bs
import ReadFile as rf
from ReadFile import ABIF_Entry
import Output

######################################################################################
# DEFINITIONS ########################################################################
######################################################################################

# Supported Element Type Numbers
ELEMENT_TYPE_NUMBERS = (1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 18, 19)

def parse_file(_filename, _verbose=0):
    """
    Reads tags out of a file and returns a dictionary of tag names containing the data lists
    :param _filename: 
    :param _verbose: 
    :return: 
    """

    bf = open(_filename, 'rb')
    bf.seek(0)
    tag_dict = {}

    ######################################################################################
    # HEADER AREA ########################################################################
    ######################################################################################

    # First 4 bytes = ABIF, next 2 bytes = Version Number
    buffer = bs.unpack("t32s16", bf.read(6))
    if _verbose:
        print "ABIF:         ", buffer[0]
        print "Version:      ", buffer[1]

    # Next 28 bytes are DirEntry struct
    buffer = bs.unpack("t32s32s16s16s32s32s32s32", bf.read(28))
    if _verbose:
        print "tdir:         ", buffer[0]
        print "Number:       ", buffer[1]
        print "Element Type: ", buffer[2]
        print "Element Size: ", buffer[3]
        print "Num Elements: ", buffer[4]
        print "Data Size:    ", buffer[5]
        print "Dir Offset:   ", buffer[6]
        print "__________________________________"

    dir_count = buffer[4]  # Number of directories in the file
    data_offset = buffer[6] # File position offset to the directory entries

    # Last 94 bytes are reserved (seek past and ignore)
    bf.seek(94, 1)

    ######################################################################################
    # DIRECTORY AREA #####################################################################
    ######################################################################################

    # Seek to the directory entry offset specified in the header
    bf.seek(data_offset)

    # Iterate through the directory entries
    for i in range(0, dir_count, 1):
        if _verbose:
            print "Seek Pos:    ", bf.tell(),
        buffer = bs.unpack("t32s32s16s16s32s32s32r32", bf.read(28))
        dir_entry = ABIF_Entry(tag_name=buffer[0].encode('ascii', 'ignore'),
                               tag_num=buffer[1],
                               elem_type=buffer[2],
                               elem_size=buffer[3],
                               num_elem=buffer[4],
                               data_size=buffer[5],
                               data_offset=buffer[6])

        # TODO: Command line argument to allow user-defined data types (disabled by default)
        if dir_entry.elem_type not in ELEMENT_TYPE_NUMBERS:
            if _verbose:
                print "SKIPPED [Unsupported Data Type]"
                print "__________________________________"
            continue

        if dir_entry.elem_type != 18: # TODO: we only look for and pull out pStrings.. implement the rest
            print
            continue

        if _verbose:
            print
            print "Tag Name:    ", dir_entry.tag_name
            print "Tag Number:  ", dir_entry.tag_num
            print "Element Type:", dir_entry.elem_type
            print "Element Size:", dir_entry.elem_size
            print "Num Elements:", dir_entry.num_elem
            print "Data Size:   ", dir_entry.data_size

        # If the data size <= 4, the data_offset field contains the value
        # Otherwise, treat data_offset as the offset in the file to the value
        if dir_entry.data_size > 4:
            print "Data Offset: ", dir_entry.data_offset
            file_counter = bf.tell()  # Store seek position before jumping
            bf.seek(dir_entry.data_offset)
            value = rf.read_pstring(bf)
            bf.seek(file_counter)     # Return to normal seek
        else:
            if _verbose:
                print "In-Field data values not yet supported."  # TODO
            continue

        print "__________________________________"

        try:
            tag_dict[dir_entry.tag_name].append(value)
        except KeyError:
            tag_dict[dir_entry.tag_name] = list()
            tag_dict[dir_entry.tag_name].append(value)

    # Use < to unpack Big Endian data formats stored in data_offset
    # data_offset is read out as raw data until we figure out how to treat it

    bf.close()
    return tag_dict

def print_keys(_dict):
    for key in _dict.keys():
        print key, _dict[key]


tag_dict = parse_file("./sample_data/B4 1 Victim Std.fsa", 1)
print_keys(tag_dict)
Output.toXML(tag_dict, "TEST")
