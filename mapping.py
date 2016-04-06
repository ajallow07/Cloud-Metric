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

AWS_FLAVORS = ["t2.nano","t2.micro","t2.small","t2.medium", "t2.large","m4.large","m3.medium","m3.xlarge","m3.large","c4.large","c3.large","r3.large","m4.2xlarge",
    "r3.xlarge", "i2.xlarge" ,"i2.2xlarge" ,"i2.4xlarge","i2.8xlarge","c3.xlarge","c4.xlarge"
    "m4.4xlarge","m3.2xlarge","m4.10xlarge","m4.xlarge"
    "c4.2xlarge", "c4.4xlarge","c4.8xlarge","c3.2xlarge","c3.4xlarge","c3.8xlarge","g2.2xlarge","g2.8xlarge",
    "r3.2xlarge", "r3.4xlarge", "r3.8xlarge",
     "d2.xlarge","d2.2xlarge","d2.4xlarge","d2.8xlarge "]

GC_FLAVORS = ["F1-MICRO","G1-SMALL", "N1-STANDARD-1" , "N1-STANDARD-2", "N1-STANDARD-4", "N1-STANDARD-8",
            "N1-STANDARD-16", "N1-STANDARD-32", "N1-HIGHMEM-2", "N1-HIGHMEM-4", "N1-HIGHMEM-8",
            "N1-HIGHMEM-16", "N1-HIGHMEM-32"
            ,"N1-HIGHCPU-2","N1-HIGHCPU-4","N1-HIGHCPU-8","N1-HIGHCPU-16","N1-HIGHCPU-32"]

def getClosestMatchingInstanceInAWS(vcpu, memory):

    return (FlavorName)
