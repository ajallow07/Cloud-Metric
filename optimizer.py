 #! /usr/bin/env python

import config
import math
import mapping, computeCost
from computeCost import read_EC2_ondemand_instance_prices, aws_storage_prices, gce_price
from mapping import getMatchingInstances, AWS_FLAVORS, GC_FLAVORS
from config import NODE_COLLECTION as nc, REPORT_COLLECTION as rc
#Node for support of  multi cluster , we will need cluster Id identification


def get_machine_resources(machine):
    vcpu = 0
    mem = 0
    strg = 0
    opsys = ''
    for resource in nc.find({"node":machine}, {"cpu":1,"memory":1, "disk":1, "os":1, "_id":0}):
        vcpu = resource['cpu']
        mem = float(resource['memory'])
        strg = float(resource['disk'])
        opsys = resource['os']
    return vcpu, mem, strg, opsys

def get_nodes_in_cluster(cluster):
    machines_in_cluster = []
    #get_node_name = function(doc) { return doc.node }
    for machine in nc.find({"cluster_id":cluster}, {"node":1,"_id":0}):
        machines_in_cluster.append(machine['node'])
    return machines_in_cluster

def get_max_resources_utilized(machine):
    cpu_percent = 0
    optimizedCPU = 0
    optimizedMem = 0
    percent_val = 100
    #time_horizon = 48 #2 days of of resources utilization
    mem_percent = 0
    #disk_percent = 0
    cpu_size, mem_size, disk_size, os = get_machine_resources(machine)

    avg_CPU_And_Mem_Utilization = [{ "$group": {"_id": { "node": machine},
    "avgCPU": {"$avg": "$cpu.user"}, "avgMemory" :{ "$avg": "$memory"}}}]

    #average CPU and Memory Utilication over time
    for avg in rc.aggregate(avg_CPU_And_Mem_Utilization):
        cpu_percent = avg['avgCPU']
        mem_percent = avg['avgMemory']

    #find({"node":machine}, {"_id":0, "cpu.user":1}).sort([("cpu.user",-1)]).limit(1):
    #highest memory usage over time period
    #for max_mem in rc.find({"node":machine}, {"_id":0, "memory":1}).sort([("memory",-1)]).limit(1):
          #mem_percent = max_mem['memory']

    optimizedCPU = math.ceil(cpu_percent/percent_val * cpu_size)
    optimizedMem = math.ceil((mem_percent)/percent_val * mem_size)

    #handle cpu not a power of 2
    if optimizedCPU > 0:
        expVal = math.log(optimizedCPU, 2)
        if (expVal - int(expVal)) > 0:
            optimizedCPU = int(2**math.ceil(math.log(optimizedCPU,2)))

    return optimizedCPU, optimizedMem, math.ceil(disk_size), os

#retrieve matching instance on AWS and GCP based on the usage data
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

def get_matching_instance_with_PD_OS(cluster):

    gcp_instances = []
    aws_instances = []

    for machine in cluster:
        max_cpu, max_memory, disk, os = get_max_resources_utilized(machine)

        flavorsGCP = getMatchingInstances(GC_FLAVORS, max_cpu, max_memory)
        if flavorsGCP:
            gcp_instances.append([flavorsGCP[0]['name'], disk, os])

        flavorsAWS = getMatchingInstances(AWS_FLAVORS, max_cpu, max_memory)

        if flavorsAWS:
            aws_instances.append([flavorsAWS[0]['name'], disk, os])

    return gcp_instances, aws_instances

def get_cost_of_recommended_instances_on_AWS(recommendedInstances):
    recommendedInstancesAndCost = []
    defaultRegion = 'us-east-1'
    totalCost = 0
    for instance in recommendedInstances:
        instanceCost = read_EC2_ondemand_instance_prices(1, defaultRegion, instance[0], instance[2].lower())
        persistentDiskCost = aws_storage_prices(defaultRegion, instance[1])

        totalInstanceCost = instanceCost + persistentDiskCost
        totalCost += totalInstanceCost
        recommendedInstancesAndCost.append([instance[0], totalInstanceCost])

    return recommendedInstancesAndCost, totalCost

def get_cost_of_recommended_instances_on_GCP(recommendedInstances):
    defaultRegion = 'us'
    vm_class = 'regular'
    recommendedInstancesAndCost = []
    totalCost = 0

    for instance in recommendedInstances:
        instanceCost = gce_price(1, vm_class ,defaultRegion , instance[0], instance[1], instance[2])
        if instanceCost:
            totalCost += instanceCost
            recommendedInstancesAndCost.append([instance[0], instanceCost])

    return recommendedInstancesAndCost, totalCost

if __name__ == '__main__':
    print get_machine_resources('aj-hadoop-slave-1')
    print get_max_resources_utilized("aj-hadoop-slave-1")
    print get_max_resources_utilized("aj-hadoop-slave-2")

    print get_matching_instance_with_PD_OS("Test")
