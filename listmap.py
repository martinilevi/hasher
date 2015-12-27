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

def get_argument_parser():
    # initialize the parser object:
    parser = argparse.ArgumentParser(description='print dictionaries persisted with pickle lib')   

    # define options here:
    parser.add_argument('paths', metavar='path', type=str, nargs='+',
                        default=['.',], help='path to-be-printed files.')

    return parser

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
    if argv is None:
        argv = sys.argv[1:]

    parser = get_argument_parser()
    args = parser.parse_args(argv)

    for f in args.paths:
        map_candidate = readMap(f)
        printMap(map_candidate)

    result = 0

    return result

if __name__ == '__main__':
    status = main()
    sys.exit(status)
