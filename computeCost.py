#!/usr/bin/env python

import csv
import sys
import json
import re

#computes the estimated monthly prices of running AWS instances
def read_EC2_ondemand_instance_prices(number, region, flavor, os):
	if os == "darwin" or os=="POSIX":
		os="linux"
	if number <=0:
		return 0
	ifile  = open('EC2_OnDemand.csv', "r")

	reader = csv.reader(ifile)

	unit_cost = 0
	rownum = 0
	for row in reader:

	    if rownum != 0:
	    	if row[0]==region and row[1] ==flavor and row[2]==os:
		    	unit_cost = row[3]
		     	break

	    rownum += 1
	ifile.close()

	cost = float(unit_cost) * int(number)
	total_price = cost * (30.5 * 24)
	return (total_price)
#computes the monthly storage cost on AWS
def aws_storage_prices(region, storage_size):
	'''
	config = json.loads(open("pricing-storage-s3.json").read())
	storage_cost = 0
	monthly_Storage_Cost = 0
	#print [0]['tiers'][0]['storageTypes'][0]['prices']['USD']
	data_centers = config['config']['regions']

	for data_center in data_centers:

		if region==data_center['region']:
			storage_cost = data_center['tiers'][1]['storageTypes'][0]['prices']['USD']
			break

	#print storage_cost
	'''
	return float(0.045) * int(storage_size)
		#print region['region'], region['tiers'][0]['storageTypes'][0]['prices']['USD']
	#print monthly_Storage_Cost

#computes the an estimated mponthly cost of running instances on google cloud
def gce_price(instances, vm_class, zone, machine_type, storage_size, os):

	config = json.loads(open("Google pricelist.json").read())
	sustained_use_discount = 0.7
	flavor_hourly_cost = config['gcp_price_list']['CP-COMPUTEENGINE-VMIMAGE-'+machine_type][zone]
	paid_os_cost= 0
	#local_SSD_cost = ssd_number * 81.75 * instances
	vCPUs = 0
	pd_storage_cost = storage_size * float(config['gcp_price_list']['CP-COMPUTEENGINE-STORAGE-PD-CAPACITY']['us'])
	average_monthly_hours = (30.5 * 24)#(((720*4) + (744*7) + (28*24*1))/12)
	#get the number of vCPUs for instances not F1-MICRO and G1-SMALL
	if machine_type!="F1-MICRO" and machine_type!="G1-SMALL":
		vCPUs = int(re.search("(?<=\-)\d+", machine_type).group())

	#gets the cost of paid operating systems on gc compute engine,
	#such as win, suse, and rhel
	if os == "rhel":
		if vCPUs <= 4:
			paid_os_cost = instances* float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['low'])* average_monthly_hours
		else:
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['high'])* average_monthly_hours
	if os == "suse":
		if machine_type == "F1-MICRO" or machine_type=="G1-SMALL":
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['low'])* average_monthly_hours
		else:
			paid_os_cost = instances* float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['high'])*average_monthly_hours

	if os == "win":
		if machine_type == "F1-MICRO" or machine_type=="G1-SMALL":
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['low'])* average_monthly_hours
		else:
			paid_os_cost = instances * vCPUs * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['high']) * average_monthly_hours


	if vm_class == "preemtible":
		monthly_cost = (instances * float(flavor_hourly_cost) * average_monthly_hours)
	else:
		monthly_cost = (instances * float(flavor_hourly_cost) * average_monthly_hours) * sustained_use_discount

	total_monthly_cost = (monthly_cost + paid_os_cost)

	total_vms_monthly_cost = pd_storage_cost + total_monthly_cost

	return total_vms_monthly_cost
