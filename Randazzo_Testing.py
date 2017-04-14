from collections import namedtuple

import bitstruct as bs

######################################################################################
# DEFINITIONS ########################################################################
######################################################################################

# Supported Element Type Numbers
ELEMENT_TYPE_NUMBERS = (1, 2, 3, 4, 5, 7, 8, 10, 11, 13, 18, 19)

# Named Tuple to store extracted directory entry fields
ABIF_Entry = namedtuple("dir_entry", "tag_name \
                                      tag_num \
                                      elem_type \
                                      elem_size \
                                      num_elem \
                                      data_size \
                                      data_offset")

# open file
bf = open("./sample_data/B4 1 Victim Std.fsa", 'rb')
bf.seek(0)

######################################################################################
# HEADER AREA ########################################################################
######################################################################################

# First 4 bytes = ABIF, next 2 bytes = Version Number
buffer = bs.unpack("t32s16", bf.read(6))
print "ABIF:        ", buffer[0]
print "Version:     ", buffer[1]

# Next 28 bytes are DirEntry struct, points to directory
buffer = bs.unpack("t32s32s16s16s32s32s32s32", bf.read(28))
print "tdir:         ", buffer[0]
print "Number:       ", buffer[1]
print "Element Type: ", buffer[2]
print "Element Size: ", buffer[3]
print "Num Elements: ", buffer[4]
print "Data Size:    ", buffer[5]
print "Dir Offset:   ", buffer[6]
print "__________________________________"

dir_count = buffer[4]
data_offset = buffer[6]

# Last 94 bytes are reserved (ignore)
bf.seek(94, 1)

######################################################################################
# DIRECTORY AREA #####################################################################
######################################################################################

# Seek to the directory entry offset specified in the header
bf.seek(data_offset)

# Iterate through the directory entries
for i in range(0, dir_count, 1):
    buffer = bs.unpack("t32s32s16s16s32s32s32s32", bf.read(28))
    dir_entry = ABIF_Entry(tag_name=buffer[0],
                           tag_num=buffer[1],
                           elem_type=buffer[2],
                           elem_size=buffer[3],
                           num_elem=buffer[4],
                           data_size=buffer[5],
                           data_offset=buffer[6])

    # TODO: Command line argument to allow user-defined data types (disabled by default)
    if dir_entry.elem_type not in ELEMENT_TYPE_NUMBERS:
        continue

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
    else:
        bf.seek(-4, 1)
        print "Value:       ", bs.unpack("r32", bf.read(4))

    print "__________________________________"

# Use < to unpack Big Endian data formats stored in data_offset
