 #! /usr/bin/env python

import config
import math
import mapping
from mapping import getMatchingInstanceInGCE, getMatchingInstanceInAWS, AWS_FLAVORS, GC_FLAVORS
from config import DB_NODE as db, DB_REPORT as dr, NODE_COLLECTION as nc, REPORT_COLLECTION as rc
#Node for support of  multi cluster , we will need cluster Id identification


def get_cpu_size(machine):
    for cpu in nc.find({"node":machine}, {"cpu":1,"_id":0}):
        size = cpu['cpu']
    return size

def get_memory_size(machine):
    size = 0
    for memory in nc.find({"node":machine}, {"memory":1,"_id":0}):
        size = float(memory['memory'])
    return size

def get_nodes_in_cluster():
    machines_in_cluster = []
    #get_node_name = function(doc) { return doc.node }
    for machine in nc.find({}, {"node":1,"_id":0}):
        machines_in_cluster.append(machine['node'])
    return machines_in_cluster

def get_max_memory_utilized(machine):
    mem_usage = 0
    mem_percent = 0
    mem_size = get_memory_size(machine)
    #get the maximum cpu usage
    for max_mem in rc.find({"node":machine}, {"_id":0, "memory":1}).sort([("memory",-1)]).limit(1):
         mem_percent = max_mem['memory']
    return math.ceil((mem_percent) /100 * mem_size)

def get_max_cpu_utilized(machine):
    cpu_usage = 0
    cpu_percent = 0
    cpu_size = get_cpu_size(machine)
    #get the maximum cpu usage
    for max_cpu in rc.find({"node":machine}, {"_id":0, "cpu.user":1}).sort([("cpu.user",-1)]).limit(1):
         cpu_percent = max_cpu['cpu']['user']

    return math.ceil(cpu_percent/100 * cpu_size)

def get_resources_utilized():
    machine_resources = dict()
    for machine in get_nodes_in_cluster():
        machine_resources.update({machine:{'cpu': get_max_cpu_utilized(machine), 'memory':get_max_memory_utilized(machine)}})
        #machine_resources.update(machine:)

    return machine_resources

def get_matching_instance_in_gcp(doc):
    gcp_instances =[]
    for machine in doc:
         flavors = getMatchingInstanceInGCE(GC_FLAVORS, get_max_cpu_utilized(machine), get_max_memory_utilized(machine))
         gcp_instances.append(flavors)
    return gcp_instances

def get_matching_instance_in_aws(doc):
    aws_instances =[]
    for machine in doc:
        flavors = getMatchingInstanceInAWS(AWS_FLAVORS, get_max_cpu_utilized(machine), get_max_memory_utilized(machine))
        aws_instances.append(flavors)
    return aws_instances

def get_cost_of_recommended_instances():

    
    return 0


if __name__ == '__main__':
    print get_max_cpu_utilized("dev-node")
    machine = get_resources_utilized()
    print machine
    #machine = get_nodes_in_cluster()
    #print get_matching_instance_in_aws(machine)
