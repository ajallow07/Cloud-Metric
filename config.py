import pymongo
from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Put your secret key here'
VM_DB = 'vm_nodes'
REPORT_DB = 'reports'
DB_NODE = MongoClient('130.238.29.106', 27017)[VM_DB]
DB_REPORT = MongoClient('130.238.29.106', 27017)[REPORT_DB]
NODE_COLLECTION = DB_NODE.machines
REPORT_COLLECTION = DB_REPORT.resources

SETTINGS_COLLECTION_1 = DB_NODE.settings
SETTINGS_COLLECTION_2 = DB_REPORT.settings

DEBUG = True
