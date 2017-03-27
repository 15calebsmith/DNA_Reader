import ReadFile as rf
import os
import sys

########################################################################
### Functions
########################################################################
def testFileExt(inPath):
    '''
    :param inPath: Path to file
    :return: A list containing inPath if valid extension, otherwise empty list
    '''
    print '\t   ---testFileExt---'
    print '\t>> testFileExt      | inPath       \t=', inPath
    ext = os.path.splitext(inPath)[1]
    print '\t>> testFileExt      | ext          \t=', ext
    if ext == '.fsa':
        #rf.fsa(inPath)
        return [inPath]
    # elif ext == '.hid':
    #     #rf.hid(inPath)
    #     return True
    else:
        print 'Extension not supported.'
        #print 'File must be either .fsa or .hid'
        print 'File must be .fsa'
        return []

def testDir(inPath, rec):
    '''
    :param inPath: Path to directory
    :param rec: Boolean value to tell to recurse (True) or not (False)
    :return: List of paths to valid files, otherwise empty list
    '''
    print '\t   ---testDir---'
    print '\t>> testDir          | inPath       \t=', inPath
    print '\t>> testDir          | rec          \t=', rec
    validFileList = []
    print '\t>> testDir          | validFileList\t=', validFileList

    if (rec != 'y' and rec != 'n'):
        rec = raw_input('Recurse? (y/n): ')
        print rec
    if rec == 'y':
        # recursive file reading logic from
        # http://stackoverflow.com/questions/2212643/python-recursive-folder-read
        for root, subFolders, files in os.walk(inPath):
            print('\t>> testDir          | root         \t=' + root)
            print('\t>> testDir          | subFolders   \t=' + str(subFolders))
            print('\t>> testDir          | files        \t=' + str(files))

            for folder in subFolders:
                print('\t>> testDir          | folder        \t=' + str(folder))
            for filename in files:
                print('\t>> testDir          | filename     \t=' + filename)
                path = os.path.join(root, filename)
                print('\t>> testDir          | path         \t=' + path)
                if testFileExt(path):
                    validFileList.append(path)
    elif rec == 'n':
        print '"', str(inPath), '" is a directory, but recursion is off.'
    else:
        print 'recursion parameter unknown. Use "y" for yes, and "n" for no.'
    return validFileList

def testPath(inPath, rec):
    '''
    :param inPath: Path to be tested
    :param rec: Boolean value to tell to recurse (True) or not (False)
    :return: List of paths to valid files, otherwise empty list
    '''
    print '\t   ---testPath---'
    print '\t>> testPath         | inpath       \t=', inPath
    print '\t>> testPath         | rec          \t=', rec
    if os.path.exists(inPath):
        if os.path.isdir(inPath):
            return testDir(inPath, rec)
        elif os.path.isfile(inPath):
            return testFileExt(inPath)
    else:
        print '"', str(inPath), '" does not exist.'
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

    validPaths = testPath(normAbsInPath, recurse)
    print '\t>> start            | validPaths   \t=', validPaths
    print '\t>> start            | This is where we read the files'
    for file in validPaths:
        print '\t>> start            | file         \t=', file

else:
    print 'Not enough arguments.'
    print 'Format: inPath OutPath [Recurse]'

