  #! /usr/bin/env python
import os
import pymongo
from pymongo import MongoClient

WTF_CSRF_ENABLED = True
CLUSTER_KEY = ''
DB_NODE = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)['Node_Data']
CLUSTER_COLLECTION = DB_NODE.clusters
NODE_COLLECTION = DB_NODE.metered_data
REPORT_COLLECTION = DB_NODE.resources_usage_data
