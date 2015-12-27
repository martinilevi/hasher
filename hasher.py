#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) Telefonica I+D. All rights reserved.
#
# requires:
# pip install netaddr

"""
import re
import operator
"""
import os
import sys
import argparse
import traceback

import hashlib
import zlib
import pickle

thefiles_crc = {}
thefiles_sha = {}

def get_argument_parser():
    # initialize the parser object:
    parser = argparse.ArgumentParser(description='Hash some paths')   


    # define options here:
    parser.add_argument('paths', metavar='path', type=str, nargs='*',
                        default=['.',], help='path to-be-hashed directories.')

    return parser

def crc(fileName):
    """
    Perform crc32 checksum of file and return string with hex representation
    """
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def sha(fileName):
    """
    Perform sha256 hash of file and return string with hex representation
    """
    h = hashlib.sha256()
    for eachLine in open(fileName,"rb"):
        h.update(eachLine)
    return h.hexdigest()

def walk(rootdir='.'):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('\t%s' % fname)

def walkAndHash(rootDirs):
    for rootDir in rootDirs:
        for dirName, subdirList, fileList in os.walk(rootDir):
            #print('Found directory: %s' % dirName)
            for fname in fileList:
                absname=os.path.join(dirName,fname)
                cc = crc(absname)
                ss = sha(absname)
                if cc not in thefiles_crc:
                    thefiles_crc[cc] = absname
                else:
                    print "%s COLLIDES WITH %s ON CRC32 CHECK" % (absname, thefiles_crc[cc])

                if ss not in thefiles_sha:
                    thefiles_sha[ss] = absname
                else:
                    print "%s COLLIDES WITH %s ON SHA256 CHECK" % (absname, thefiles_sha[ss])
                    
                #print('\t%s\t%s\t%s' % (absname, cc, ss))

def saveMap(themap, fname):
    try:
        afile = open(fname, 'wb')
        pickle.dump(themap, afile)
        afile.close()
        return True
    except Exception, e:
        print "Error saving map %s to %s"%(themap, fname)
        return False

def readMap(fname):
    try:
        afile = open(fname, 'rb')
        tmp = pickle.load(afile)
        afile.close()
        print  >> sys.stderr, "DONE, %d files read"%len(tmp)
        sys.stderr.flush()
        return tmp

    except Exception, e:
        print "File %s not found or doesn't contain valid data"%(fname)
        return None

def printMap(m):
    for k in m.keys():
        print k, m[k]

def main(argv=None):
    global thefiles_crc, thefiles_sha
    if argv is None:
        argv = sys.argv[1:]

    parser = get_argument_parser()
    args = parser.parse_args(argv)

    map_candidate = readMap(r'crc32.hasher')
    if map_candidate:
        thefiles_crc = map_candidate

    map_candidate = readMap(r'sha256.hasher')
    print "*"*80
    print map_candidate
    print "*"*80
    if map_candidate:
        thefiles_sha = map_candidate

    map_candidate = None
 
    walkAndHash(args.paths)

    #printMap(thefiles_sha)
    #printMap(thefiles_crc)

    saveMap(thefiles_crc, r'crc32.hasher')
    saveMap(thefiles_sha, r'sha256.hasher')

    result = 0

    return result

if __name__ == '__main__':
    status = main()
    sys.exit(status)
