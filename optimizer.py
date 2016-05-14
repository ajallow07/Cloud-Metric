 #! /usr/bin/env python

import config
import math
import mapping, computeCost
from computeCost import read_EC2_ondemand_instance_prices, aws_storage_prices, gce_price
from mapping import getMatchingInstanceInGCE, getMatchingInstanceInAWS, AWS_FLAVORS, GC_FLAVORS
from config import DB_NODE as db, DB_REPORT as dr, NODE_COLLECTION as nc, REPORT_COLLECTION as rc
#Node for support of  multi cluster , we will need cluster Id identification


def get_machine_resources(machine):
    for resource in nc.find({"node":machine}, {"cpu":1,"memory":1, "disk":1, "os":1, "_id":0}):
        cpu = resource['cpu']
        memory = float(resource['memory'])
        disk = float(resource['disk'])
        os = resource['os']
    return cpu, memory, disk, os

def get_nodes_in_cluster():
    machines_in_cluster = []
    #get_node_name = function(doc) { return doc.node }
    for machine in nc.find({}, {"node":1,"_id":0}):
        machines_in_cluster.append(machine['node'])
    return machines_in_cluster

def get_max_resources_utilized(machine):
    cpu_percent = 0
    percent_val = 100
    mem_percent = 0
    #disk_percent = 0
    cpu_size, mem_size, disk_size, os = get_machine_resources(machine)
    #highest cpu usage over time
    for max_cpu in rc.find({"node":machine}, {"_id":0, "cpu.user":1}).sort([("cpu.user",-1)]).limit(1):
         cpu_percent = max_cpu['cpu']['user']
    #highest memory usage over time period
    for max_mem in rc.find({"node":machine}, {"_id":0, "memory":1}).sort([("memory",-1)]).limit(1):
         mem_percent = max_mem['memory']

    return math.ceil(cpu_percent/percent_val * cpu_size), math.ceil((mem_percent) /percent_val * mem_size), math.ceil(disk_size), os

def get_matching_instance_in_providers(doc):

    gcp_instances = []
    aws_instances = []

    for machine in doc:
        max_cpu, max_memory, disk, os = get_max_resources_utilized(machine)

        flavors = getMatchingInstanceInGCE(GC_FLAVORS, max_cpu, max_memory)
        gcp_instances.append(flavors)

        flavors = getMatchingInstanceInAWS(AWS_FLAVORS, max_cpu, max_memory)
        aws_instances.append(flavors)

    return gcp_instances, aws_instances

def get_matching_instance_with_PD_OS(doc):

    gcp_instances = []
    aws_instances = []

    for machine in doc:
        max_cpu, max_memory, disk, os = get_max_resources_utilized(machine)

        flavors = getMatchingInstanceInGCE(GC_FLAVORS, max_cpu, max_memory)
        gcp_instances.append([flavors[0]['name'], disk, os])

        flavors = getMatchingInstanceInAWS(AWS_FLAVORS, max_cpu, max_memory)
        aws_instances.append([flavors[0]['name'], disk, os])

    return gcp_instances, aws_instances

def get_cost_of_recommended_instances_on_AWS(recommendedInstances):
    recommendedInstancesAndCost = []
    totalCost = 0
    for instance in recommendedInstances:
        instanceCost = read_EC2_ondemand_instance_prices(1, 'us-east-1', instance[0], instance[2])
        persistentDiskCost = aws_storage_prices('us-east-1', instance[1])
        totalInstanceCost = instanceCost + persistentDiskCost
        totalCost += totalInstanceCost
        recommendedInstancesAndCost.append([instance[0], totalInstanceCost])

    return recommendedInstancesAndCost, totalCost

def get_cost_of_recommended_instances_on_GCP(recommendedInstances):

    recommendedInstancesAndCost = []
    totalCost = 0

    for instance in recommendedInstances:
        instanceCost = gce_price(1,'regular', 'us', instance[0], instance[1], instance[2])
        totalCost += instanceCost

        recommendedInstancesAndCost.append([instance[0], instanceCost])

    return recommendedInstancesAndCost, totalCost


if __name__ == '__main__':

    machine = get_nodes_in_cluster()
    print get_cost_of_recommended_instances_on_GCP(get_matching_instance_with_PD_OS(machine)[0])
