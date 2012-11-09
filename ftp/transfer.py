#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 

import os
import sys
import subprocess
import ftplib

from setting import  REMOTE_HOST, USER, PASSWORD

def check_filename(filename):
    '''
    This function generates an output file name from the input file name.
    '''
    if filename.endswith(".wmv"):
        basename = filename[:filename.rfind(".wmv")]
        return (filename, basename + ".mp4")
    else:
        return (None, None)




def convert_file(input, output):
    '''
    This function calls ffmpeg to convert wmv file to mp4 file.
    Ensure that ffmpeg has libx264, libaac and other related codec support.
    '''
    p = subprocess.Popen(["ffmpeg", "-i", input, output], stdout=subprocess.PIPE)
    if p.wait() is not 0:
        sys.stderr.write("ffmpeg execute error, below is output messages:\n")
        sys.stderr.write(p.stdout.read())
        return False
    return True





def transfer_file(output):
    '''
    Open a FTP connection and send the output file to remote server.
    '''
    with ftplib.FTP(REMOTE_HOST, USER, PASSWORD) as ftp:
        with open(output, "r") as f:
            try:
                ftp.storbinary("STORE " + output, f)
                return True
            except Exception as e:
                sys.stderr.write(str(e))
                return False
    return False



def process_a_file(filename):
    '''
    Given an input file name, this function converts that file to mp4 and send it to server.
    '''
    (i,o) = check_filename(filename)
    if not i or not o:
        sys.stderr.write("argument error:" + filename)
        return 1
    if not convert_file(i,o):
        return 2
    if not transfer_file(o):
        return 3
    return 0




if __name__ == "__main__":
    for arg in sys.argv[1:]:
        (i,o) = check_filename(arg)
        if not i or not o:
            sys.stderr.write("argument error:" + arg)
            sys.exit(1)
        if not convert_file(i,o):
            sys.exit(2)
        if not transfer_file(o):
            sys.exit(3)
        sys.exit(0)



# vim: ai ts=4 sts=4 et sw=4
