import ABIF_Reader as reader
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

    log('\t   ---testFileExt---')
    log('\t>> testFileExt      | inPath       \t=' + str(in_path))
    ext = os.path.splitext(in_path)[1]
    log('\t>> testFileExt      | ext          \t=' + ext)
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

    log('\t   ---testDir---')
    log('\t>> testDir          | inPath       \t=' + str(in_path))
    log('\t>> testDir          | rec          \t=' + str(rec))
    valid_file_list = []
    log('\t>> testDir          | valid_file_list\t=' + str(valid_file_list))

    if rec != 'y' and rec != 'n':
        rec = raw_input('Recurse? (y/n): ')
        log(rec)
    if rec == 'y':
        # recursive file reading logic from
        # http://stackoverflow.com/questions/2212643/python-recursive-folder-read
        for root, subFolders, files in os.walk(in_path):
            log('\t>> testDir          | root         \t=' + root)
            log('\t>> testDir          | subFolders   \t=' + str(subFolders))
            log('\t>> testDir          | files        \t=' + str(files))

            for folder in subFolders:
                log('\t>> testDir          | folder        \t=' + str(folder))
            for filename in files:
                log('\t>> testDir          | filename     \t=' + filename)
                path = os.path.join(root, filename)
                log('\t>> testDir          | path         \t=' + path)
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

    log('\t   ---testPath---')
    log('\t>> testPath         | inpath       \t=' + str(in_path))
    log('\t>> testPath         | rec          \t=' + str(rec))
    if os.path.exists(in_path):
        if os.path.isdir(in_path):
            return test_dir(in_path, rec)
        elif os.path.isfile(in_path):
            return test_file_ext(in_path)
    else:
        print '"', str(in_path), '" does not exist.'
        return []


def log(msg):
    if verbose == 'y':
        print(msg)


if len(sys.argv) > 2:
    inPath = sys.argv[1]
    outPath = sys.argv[2]
    if len(sys.argv) > 3:
        recurse = sys.argv[3]
    else:
        recurse = None

    if len(sys.argv) > 4:
        verbose = sys.argv[4]
    else:
        verbose = None

    normAbsInPath = os.path.normpath(os.path.abspath(inPath))
    validPaths = test_path(normAbsInPath, recurse)

    log('\t   ---start---')
    log('\t>> start            | inpath       \t=' + str(inPath))
    log('\t>> start            | outpath      \t=' + str(outPath))
    log('\t>> start            | recurse      \t=' + str(recurse))
    log('\t>> start            | normAbsInPath\t=' + normAbsInPath)
    log('\t>> start            | validPaths   \t=' + str(validPaths))
    log('\t>> start            | This is where we read the files')


    if len(validPaths) > 1:
        log('\t>> start            | More than one valid file. outpath treated as dir.')
        if not os.path.exists(outPath):
            os.makedirs(outPath)
        for cur_file in validPaths:
            log('\t>> start            | file         \t=' + cur_file)
            rdr = reader.ABIF_Reader()
            rdr.read_file(cur_file, False)
            rdr.write_xml(os.path.join(outPath, os.path.basename(cur_file)))
    elif len(validPaths) == 1:
        log('\t>> start            | Only one valid file. outpath treated as file name.')
        log('\t>> start            | file         \t=' + str(validPaths[0]))
        rdr = reader.ABIF_Reader()
        rdr.read_file(validPaths[0], verbose)
        rdr.write_xml(outPath)
    else:
        log("\t>> start            | validPaths has zero, or a negative number (error) of elements.")
        log("\t>> start            | Expected only when input is a dir, and recursion is off (0 elements).")

else:
    print 'Not enough arguments.'
    print 'Format: inPath OutPath [Recurse] [verbose/debug]'


