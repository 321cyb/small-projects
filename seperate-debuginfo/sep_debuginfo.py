#!/usr/bin/env  python2
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 

#What this program does is to strip debuginfo of a directory
#and save the stripped debuginfo into another directory.

#Want to know more about stripped debuginfo, please read `info gdb`
#"18.2 Debugging Information in Separate Files"

import os
import os.path
import sys
import re
import shutil
import argparse
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)

#copy from Python 3 std lib.
def getstatusoutput(cmd):
    """Return (status, output) of executing cmd in a shell.

    Execute the string 'cmd' in a shell with os.popen() and return a 2-tuple
    (status, output).  cmd is actually run as '{ cmd ; } 2>&1', so that the
    returned output will contain output or error messages.  A trailing newline
    is stripped from the output.  The exit status for the command can be
    interpreted according to the rules for the C function wait().  Example:

    >>> import subprocess
    >>> subprocess.getstatusoutput('ls /bin/ls')
    (0, '/bin/ls')
    >>> subprocess.getstatusoutput('cat /bin/junk')
    (256, 'cat: /bin/junk: No such file or directory')
    >>> subprocess.getstatusoutput('/bin/junk')
    (256, 'sh: /bin/junk: not found')
    """
    pipe = os.popen('{ ' + cmd + '; } 2>&1', 'r')
    text = pipe.read()
    sts = pipe.close()
    if sts is None: sts = 0
    if text[-1:] == '\n': text = text[:-1]
    return sts, text


def ensure_dependencies(binary):
    status, output = getstatusoutput("which {0}".format(binary))
    if status != 0:
        print output
        sys.exit(1)


def ensure_dir_exists(dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)


def process_one_file(file_name, src_dir, dest_dir):
    rel_path       = file_name[(len(src_dir)+1):]
    debuginfo_path = os.path.join(dest_dir, rel_path + ".debug")

    output = subprocess.check_output(["readelf", "-S", file_name])

    if r".debug_info" not in output and  r".debug_str" not in output:
        print "{0} contains no .debug_info nor .debug_str section.".format(file_name)
        return
    if r".gnu_debuglink" in output:
        print "{0} already contains .gnu_debuglink section.".format(file_name)
        return

    status = subprocess.check_call(["objcopy", "--only-keep-debug", file_name, file_name + ".debug"])
    if status != 0:
        print "objcopy --only-keep-debug {0} {0}.debug".format(file_name) + " error."
        return

    status = subprocess.check_call(["strip",  "-g",  file_name])
    if status != 0:
        print "strip -g {0}".format(file_name) + " error."
        return

    status = subprocess.check_call(["objcopy", "--add-gnu-debuglink={0}.debug".format(file_name), file_name])
    if status != 0:
        print "objcopy --add-gnu-debuglink={0}.debug {0}".format(file_name) + " error."
        return

    ensure_dir_exists(os.path.dirname(debuginfo_path))
    shutil.move(file_name + ".debug", debuginfo_path)
    print "{0} debuginfo stripped to {1}".format(file_name, debuginfo_path)


def main(src_dir, dest_dir):
    ensure_dependencies("scanelf")
    ensure_dependencies("strip")
    ensure_dependencies("objcopy")
    ensure_dependencies("readelf")
    ensure_dir_exists(dest_dir)

    SCANELF_CMD_STRING  = 'scanelf -R --symlink --etype "ET_EXEC,ET_DYN" {0}'.format(src_dir)

    #first use scanelf find all executable and shared libs.
    #then for each elf found, strip and save it to dest_dir
    status, elf_files = getstatusoutput(SCANELF_CMD_STRING)

    if status != 0:
        print "scanelf executes error."
        sys.exit(1)

    logging.debug(elf_files)
    for line in elf_files.splitlines()[1:]:
        #scanelf example output:
        #ET_EXEC ./tmp/a.out 
        #ET_DYN ./tmp/libs.so 
        file_name = re.sub(r"^(ET_EXEC|ET_DYN)", "", line).strip()
        process_one_file(os.path.abspath(file_name), os.path.abspath(src_dir), os.path.abspath(dest_dir))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="strip a directory and save stripped debuginfo into another directory.")
    parser.add_argument("--src-dir", dest="src_dir", required=True)
    parser.add_argument("--dest-dir", dest="dest_dir", required=True)
    args = parser.parse_args()

    main(args.src_dir, args.dest_dir)


# vim: ai ts=4 sts=4 et sw=4
