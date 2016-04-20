#! /usr/bin/env python
"""
This file performs resource monitoring on machines
Monitoring cpu, memory, disk, and network resources

"""
from datetime import datetime
import psutil
import pymongo
from pymongo import MongoClient
import socket

#Utilize the first disk partition
"""
first_mnt = psutil.disk_partitions(all=False)[0].mountpoint
var_cpu = psutil.cpu_percent(interval=1)
var_mem = psutil.virtual_memory().percent
var_disk = psutil.disk_usage(first_mnt).percent

"""

def main():

    cpu = psutil.cpu_times_percent()
    disk_root = psutil.disk_usage('/')
    phymem = psutil.virtual_memory()

    doc = dict()
    doc['node'] = socket.gethostname()
    doc['dt'] = datetime.now()
    doc['disk'] = disk_root.percent
    doc['memory'] = phymem.percent
    doc['cpu'] = {
       'user': cpu.user,
       'nice': cpu.nice,
       'system': cpu.system,
    }

    try:
        conn = MongoClient('130.238.29.106', 27017)
        db = conn.reports
        result = db.resources.insert_one(doc)
        conn.close()

    except Exception as e:
        print "Could not insert data to db: "+str(e)

if __name__ == '__main__':
    import time
    while True:
        main()
        time.sleep(60) # pause for 30 seconds
