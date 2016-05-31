#! /usr/bin/env python

from flask import Flask,request, render_template, jsonify, session
import config, os, math, json, datetime, optimizer
from mapping import getMatchingInstances, AWS_FLAVORS, GC_FLAVORS
from computeCost import gce_price, aws_storage_prices, read_EC2_ondemand_instance_prices
from config import NODE_COLLECTION as nc, REPORT_COLLECTION as rc, CLUSTER_COLLECTION as cc
from jinja2 import Environment, FileSystemLoader
from math import ceil
from bson import json_util
from bson.json_util import dumps
from optimizer import get_nodes_in_cluster, get_matching_instance_with_PD_OS, get_cost_of_recommended_instances_on_AWS, get_cost_of_recommended_instances_on_GCP
from operator import itemgetter, attrgetter


app = Flask(__name__)

app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
# Define the template directory
#tpldir = os.path.dirname(os.path.abspath(__file__))+'/templates/'
# Setup the template enviroment
#env = Environment(loader=FileSystemLoader(tpldir), trim_blocks=True)
#FIELDS = {'node': True, 'dt': True, 'disk': True, 'memory': True, 'cpu': True, '_id': False}



@app.route('/show_costs/<machine>')
def show_costs(machine):

    if not machine:

        return render_template("costs.html", machine=None, awsregions= '', gcpregions='', data='');

    regionCostAWS = []
    regionCostGCP = []
    awsregions = [
    "us-east-1",
    "us-west-1",
    "us-west-2",
    "eu-west-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-northeast-1",
    "sa-east-1",
    "eu-central-1",
    "us-gov-west-1"
    ]
    gcpregions = ['us', 'europe', 'asia']
    specs = [node for node in nc.find({"node":machine},{'_id': False})]
    flavorAWS = getMatchingInstances(AWS_FLAVORS, specs[0]['cpu'], ceil(float(specs[0]['memory'])))
    flavorGCP = getMatchingInstances(GC_FLAVORS, specs[0]['cpu'], ceil(float(specs[0]['memory'])))

    for dataCenter in awsregions:
        instanceCost = read_EC2_ondemand_instance_prices(1, dataCenter, flavorAWS[0]['name'], specs[0]['os'].lower())
        storageCost = aws_storage_prices(dataCenter, ceil(float(specs[0]['disk'])))

        monthlyCost = instanceCost + storageCost
        #dic.(dataCenter, monthlyCost)
        if instanceCost > 0:
            regionCostAWS.append((dataCenter, monthlyCost))

    sortedRegionCostOnAWS = sorted(regionCostAWS, key= itemgetter(1))

    for dataCenter in gcpregions:
        instanceCost = gce_price(1,"regular", dataCenter, flavorGCP[0]['name'], ceil(float(specs[0]['disk'])), specs[0]['os'])
        if instanceCost > 0:
            regionCostGCP.append((dataCenter, instanceCost))

    sortedRegionCostOnGCP = sorted(regionCostGCP, key= itemgetter(1))

    return render_template("costs.html", machine=machine, awsregions= sortedRegionCostOnAWS, gcpregions=sortedRegionCostOnGCP);


#monitoring aspect
@app.route('/show_charts/<machine>')
def show_charts(machine, chartID='chart_ID', chart_type='spline', chart_height=500, zoom_type='x'):
    FILTER = {'node': machine}
    if rc.find(FILTER).count() < 600:
        data_cursor = rc.find(FILTER)
    else:
        data_cursor = rc.find(FILTER).skip(rc.find(FILTER).count() - 600)

    cpu_user = []
    mem_per = []
    disk_usage = []
    json_data = []
    for data in data_cursor:
        #json_data.append(data)
        #if data['node'] == machine:
        date = data['dt']
        date_str = date.strftime('%b %d, %H:%M')
        disk_usage.append([date_str, data['disk']])
        mem_per.append([date_str, data['memory']])
        cpu_user.append([date_str, data['cpu']['user']])

        #json_cpu.append(cpu_user)
       #json_data = json.dumps(cpu_user, default=json_util.default)
    text_title = "Resource Monitring metrics: "+str(machine)
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": zoom_type}
    credits = {}
    if cpu_user:
        series = [
            {"name": 'cpu',
            "type": 'spline',
            "data": cpu_user
            }, {
                "name" : 'memory',
                "type": 'spline',
                "data" :  mem_per
            },
            {
                "name": 'disk',
                "type": 'spline',
                "data": disk_usage
            }
        ]
        title = {"text": text_title}
        xAxis = {"type": 'datetime',
            "categories": [cpu_user[0][0]],
            "tickInterval": 50
        }
        yAxis = {
            "title": {"text": 'Usage %'},
            "ceiling": 100,
            "floor": 0
            }

        return render_template('graphs.html', chartID=chartID, chart= chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

    return render_template('graphs.html', chartID=chartID, chart= chart, series=[], title="Resource Monitoring", xAxis={}, yAxis={})



@app.route('/')
def home():

    cNames = []
    clusterCount = cc.count()
    if clusterCount > 0:

        cNames = [cluster['name'] for cluster in cc.find({},{'_id':0, 'name':1})]
        if not session.has_key('cluster'):
            session['cluster'] = cNames[0]
    return render_template('home.html', clusterNumber=clusterCount, clusterNames=cNames, session=session)

@app.route('/matchingAWSInstances/<machine>')
def awsInstances(machine):
    cloud = 'AWS'
    machineList = [machine for machine in nc.find({"node":machine},{'_id': False})]
    totalCost = 0

    matchingFlavor = getMatchingInstances(AWS_FLAVORS, machine['cpu'], ceil(float(machine['memory'])))
    matchingMachines = sorted(matchingFlavor)
    return render_template('matching_instances.html', data=matchingMachines, cloudProvider =cloud)


@app.route('/matchingGCPInstances/<machine>')
def gcpInstances(machine):
    cloud = 'GCP'
    machineList = [machine for machine in nc.find({"node":machine},{'_id': False})]

    matchingFlavor = getMatchingInstances(GC_FLAVORS, machine['cpu'], ceil(float(machine['memory'])))
    matchingMachines = sorted(matchingFlavor)
    return render_template('matching_instances.html', data=matchingMachines, cloudProvider=cloud)

@app.route('/nodes/<cluster>')
def nodes(cluster):
    session['cluster'] = cluster
    machineList = [machine for machine in nc.find({"cluster_id":cluster},{'_id':False})]
    #my_keys = ['node','os','cpu', 'memory', 'disk']
    computedAWSCost = []
    computedGCPCost = []
    totalAWSCost = 0
    totalGCPCost = 0
    for machine in machineList:
        #get GCP costs
        flavorGCP= getMatchingInstances(GC_FLAVORS, machine['cpu'], ceil(float(machine['memory'])))
        instanceCostGCP = gce_price(1,"regular", "us", flavorGCP[0]['name'], ceil(float(machine['disk'])), machine['os'])
        totalGCPCost += instanceCostGCP
        computedGCPCost.append(instanceCostGCP)

        #get aws costs
        flavorAWS = getMatchingInstances(AWS_FLAVORS, machine['cpu'], ceil(float(machine['memory'])))
        instanceCostAWS = read_EC2_ondemand_instance_prices(1, "us-east-1", flavorAWS[0]['name'], machine['os'].lower())
        storageAWSCost = aws_storage_prices("us-east-1", ceil(float(machine['disk'])))
        monthlyCost = instanceCostAWS + storageAWSCost
        totalAWSCost += monthlyCost
        computedAWSCost.append(monthlyCost)

    return render_template('nodes.html', data=machineList, ceil=ceil, dataAWS=zip(machineList,computedAWSCost),
    totalAWS=totalAWSCost, totalGCP=totalGCPCost, dataGCP= zip(machineList,computedGCPCost), session=session)


@app.route('/show_cluster_charts/<cluster>')
def show_cluster_chart(cluster, chartID='chart_ID', chart_type='spline', chart_height=500, zoom_type='xy'):

    AGGR = [{ "$match": { "cluster_id": cluster }},
    {"$group" : { "_id": { "$dateToString": { "format": "%Y-%m-%d %H:00", "date": "$dt" }},
    "avgCPU": {"$avg": "$cpu.user"}, "avgMemory" :{ "$avg": "$memory"}, "avgDisk": {"$avg": "$disk"}}},
    {"$sort": {"_id": 1}}]

    data_cursor = rc.aggregate(AGGR)

    cpu_user = []
    mem_per = []
    disk_usage = []
    json_data = []
    for data in data_cursor:
        #json_data.append(data)
        #if data['node'] == machine:

        date_form = datetime.datetime.strptime(data['_id'], "%Y-%m-%d %H:%M")
        date_str = date_form.strftime('%b %d, %H:%M')
        disk_usage.append([date_str, data['avgDisk']])
        mem_per.append([date_str, data['avgMemory']])
        cpu_user.append([date_str, data['avgCPU']])

    text_title = "Resource Monitoring metrics on "+str(session['cluster'])+ " cluster"
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "zoomType": zoom_type}
    credits = {}

    if cpu_user:
        series = [
            {"name": 'cpu',
            "type": 'spline',
            "data": cpu_user
            }, {
                "name" : 'memory',
                "type": 'spline',
                "data" :  mem_per
            },
            {
                "name": 'disk',
                "type": 'spline',
                "data": disk_usage
            }
        ]
        title = {"text": text_title}
        xAxis = {"type": 'datetime',
            "categories": [cpu_user[0][0]],
            "tickInterval": 60
        }
        yAxis = {"title": {"text": 'Utilization %'},
        "ceiling": 100,
        "floor": 0
        }

        return render_template('cluster_monitor.html', chartID=chartID, chart= chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

    return render_template('cluster_monitor.html', chartID=chartID, chart=chart, series=[], title="Resource Monitoring", xAxis={}, yAxis={})

@app.route('/recommender/<cluster>')
def recommender(cluster):
    gcp_instances =[]
    aws_instances =[]
    gceCostData =[]
    totalGCPCost=0
    awsCostData =[]
    totalAWSCost=0

    nodes_in_cluster = get_nodes_in_cluster(cluster)
    if nodes_in_cluster:
        gcp_instances, aws_instances = get_matching_instance_with_PD_OS(nodes_in_cluster)

    #if not (len(nodes_in_cluster) > len(gcp_instances)):
    gceCostData, totalGCPCost = get_cost_of_recommended_instances_on_GCP(gcp_instances)

    #if not (len(nodes_in_cluster) > len(aws_instances)):
    awsCostData, totalAWSCost = get_cost_of_recommended_instances_on_AWS(aws_instances)

    return render_template('recommendation.html', aws=aws_instances,
    gcp=gcp_instances, awsData=awsCostData, gcpData=gceCostData, awstotal=totalAWSCost, gcptotal=totalGCPCost)

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
