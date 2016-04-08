import pymongo
from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Put your secret key here'
DB_NAME = 'vm_nodes'
DATABASE = MongoClient('130.238.29.106', 27017)[DB_NAME]
NODE_COLLECTION = DATABASE.machines
SETTINGS_COLLECTION = DATABASE.settings
DEBUG = True
