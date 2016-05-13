 #! /usr/bin/env python

import platform, socket
import psutil
import sys, datetime, os, json
import pymongo
from pymongo import MongoClient


"""
Retrieve memmory information
"""

def bytes_to_human(n):
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f' % (value)
    return "%s" % n


def get_total_memory(nt):
    memory = 0
    for name in nt._fields:
        value = getattr(nt, name)
        if name == 'total':
            memory = bytes_to_human(value)
    return memory


"""
Retrieve CPU information

"""
def get_block_storage():
    disk_size = 0
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        disk_size = bytes_to_human(usage.total)
    return disk_size

def detect_ncpus():
        """Detects the number of effective CPUs in the system"""
        #for Linux, Unix and MacOS
        if hasattr(os, "sysconf"):
            if "SC_NPROCESSORS_ONLN" in os.sysconf_names:
                #Linux and Unix
                ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
                if isinstance(ncpus, int) and ncpus > 0:
                    return ncpus
            else:
                #MacOS X
                return int(os.popen2("sysctl -n hw.ncpu")[1].read())
        #for Windows
        if "NUMBER_OF_PROCESSORS" in os.environ:
            ncpus = int(os.environ["NUMBER_OF_PROCESSORS"])
            if ncpus > 0:
                return ncpus
        #return the default value
        return 1

def insert_data():

    if len(sys.argv) < 2:
        print "Error, Usage: ./resource_mining.py [MongoDB IP]"
        sys.exit()

    SECRET_KEY = 'Put your secret key here'
    VM_DB = 'vm_nodes'
    REPORT_DB = 'reports'
    DB_NODE = MongoClient(sys.argv[1], 27017)[VM_DB]
    NODE_COLLECTION = DB_NODE.machines


#   returns a json object
    #MEMORY_SIZE = get_total_memory(psutil.virtual_memory())
    #DISK_SIZE = get_block_storage()
    #vCPU_COUNT = detect_ncpus()
    doc = dict()
    doc['node'] = socket.gethostname()
    doc['os'] = platform.system()
    doc['cpu'] = detect_ncpus()
    doc['memory'] = get_total_memory(psutil.virtual_memory())
    doc['disk'] = get_block_storage()

    #values = {'node': NODE, 'os': OS, 'cpu': vCPU_COUNT, 'memory': MEMORY_SIZE, 'disk': DISK_SIZE}
    #print vCPU_COUNT
    #print values
    #Connect to MongoDB

    try:
        db = DB_NODE
        result = db.machines.insert_one(doc)

        #obj_id = result.inserted_id
        #print obj_id
    except Exception as e:
        print "Could not insert data to db: "+str(e)


if __name__=='__main__':
    insert_data()
