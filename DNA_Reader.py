import Read_Types as rf
import os
import sys


########################################################################
# Functions ############################################################
########################################################################


def test_file_ext(in_path):
    """
    :param in_path: Path to file
    :return: A list containing inPath if valid extension, otherwise empty list
    """

    print '\t   ---testFileExt---'
    print '\t>> testFileExt      | inPath       \t=', in_path
    ext = os.path.splitext(in_path)[1]
    print '\t>> testFileExt      | ext          \t=', ext
    if ext == '.fsa':
        # rf.fsa(inPath)
        return [in_path]
    # elif ext == '.hid':
    #     #rf.hid(inPath)
    #     return True
    else:
        print 'Extension not supported.'
        # print 'File must be either .fsa or .hid'
        print 'File must be .fsa'
        return []


def test_dir(in_path, rec):
    """
    :param in_path: Path to directory
    :param rec: Boolean value to tell to recurse (True) or not (False)
    :return: List of paths to valid files, otherwise empty list
    """

    print '\t   ---testDir---'
    print '\t>> testDir          | inPath       \t=', in_path
    print '\t>> testDir          | rec          \t=', rec
    valid_file_list = []
    print '\t>> testDir          | valid_file_list\t=', valid_file_list

    if rec != 'y' and rec != 'n':
        rec = raw_input('Recurse? (y/n): ')
        print rec
    if rec == 'y':
        # recursive file reading logic from
        # http://stackoverflow.com/questions/2212643/python-recursive-folder-read
        for root, subFolders, files in os.walk(in_path):
            print('\t>> testDir          | root         \t=' + root)
            print('\t>> testDir          | subFolders   \t=' + str(subFolders))
            print('\t>> testDir          | files        \t=' + str(files))

            for folder in subFolders:
                print('\t>> testDir          | folder        \t=' + str(folder))
            for filename in files:
                print('\t>> testDir          | filename     \t=' + filename)
                path = os.path.join(root, filename)
                print('\t>> testDir          | path         \t=' + path)
                if test_file_ext(path):
                    valid_file_list.append(path)
    elif rec == 'n':
        print '"', str(in_path), '" is a directory, but recursion is off.'
    else:
        print 'recursion parameter unknown. Use "y" for yes, and "n" for no.'
    return valid_file_list


def test_path(in_path, rec):
    """
    :param in_path: Path to be tested
    :param rec: Boolean value to tell to recurse (True) or not (False)
    :return: List of paths to valid files, otherwise empty list
    """

    print '\t   ---testPath---'
    print '\t>> testPath         | inpath       \t=', in_path
    print '\t>> testPath         | rec          \t=', rec
    if os.path.exists(in_path):
        if os.path.isdir(in_path):
            return test_dir(in_path, rec)
        elif os.path.isfile(in_path):
            return test_file_ext(in_path)
    else:
        print '"', str(in_path), '" does not exist.'
        return []


print '\t   ---start---'
if len(sys.argv) > 2:
    inPath = sys.argv[1]
    outPath = sys.argv[2]
    if len(sys.argv) > 3:
        recurse = sys.argv[3]
    else:
        recurse = None
    normAbsInPath = os.path.normpath(os.path.abspath(inPath))

    print '\t>> start            | inpath       \t=', inPath
    print '\t>> start            | outpath      \t=', outPath
    print '\t>> start            | recurse      \t=', recurse
    print '\t>> start            | normAbsInPath\t=', normAbsInPath

    validPaths = test_path(normAbsInPath, recurse)
    print '\t>> start            | validPaths   \t=', validPaths
    print '\t>> start            | This is where we read the files'
    for cur_file in validPaths:
        print '\t>> start            | file         \t=', cur_file

else:
    print 'Not enough arguments.'
    print 'Format: inPath OutPath [Recurse]'
