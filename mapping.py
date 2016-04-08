#! /usr/bin/env python


"""
In this file, we search through the Google and Amazon pricing data and gives
the most optimal (flavor which is closest of match to the a given instance parameters)
instance that matches or is closest to the choices of input parameters
, These parameters of instances are: os, vCPU, memory. We will also consider storage choices as well

1. A method that takes in input paramters and return a flavor for each of Google and Amazon
2. Methods that takes a flavor instances and compute compute the cost (done)
3.
"""
AWS_FLAVORS = [{"t2.nano": {"vCPU": 1,"memory": 0.5}},
                {"t2.micro": {"vCPU": 1,"memory": 1}},
                {"t2.small": {"vCPU": 1,"memory": 2}},
                {"t2.medium" : {"vCPU": 2,"memory": 4}},
                {"t2.large" : {"vCPU": 2,"memory": 8}},
                {"m4.large" : {"vCPU": 2,"memory": 8}},
                {"m3.medium": {"vCPU": 1,"memory": 3.75}},
                {"m3.xlarge": {"vCPU": 2,"memory": 15}},
                {"m3.large": {"vCPU": 2,"memory": 7.5}},
                {"c4.large":{"vCPU":2,"memory": 3.75}},
                {"c3.large": {"vCPU": 2,"memory": 3.75}},
                {"r3.large" : {"vCPU": 2,"memory": 15}},
                {"m4.2xlarge": {"vCPU": 2,"memory": 32}},
                {"r3.xlarge" : {"vCPU": 4,"memory": 30.5}},
                {"i2.xlarge": {"vCPU": 4,"memory": 30.5}} ,
                {"i2.2xlarge" : {"vCPU":8,"memory": 61}},
                {"i2.4xlarge" : {"vCPU": 16,"memory": 122}},
                {"i2.8xlarge" : {"vCPU": 32,"memory": 244}},
                {"c3.xlarge": {"vCPU": 4,"memory": 7.5}},
                {"c4.xlarge" : {"vCPU": 4,"memory": 7.5}},
                {"m4.4xlarge" : {"vCPU": 16,"memory": 64}},
                {"m3.2xlarge": {"vCPU":8,"memory": 30}},
                {"m4.10xlarge" : {"vCPU": 40,"memory": 160}},
                {"m4.xlarge" : {"vCPU": 4,"memory": 16}},
                {"c4.2xlarge": {"vCPU": 8,"memory": 15}},
                {"c4.4xlarge": {"vCPU": 16,"memory": 30}},
                {"c4.8xlarge": {"vCPU": 32,"memory": 60}},
                {"c3.2xlarge" : {"vCPU": 8,"memory": 15}},
                {"c3.4xlarge",: {"vCPU": 16,"memory": 30}}
                {"c3.8xlarge": {"vCPU": 32,"memory": 60}},
                {"g2.2xlarge": {"vCPU": 8,"memory": 15}},
                {"g2.8xlarge": {"vCPU": 32,"memory": 60}},
                {"r3.2xlarge": {"vCPU": 8,"memory": 61}},
                {"r3.4xlarge": {"vCPU": 16,"memory": 122}},
                {"r3.8xlarge": {"vCPU": 32,"memory": 244}},
                {"d2.xlarge": {"vCPU": 4,"memory": 30.5}},
                {"d2.2xlarge" : {"vCPU":8,"memory": 61}},
                {"d2.4xlarge": {"vCPU":16,"memory": 122}},
                {"d2.8xlarge": {"vCPU": 22,"memory": 244}}
                ]

GC_FLAVORS = [   {"F1-MICRO" : {"vCPU": 1,"memory": 0.60}},
                {"G1-SMALL" : {"vCPU": 1,"memory": 1.70}},
                {"N1-STANDARD-1": {"vCPU": 1,"memory": 3.75}} ,
                {"N1-STANDARD-2": {"vCPU": 2,"memory": 7.5}},
                {"N1-STANDARD-4": {"vCPU": 4,"memory": 15}},
                {"N1-STANDARD-8": {"vCPU": 8,"memory": 30}},
                {"N1-STANDARD-16": {"vCPU": 16,"memory": 60}},
                {"N1-STANDARD-32": {"vCPU": 32,"memory": 120}},
                {"N1-HIGHMEM-2": {"vCPU": 2,"memory": 13}},
                {"N1-HIGHMEM-4": {"vCPU": 4,"memory": 26}},
                {"N1-HIGHMEM-8": {"vCPU": 8,"memory": 52}},
                {"N1-HIGHMEM-16": {"vCPU": 16,"memory": 104}},
                {"N1-HIGHMEM-32": {"vCPU": 32,"memory":208}},
                {"N1-HIGHCPU-2": {"vCPU": 2,"memory": 1.80}},
                {"N1-HIGHCPU-4": {"vCPU": 4,"memory": 3.60},
                {"N1-HIGHCPU-8": {"vCPU": 8,"memory": 7.20}},
                {"N1-HIGHCPU-16": {"vCPU": 16,"memory": 14.40}},
                {"N1-HIGHCPU-32": {"vCPU": 32,"memory": 28.80}}
            ]

def getClosestMatchingInstanceInAWS(awsflavors, vcpu, memory):

    return none
