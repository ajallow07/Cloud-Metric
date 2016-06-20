  #!/usr/bin/env python
import csv, os
import sys
import json
import re

#computes the estimated monthly prices of running AWS instances

def read_EC2_ondemand_instance_prices(number, region, flavor, ops):
	AWS_DATA = os.path.abspath('EC2_OnDemand.csv')
	if ops == "darwin" or os=="POSIX":
		ops="linux"
	if number <=0:
		return 0
	ifile  = open(AWS_DATA, "r")

	reader = csv.reader(ifile)

	unit_cost = 0
	rownum = 0
	for row in reader:

	    if rownum != 0:
	    	if row[0]==region and row[1] ==flavor and row[2]==ops:
		    	unit_cost = row[3]
		     	break

	    rownum += 1
	ifile.close()

	cost = float(unit_cost) * int(number)
	total_price = cost * (30.5 * 24)
	return (total_price)

#compute On-demand prices on
#computes the monthly storage cost on AWS
def aws_storage_prices(region, storage_size):
	#uses magnetic volumes pricing
	return float(0.050) * int(storage_size)

def aws_on_demand_costs(number, region, flavor, storage_size, ops, usage_percent):
	on_demand_usage_cost = []
	on_demand_hours = 30.5 * 24 * float(usage_percent)/float(100)
	AWS_DATA = os.path.abspath('EC2_OnDemand.csv')
	if ops == "darwin" or os=="POSIX":
		ops="linux"
	if number <=0:
		return 0
	ifile  = open(AWS_DATA, "r")
	reader = csv.reader(ifile)

	unit_cost = 0
	rownum = 0
	for row in reader:
	    if rownum != 0:
	    	if row[0]==region and row[1] ==flavor and row[2]==ops:
		    	unit_cost = row[3]
		     	break
	    rownum += 1

	ifile.close()
	total_cost = float(format((float(unit_cost) * number * on_demand_hours), '.2f'))

	on_demand_usage_cost.append(usage_percent)
	on_demand_usage_cost.append(total_cost)

	return on_demand_usage_cost
#get the unit cost of an aws instance over percentage of usage in month
def get_aws_instance_unit_cost(region, flavor, ops, percentage_usage):
	on_demand_unit_cost = []
	AWS_DATA = os.path.abspath('EC2_OnDemand.csv')
	if ops == "darwin" or os=="POSIX":
		ops="linux"

	ifile  = open(AWS_DATA, "r")
	reader = csv.reader(ifile)
	unit_cost = 0
	rownum = 0
	for row in reader:
	    if rownum != 0:
	    	if row[0]==region and row[1] ==flavor and row[2]==ops:
		    	unit_cost = row[3]
		     	break
	    rownum += 1
	ifile.close()
	on_demand_unit_cost.append(percentage_usage)
	on_demand_unit_cost.append(float(unit_cost))

	return on_demand_unit_cost
#get the unit cost of an gcp ce instance over percentage of usage in month
def get_gcp_instance_unit_cost(zone, machine_type, ops, usage_percent):
	On_demand_usage_cost = []
	GC_DATA = os.path.abspath('Google_pricelist.json')
	config = json.loads(open(GC_DATA).read())

	hourly_cost = config['gcp_price_list']['CP-COMPUTEENGINE-VMIMAGE-'+machine_type][zone]

	paid_os_cost = 0
	vCPUs = 0

	#get the number of vCPUs for instances not F1-MICRO and G1-SMALL
	if machine_type!="F1-MICRO" and machine_type!="G1-SMALL":
		vCPUs = int(re.search("(?<=\-)\d+", machine_type).group())

	#100% is charge for usage below 25%
	if usage_percent <= 25:
		hourly_cost *= 1
	elif usage_percent <= 50:
		hourly_cost *= 0.80

	elif usage_percent <= 75:
		hourly_cost *= 0.60
	else:
		hourly_cost *= 0.40
	#gets the cost of paid operating systems on gc compute engine,
	#such as win, suse, and rhel
	if ops == "rhel":
		if vCPUs <= 4:
			paid_os_cost = float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])
		else:
			paid_os_cost = float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['high'])
	if ops== "suse":
		if machine_type == "F1-MICRO" or machine_type=="G1-SMALL":
			paid_os_cost = float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])
		else:
			paid_os_cost = float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['high'])
	if ops == "win":
		if machine_type == "F1-MICRO" or machine_type=="G1-SMALL":
			paid_os_cost = float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])* on_demand_hours
		else:
			paid_os_cost = vCPUs * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['high'])

	on_demand_unit_cost = float(format((float(hourly_cost) + paid_os_cost),'.3f'))

	On_demand_usage_cost.append(usage_percent)
	On_demand_usage_cost.append(on_demand_unit_cost)

	return On_demand_usage_cost

#computes the an estimated mponthly cost of running instances on google cloud
def gce_price(instances, vm_class, zone, machine_type, storage_size, ops):
	GC_DATA = os.path.abspath('Google_pricelist.json')
	config = json.loads(open(GC_DATA).read())
	sustained_use_discount = 0.7
	flavor_hourly_cost = config['gcp_price_list']['CP-COMPUTEENGINE-VMIMAGE-'+machine_type][zone]
	paid_os_cost= 0
	#local_SSD_cost = ssd_number * 81.75 * instances
	vCPUs = 0
	pd_storage_cost = storage_size * float(config['gcp_price_list']['CP-COMPUTEENGINE-STORAGE-PD-CAPACITY']['us'])
	average_monthly_hours = (30.5 * 24)

	#get the number of vCPUs for instances not F1-MICRO and G1-SMALL
	if machine_type!="F1-MICRO" and machine_type!="G1-SMALL":
		vCPUs = int(re.search("(?<=\-)\d+", machine_type).group())

	#gets the cost of paid operating systems on gc compute engine,
	#such as win, suse, and rhel
	if ops == "rhel":
		if vCPUs <= 4:
			paid_os_cost = instances* float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])* average_monthly_hours
		else:
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['high'])* average_monthly_hours
	if ops== "suse":
		if machine_type == "F1-MICRO" or machine_type=="G1-SMALL":
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])* average_monthly_hours
		else:
			paid_os_cost = instances* float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['high'])*average_monthly_hours

	if ops == "win":
		if machine_type == "F1-MICRO" or machine_type=="G1-SMALL":
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])* average_monthly_hours
		else:
			paid_os_cost = instances * vCPUs * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['high']) * average_monthly_hours

	if vm_class == "preemtible":
		monthly_cost = (instances * float(flavor_hourly_cost) * average_monthly_hours)
	else:
		monthly_cost = (instances * float(flavor_hourly_cost) * average_monthly_hours) * sustained_use_discount

	total_monthly_cost = (monthly_cost + paid_os_cost)

	total_vms_monthly_cost = pd_storage_cost + total_monthly_cost

	return total_vms_monthly_cost


#computes the estimated cost based on percentage of usage in  the month
def gce_on_demand_costs(instances, zone, machine_type, storage_size, ops, usage_percent):
	On_demand_usage_cost = []
	sustained_use_discount = 1
	GC_DATA = os.path.abspath('Google_pricelist.json')
	config = json.loads(open(GC_DATA).read())

	hourly_cost = config['gcp_price_list']['CP-COMPUTEENGINE-VMIMAGE-'+machine_type][zone]
	on_demand_hours = 30 * 24
	paid_os_cost= 0
	vCPUs = 0

	pd_storage_cost =  (float(usage_percent)/float(100)) * storage_size * float(config['gcp_price_list']['CP-COMPUTEENGINE-STORAGE-PD-CAPACITY']['us'])

	#get the number of vCPUs for instances not F1-MICRO and G1-SMALL
	if machine_type!="F1-MICRO" and machine_type!="G1-SMALL":
		vCPUs = int(re.search("(?<=\-)\d+", machine_type).group())

	#100% is charge for usage below 25%
	if usage_percent <= 25:
		hourly_cost *= 1
		on_demand_hours  *= (float(usage_percent)/float(100))
	elif usage_percent <= 50:
		hourly_cost *= 0.80
		on_demand_hours  *= (float(usage_percent - 25)/float(100))
	elif usage_percent <= 75:
		hourly_cost *= 0.60
		on_demand_hours  *= (float(usage_percent - 50)/float(100))
	else:
		hourly_cost *= 0.40
		on_demand_hours  *= (float(usage_percent - 75)/float(100))
	#gets the cost of paid operating systems on gc compute engine,
	#such as win, suse, and rhel
	if ops == "rhel":
		if vCPUs <= 4:
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])* on_demand_hours
		else:
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['high'])* on_demand_hours
	if ops== "suse":
		if machine_type == "F1-MICRO" or machine_type=="G1-SMALL":
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])* on_demand_hours
		else:
			paid_os_cost = instances* float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['high'])*on_demand_hours
	if ops == "win":
		if machine_type == "F1-MICRO" or machine_type=="G1-SMALL":
			paid_os_cost = instances * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][ops]['low'])* on_demand_hours
		else:
			paid_os_cost = instances * vCPUs * float(config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['high']) * on_demand_hours

	on_demand_cost = instances * float(hourly_cost) * on_demand_hours

	total_on_demand_cost = float(format((on_demand_cost + paid_os_cost), '.2f'))

	On_demand_usage_cost.append(usage_percent)
	On_demand_usage_cost.append(total_on_demand_cost)

	return On_demand_usage_cost
	
'''
if __name__ == '__main__':

	print get_aws_instance_unit_cost('us-east-1', 'm3.large','linux', 100)
	print get_gcp_instance_unit_cost('us', 'N1-STANDARD-1','linux', 35)
'''
