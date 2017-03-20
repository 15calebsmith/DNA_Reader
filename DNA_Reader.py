import ReadFile as rf
import os
import sys

########################################################################
def testFileExt(inPath):
    print '\t   ---testFileExt---'
    print '\t>> inPath       \t=', inPath
    ext = os.path.splitext(inPath)[1]
    print '\t>> ext          \t=', ext
    if ext == '.fsa':
        rf.fsa(inPath)
        return True
    elif ext == '.hid':
        rf.hid(inPath)
        return True
    else:
        print 'Extension not supported.'
        print 'File must be either .fsa or .hid'
        return False

def testDir(inPath, rec):
    print '\t   ---testDir---'
    print '\t>> inPath       \t=', inPath
    print '\t>> rec          \t=', rec
    if rec == 'y':
        # recursive file reading logic from
        # http://stackoverflow.com/questions/2212643/python-recursive-folder-read
        for root, files in os.walk(inPath):
            print('\t>> root         \t=' + root)

            #for filename in files:
            #    path = os.path.join(root, filename)
            #    testFileExt(path)
        return True
    elif rec == 'n':
        print '"', str(inPath), '" is a directory, but recursion is off.'
        return False
    else:
        print 'recursion parameter unknown. Use "y" for yes, and "n" for no.'
        return False

def testPath(inPath, rec):
    print '\t   ---testPath---'
    if os.path.exists(inPath):
        if os.path.isdir(inPath):
            testDir(inPath, rec)
        elif os.path.isfile(inPath):
            testFileExt(inPath)
    else:
        print '"', str(inPath), '" does not exist.'
        return False

print '\t   ---start---'
if len(sys.argv) > 3:
    inPath = sys.argv[1]
    outPath = sys.argv[2]
    recurse = sys.argv[3]
    normAbsInPath = os.path.normpath(os.path.abspath(inPath))

    print '\t>> inpath       \t=', inPath
    print '\t>> outpath      \t=', outPath
    print '\t>> recurse      \t=', recurse
    print '\t>> normAbsInPath\t=', normAbsInPath

    testPath(normAbsInPath, recurse)

else:
    print 'Not enough arguments.'
    print 'Format: inPath OutPath Recurse'

print '\n'
