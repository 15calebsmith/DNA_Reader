import ReadFile as rf
import os
import sys

########################################################################
def fsa(path):
    print '\t   ---fsa---'
    print '\t>> fsa file found'
    print '\t>> inPath       \t=', path

def hid(path):
    print '\t   ---testPath---'
    print '\t>> hid file found'
    print '\t>> inPath       \t=', path

def testFile(inPath):
    print '\t   ---testFile---'
    #absInPath = os.path.abspath(inPath)
    if os.path.isfile(inPath):
        #print str(os.path.abspath(inPath)), 'is a file'
        ext = os.path.splitext(inPath)[1]
        print '\t>> ext          \t=', ext
        if ext == '.fsa':
            fsa(inPath)
        elif ext == '.hid':
            hid(inPath)

def testPath(inPath, rec):
    print '\t   ---testPath---'
    if os.path.exists(inPath):
        if os.path.isdir(inPath):
            print '\t>> ', str(os.path.basename(inPath)), 'is a dir'
            print '\t>> rec          \t=', rec
            if rec == '1':
                # recursive file reading logic from
                # http://stackoverflow.com/questions/2212643/python-recursive-folder-read
                for root, files in os.walk(inPath):
                    print('\t>> root         \t=' + root)

                    for filename in files:
                        path = os.path.join(root, filename)
                        testFile(path)
            else:

                print 'Directory found, but recursion is off.'
        elif os.path.isfile(inPath):
            testFile(inPath)
    else:
        print str(inPath), 'is not a dir or file'

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

print ''
