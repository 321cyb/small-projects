#!/usr/bin/env  python3
#-*- coding: utf-8 -*-
#Author: Kevin Chen
#Date: 
#Problem description: http://www.taskcity.com/p/135698



#Known issues: Use os.stat to check file size may get wrong result
#on NFS devices.


import os
import sys


import logging
import signal
import threading
import subprocess
import pdb
import argparse

import transfer


parser = argparse.ArgumentParser(description="Monitors all .wmv files under a directory and uploads them to a FTP.")
parser.add_argument("-d", default=".")


transfer_in_progress = False
folder_name = None

last_file_dict = None
last_file_set  = None
sent_files     - set()
#By the way, I hate global variable.


def collect_data():
    '''
    walk through the directory and collects current file size information.
    '''
    global folder_name
    global sent_files
    current_file_dict = {}
    for dirpath, dirnames, filenames in os.walk(folder_name):
        for filename in filenames:
            if filename.endswith(".wmv") and filename not in sent_files:
                join_name = os.path.join(dirpath, filename)
                current_file_dict[join_name] = os.stat(join_name).st_size
    current_file_set = set(current_file_dict)
    return (current_file_dict, current_file_set)



def findout_complete_files(current_file_dict, current_file_set):
    '''
    Give the current snapshot and the last snapshot, computes the files that are not changed,
    and we consider them finished.
    '''
    global last_file_dict
    global last_file_set
    complete_files = []
    mutual_set = current_file_set & last_file_set
    for file in mutual_set:
        if current_file_dict[file] == last_file_dict[file]:
            complete_files.append(file)
            logging.debug("check_complete_files add file: {0}, current size is {1}".format( file, current_file_dict[file]))
    return complete_files





def timeout_handler(first_time = False):
    '''
    called when time out.
    '''
    global transfer_in_progress
    global last_file_dict
    global last_file_set
    global sent_files
    logging.warning("")
    logging.warning("timeout_handler enters, first_time is {0}".format(first_time))
    if transfer_in_progress:
        return

    complete_files = []

    current_file_dict, current_file_set = collect_data()

    if not first_time:
        complete_files = findout_complete_files(current_file_dict, current_file_set)

    last_file_dict, last_file_set = current_file_dict, current_file_set

    transfer_in_progress = True

    for file in  complete_files:
        if file not in sent_files: #double check, to be safe.
            print(file + "is ready to be processed.")
            if transfer.process_a_file(file) == 0:
                sent_files.add(file)


    transfer_in_progress = False
    threading.Timer(6, timeout_handler).start()



def start_monitor():
    timeout_handler(True)
    dummy_event = threading.Event()
    dummy_event.wait()




if __name__ == "__main__":
    args = parser.parse_args()
    folder_name = args.d

    logging.basicConfig(level=logging.DEBUG)
    #install SIGINT handler
#    signal.signal(signal.SIGINT, signal.SIG_DFL)

    start_monitor()

    


# vim: ai ts=4 sts=4 et sw=4
