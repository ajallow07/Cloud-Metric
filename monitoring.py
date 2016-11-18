#! /usr/bin/env python
"""
This file performs resource monitoring on machines
Monitoring cpu, memory, disk, and network resources

"""
from datetime import datetime
import psutil, sys,time
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

def send_resource_utilization(ip, clustername):

    cpu = psutil.cpu_times_percent()
    disk_root = psutil.disk_usage('/')
    phymem = psutil.virtual_memory()

    doc = dict()
    doc['cluster_id'] = clustername
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

        CM_DB = 'Node_Data'
        db = MongoClient(sys.argv[1], 27017)[CM_DB]
        #check for collection name in db
        #if "resources_usage_data" not in db.collection_names():
        #    db.create_collection('resources_usage_data',capped=True,size = 117964800, max=57600)

        db.resources_usage_data.insert(doc)

    except Exception as e:
        print "Could not insert data to db: "+str(e)

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print "Error, Usage: python monitoring.py [MongoDB IP] [Cluster Name] &"
        sys.exit()

    while True:
        try:
            monitoring_interval = sys.argv[3]
        except:
            monitoring_interval = 60
        send_resource_utilization(sys.argv[1], sys.argv[2])
        time.sleep(monitoring_interval) 
