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
import optparse
import traceback

import hashlib
import zlib

def get_argument_parser():
    # initialize the parser object:
    parser = optparse.OptionParser('%prog [options] port_list')

    # define options here:
    parser.add_option('-v', '--verbose', action='store_true', 
                      default=False, help='prints out a lot of information')

    parser.add_option('-c', '--country', type='str',
                      default='', help='country, current node\'s country')

    parser.add_option('-t', '--threshold', type='int',
                      default=0, help='Global requests count threshold')

    return parser

def crc(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def sha(fileName):
    h = hashlib.sha256()
    for eachLine in open(fileName,"rb"):
        h.update(eachLine)
    return h.hexdigest()

def walk(rootdir='.'):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('\t%s' % fname)

def walkAndHash(rootDir='.'):
    for dirName, subdirList, fileList in os.walk(rootDir):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            absname=os.path.join(dirName,fname)
            print('\t%s\t%s\t%s' % (absname, crc(absname), sha(absname)))

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = get_argument_parser()
    options, args = parser.parse_args(argv)
    target = ''

    result = 0

    if len(args) >= 1:
       target = args[0]

    #verbose   = options.verbose
    #_country   = options.country.upper()
    #threshold = options.threshold

    return result

if __name__ == '__main__':
    #status = main()
    #sys.exit(status)

    walkAndHash()
