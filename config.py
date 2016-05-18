#! /usr/bin/env python

import pymongo
from pymongo import MongoClient

WTF_CSRF_ENABLED = True
CLUSTER_KEY = ''
DB_NODE = MongoClient('130.238.29.106', 27017)['cloud_metric_data']
CLUSTER_COLLECTION = DB_NODE.clusters

NODE_COLLECTION = DB_NODE.metered_data

REPORT_COLLECTION = DB_NODE.resources_usage_data
