#! /usr/bin/env python

import csv, sys, json, re
import multiprocessing, os, re, sys, time

"""
In this file, we search through the Google and Amazon pricing data and gives
the most optimal (flavor which is closest of match to the a given instance parameters)
instance that matches or is closest to the choices of input parameters
, These parameters of instances are: os, vCPU, memory. We will also consider storage choices as well

1. A method that takes in input paramters and return a flavor for each of Google and Amazon
2. Methods that takes a flavor instances and compute compute the cost (done)
3.
"""
AWS_FLAVORS = [{"name": "t2.nano", "param" :{"vCPU": 1,"memory": 0.5}, "mf": 0},
                {"name":"t2.micro","param": {"vCPU": 1,"memory": 1},"mf": 0},
                {"name":"t2.small", "param": {"vCPU": 1,"memory": 2},"mf": 0},
                {"name":"t2.medium", "param" : {"vCPU": 2,"memory": 4},"mf": 0},
                {"name":"t2.large" , "param": {"vCPU": 2,"memory": 8},"mf": 0},
                {"name":"m4.large" , "param": {"vCPU": 2,"memory": 8},"mf": 0},
                {"name":"m3.medium", "param": {"vCPU": 1,"memory": 3.75},"mf": 0},
                {"name":"m3.xlarge", "param": {"vCPU": 2,"memory": 15},"mf": 0},
                {"name":"m3.large", "param": {"vCPU": 2,"memory": 7.5},"mf": 0},
                {"name":"c4.large", "param": {"vCPU":2,"memory": 3.75},"mf": 0},
                {"name":"c3.large", "param": {"vCPU": 2,"memory": 3.75},"mf": 0},
                {"name":"r3.large" , "param": {"vCPU": 2,"memory": 15},"mf": 0},
                {"name":"m4.2xlarge", "param": {"vCPU": 2,"memory": 32},"mf": 0},
                {"name":"r3.xlarge" , "param": {"vCPU": 4,"memory": 30.5},"mf": 0},
                {"name":"i2.xlarge", "param": {"vCPU": 4,"memory": 30.5},"mf": 0} ,
                {"name":"i2.2xlarge", "param" : {"vCPU":8,"memory": 61},"mf": 0},
                {"name":"i2.4xlarge" , "param": {"vCPU": 16,"memory": 122},"mf": 0},
                {"name":"i2.8xlarge", "param" : {"vCPU": 32,"memory": 244},"mf": 0},
                {"name":"c3.xlarge", "param": {"vCPU": 4,"memory": 7.5},"mf": 0},
                {"name":"c4.xlarge" , "param": {"vCPU": 4,"memory": 7.5},"mf": 0},
                {"name":"m4.4xlarge", "param" : {"vCPU": 16,"memory": 64},"mf": 0},
                {"name":"m3.2xlarge", "param": {"vCPU":8,"memory": 30},"mf": 0},
                {"name":"m4.10xlarge" , "param": {"vCPU": 40,"memory": 160},"mf": 0},
                {"name":"m4.xlarge" , "param": {"vCPU": 4,"memory": 16},"mf": 0},
                {"name":"c4.2xlarge", "param": {"vCPU": 8,"memory": 15},"mf": 0},
                {"name":"c4.4xlarge", "param": {"vCPU": 16,"memory": 30},"mf": 0},
                {"name":"c4.8xlarge", "param": {"vCPU": 32,"memory": 60},"mf": 0},
                {"name":"c3.2xlarge" , "param": {"vCPU": 8,"memory": 15},"mf": 0},
                {"name":"c3.4xlarge", "param": {"vCPU": 16,"memory": 30},"mf": 0},
                {"name":"c3.8xlarge" , "param": {"vCPU": 32,"memory": 60},"mf": 0},
                {"name":"g2.2xlarge", "param": {"vCPU": 8,"memory": 15},"mf": 0},
                {"name":"g2.8xlarge", "param": {"vCPU": 32,"memory": 60},"mf": 0},
                {"name":"r3.2xlarge", "param": {"vCPU": 8,"memory": 61},"mf": 0},
                {"name":"r3.4xlarge", "param": {"vCPU": 16,"memory": 122},"mf": 0},
                {"name":"r3.8xlarge", "param": {"vCPU": 32,"memory": 244},"mf": 0},
                {"name":"d2.xlarge", "param": {"vCPU": 4,"memory": 30.5},"mf": 0},
                {"name":"d2.2xlarge", "param": {"vCPU":8,"memory": 61},"mf": 0},
                {"name":"d2.4xlarge", "param": {"vCPU":16,"memory": 122},"mf": 0},
                {"name":"d2.8xlarge", "param": {"vCPU": 22,"memory": 244},"mf": 0}
                ]

GC_FLAVORS = [   {"name":"F1-MICRO" , "param": {"vCPU": 1, "memory": 0.60},"mf": 0},
                {"name":"G1-SMALL" , "param": {"vCPU": 1, "memory": 1.70},"mf": 0},
                {"name":"N1-STANDARD-1", "param": {"vCPU": 1, "memory": 3.75},"mf": 0},
                {"name":"N1-STANDARD-2", "param": {"vCPU": 2, "memory": 7.5},"mf": 0},
                {"name":"N1-STANDARD-4", "param": {"vCPU": 4, "memory": 15},"mf": 0},
                {"name":"N1-STANDARD-8", "param": {"vCPU": 8, "memory": 30},"mf": 0},
                {"name":"N1-STANDARD-16", "param": {"vCPU": 16, "memory": 60},"mf": 0},
                {"name":"N1-STANDARD-32", "param": {"vCPU": 32, "memory": 120},"mf": 0},
                {"name":"N1-HIGHMEM-2", "param": {"vCPU": 2, "memory": 13},"mf": 0},
                {"name":"N1-HIGHMEM-4", "param": {"vCPU": 4, "memory": 26},"mf": 0},
                {"name":"N1-HIGHMEM-8", "param": {"vCPU": 8, "memory": 52},"mf": 0},
                {"name":"N1-HIGHMEM-16", "param": {"vCPU": 16, "memory": 104},"mf": 0},
                {"name":"N1-HIGHMEM-32", "param": {"vCPU": 32, "memory":208},"mf": 0},
                {"name":"N1-HIGHCPU-2", "param": {"vCPU": 2,"memory": 1.80},"mf": 0},
                {"name":"N1-HIGHCPU-4", "param": {"vCPU": 4, "memory": 3.60},"mf": 0},
                {"name":"N1-HIGHCPU-8", "param": {"vCPU": 8, "memory": 7.20},"mf": 0},
                {"name":"N1-HIGHCPU-16", "param": {"vCPU": 16, "memory": 14.40},"mf": 0},
                {"name":"N1-HIGHCPU-32", "param": {"vCPU": 32, "memory": 28.80},"mf": 0}
            ]

def getMatchingInstanceInAWS(awsflavors, vcpu, memory):
    for flavor in awsflavors:
        #get the absolute differences in vCPU and memory usages
        flavor['mf'] = abs(vcpu-flavor['param']['vCPU']) + abs(memory - flavor['param']['memory'])

    matchingFavors = []
    minimumDiff = 10000

    for flavor in awsflavors:
        if flavor['mf'] < minimumDiff:
            minimumDiff = flavor['mf']

    for flavor in awsflavors:
        if flavor["mf"] == minimumDiff:
            matchingFavors.append(flavor['name'])

    return matchingFavors

def getMatchingInstanceInGCE(gceflavors, vcpu, memory):
    matchingFavors = []
    minimumDiff = 10000

    for flavor in gceflavors:
        #get the absolute differences in vCPU and memory usages
        flavor['mf'] = abs(vcpu-flavor['param']['vCPU']) + abs(memory - flavor['param']['memory'])
        if flavor['mf'] < minimumDiff:
            minimumDiff = flavor['mf']

    for flavor in gceflavors:
        if flavor["mf"] == minimumDiff:
            matchingFavors.append(flavor['name'])
    return matchingFavors


def averageCostOnGCP():


    return 0

def averageCostOnAWS():


    return 0
