# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import argparse

import numpy as np
import nptdms
import axographio


def tdms2axg(filename, force=False, verbose=True):
    """
    Convert a TDMS file to an AxoGraph (AXGX) file
    """

    if not os.path.isfile(filename):
        raise ValueError('error: file not found: ' + filename)
    if filename.split('.')[-1] != 'tdms':
        raise ValueError('error: file does not appear to be a TDMS file (does not end in ".tdms"): ' + filename)

    output_filename = '.'.join(filename.split('.')[:-1]) + '.axgx'
    if os.path.isfile(output_filename) and not force:
        raise FileExistsError('error: output file exists, use force flag to overwrite: ' + output_filename)

    # read the TDMS file
    tdms_file = nptdms.TdmsFile.read(filename)
    group = tdms_file.groups()[0]  # use only first group
    channels = group.channels()

    if verbose:
        print()
        print('Properties of "' + filename + '":')
        print()
        for name, value in tdms_file.properties.items():
            print(str(name) + ': ' + str(value))
        print()

    # collect the data for writing to AxoGraph format
    names = ['Time (s)']
    columns = [channels[0].time_track()]  # assume time is same for all columns
    for c in channels:
        names += [c.name]
        columns += [c[:]]

    # write the AxoGraph file
    if verbose:
        print('Writing contents to AxoGraph file "' + output_filename + '"...')
    f = axographio.file_contents(names, columns)
    f.write(output_filename)
    if verbose:
        print('Done!')


def parse_args(argv):

    description = """
    A simple script for converting National Instruments TDMS files to AxoGraph
    files.

    The AxoGraph (AXGX) file is saved with the same name and in the same
    directory as the TDMS file. By default, an existing AxoGraph file will not
    be overwritten; use --force to overwrite it.
    """

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('file',
                        help='the path to a TDMS file')
    parser.add_argument('-f', '--force', action='store_true', dest='force',
                        help='overwrite the output file if it already exists')
    parser.add_argument('-q', '--quiet', action='store_false', dest='verbose',
                        help='run silently')

    args = parser.parse_args(argv[1:])
    return args


def main():
    args = parse_args(sys.argv)
    try:
        tdms2axg(args.file, args.force, args.verbose)
    except Exception as e:
        # skip the traceback when run from the command line
        print(e)
