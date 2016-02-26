#!/usr/bin/env python

import csv
import sys
import json


def read_EC2_ondemand_instance_prices(number, region, flavor, os):
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
	return cost

def aws_storage_prices(region, storage_size):

	config = json.loads(open("pricing-storage-s3.json").read())
	storage_cost = 0
	monthly_Storage_Cost = 0
	#print [0]['tiers'][0]['storageTypes'][0]['prices']['USD']
	data_centers = config['config']['regions']

	for data_center in data_centers:
		
		if region==data_center['region']:
			storage_cost = data_center['tiers'][0]['storageTypes'][0]['prices']['USD']
			break

	#print storage_cost

	return float(storage_cost) * int(storage_size)
		#print region['region'], region['tiers'][0]['storageTypes'][0]['prices']['USD']
	#print monthly_Storage_Cost


def gce_price(instances, zone, machine_type, storage_size, os):
	
	config = json.loads(open("Google pricelist.json").read())
	sustained_use_discount = 0.3
	flavor_hourly_cost = config['gcp_price_list']['CP-COMPUTEENGINE-VMIMAGE-'+machine_type][zone]
	paid_os_cost= 0
	local_SSD_cost =0

	#if os != "linux":
		#Paid_OS = config['gcp_price_list']['CP-COMPUTEENGINE-OS'][os]['low']

	average_monthly_hours = (((720*4) + (744*7) + (29*24*1))/12)
	monthly_cost = (instances * float(flavor_hourly_cost)*average_monthly_hours)
	total_monthly_cost = (monthly_cost + local_SSD_cost + paid_os_cost)

	return total_monthly_cost







if __name__ == "__main__":
	'''
	if len(sys.argv) <= 5:

		print "Usage:[number of instances] [region] [flavor] [os] [storage-size]"


	INSTANCE_NUMBER = sys.argv[1]
	REGION = sys.argv[2];
	FLAVOR = sys.argv[3];
	OS = sys.argv[4]
	STORAGE_SIZE = sys.argv[5]
	'''
	machine_types = ["t2.nano","t2.micro","t2.large","m4.large","m3.large","c4.large","c3.large","r3.large","m4.2xlarge", "m4.4xlarge","m3.2xlarge",
		"c4.2xlarge", "c4.4xlarge","c4.8xlarge","c3.2xlarge","c3.4xlarge","c3.8xlarge","g2.2xlarge","g2.8xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge", 
		"d2.2xlarge","d2.4xlarge","d2.8xlarge "]

	aws_regions = ["us-east-1","us-west-1","us-west-2","eu-west-1","eu-central-1","ap-southeast-1","ap-northeast-1","ap-southeast-2","ap-northeast-2"
				,"sa-east-1","us-gov-west-1"]

	gce_regions = ["us", "europe","asia"]

	platforms = ["linux","rhel", "sles","mswin","mswinSQL","mswinSQLWeb"]

	gce_OS = ["linux", "rhel", "suse","win"]

	
	user_choice = input("Please select cloud provider: \n1) Amazon Web Services\n2) Google Cloud\n")

	if user_choice==1:
		#selects regions 
		region_option = "Please, select region: (0-"+str(len(aws_regions)-1)+")\n"
		for region in aws_regions:

			region_option += str(aws_regions.index(region))+") "+region + "\n"
		
		chosen_region = input(region_option)

		#type number of instances required
		intance_number = input("Please type number of instances: \n")

		#selects machine types for AWS
		flavor_options = "Please, select machine type: (0-"+str(len(machine_types)-1)+")\n"
		for machine in machine_types:

			flavor_options += str(machine_types.index(machine))+") "+machine+"\n"
		
		chosen_flavor = input(flavor_options)

		#selects operating systems types for AWS
		os_options = "Please, select OS: (0-"+str(len(platforms)-1)+")\n"

		for os in platforms:

			os_options += str(platforms.index(os))+") "+os+"\n"
		
		chosen_os = input(os_options)
		
		storage_size = input("Please, enter storage size: ")


		price = read_EC2_ondemand_instance_prices(intance_number, aws_regions[chosen_region], machine_types[chosen_flavor], platforms[chosen_os]);

		storage_price  = aws_storage_prices(aws_regions[chosen_region], storage_size)

		#print storage_price
		print "You selected: "+str(intance_number)+ ", "+str(aws_regions[chosen_region])+", "+str(machine_types[chosen_flavor])+", "+str(platforms[chosen_os])+ ", "+str(storage_size)
		print "The hourly price of the instance:  \t$%.3f "% (price/int(intance_number))

		total_price = price * (((720*4) + (744*7) + (28*24*1))/12)
		#print total_price
		print "Cost of storage: \t$%.2f " % (storage_price)
		print "Monthly cost of the instance + storage = \t$%.2f " %( total_price + storage_price); 
		print "\n\n"

		#print aws_storage_prices(REGION, STORAGE_SIZE)
	else:

		print "Estimates on Google Cloud is coming soon ...."
		
	#selects regions 
	
	gce_regions = ["us", "europe","asia"]

	gce_machine_types = ["F1-MICRO","G1-SMALL", "N1-STANDARD-1" , "N1-STANDARD-2", "N1-STANDARD-4", "N1-STANDARD-8", 
						"N1-STANDARD-16", "N1-STANDARD-32", "N1-HIGHMEM-2", "N1-HIGHMEM-4", "N1-HIGHMEM-8", "N1-HIGHMEM-16", "N1-HIGHMEM-32"
						,"N1-HIGHCPU-2","N1-HIGHCPU-4","N1-HIGHCPU-8","N1-HIGHCPU-16","N1-HIGHCPU-32"]

	gce_preemtible = "-PREEMPTIBLE"

	platforms = ["linux","rhel", "sles","mswin","mswinSQL","mswinSQLWeb"]

	gce_OS = ["linux", "rhel", "suse","win"]

	region_option = "Please, select region: (0-"+str(len(gce_regions)-1)+")\n"
	for region in gce_regions:

		region_option += str(gce_regions.index(region))+") "+region + "\n"
	
	chosen_region = gce_regions[input(region_option)]

	#type number of instances required
	instance_number = input("Please type number of instances: \n")

	flavor_choice = input("Please, select VM class: \n0) Regular \n 1) Preemtible\n")

	#selects machine types for Google Cloud
	flag_for_preempt = False
	flavor_options = "Please, select machine type: (0-"+str(len(gce_machine_types)-1)+")\n"
	for machine in gce_machine_types:

		if flavor_choice == 1:
			flag_for_preempt = True
			flavor_options += str(gce_machine_types.index(machine))+") "+machine+""+gce_preemtible+"\n"
		else:
			flavor_options += str(gce_machine_types.index(machine))+") "+machine+"\n"

	if flag_for_preempt:
		chosen_flavor =gce_machine_types[input(flavor_options)]+""+gce_preemtible
	else:
		chosen_flavor =gce_machine_types[input(flavor_options)]


	#selects operating systems types for AWS
	gce_os_options = "Please, select OS: (0-"+str(len(gce_OS)-1)+")\n"

	for os in gce_OS:

		gce_os_options += str(gce_OS.index(os))+") "+os+"\n"
	
	chosen_os =gce_OS[input(gce_os_options)]
	
	storage_size = input("Please, enter storage size: ")

	#config = json.loads(open("Google pricelist.json").read())
	#machine_types = config['gcp_price_list']['N1-HIGHMEM-4-PREEMPTIBLE']['europe']
	estimated_cost = gce_price(instance_number, chosen_region, chosen_flavor, storage_size, chosen_os)

	print estimated_cost, chosen_region, chosen_flavor, chosen_os
		





