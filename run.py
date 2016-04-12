from flask import Flask,request, render_template, jsonify
import config
import os
from mapping import getMatchingInstanceInGCE, getMatchingInstanceInAWS, AWS_FLAVORS, GC_FLAVORS
from calc import gce_price, aws_storage_prices, read_EC2_ondemand_instance_prices
import json
from config import DB_NODE as db, DB_REPORT as dr, NODE_COLLECTION as nc, REPORT_COLLECTION as rc
import math
from jinja2 import Environment, FileSystemLoader
from math import ceil
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)

# Define the template directory
#tpldir = os.path.dirname(os.path.abspath(__file__))+'/templates/'
# Setup the template enviroment
#env = Environment(loader=FileSystemLoader(tpldir), trim_blocks=True)
FIELDS = {'node': True, 'dt': True, 'disk': True, 'memory': True, 'cpu': True, '_id': False}

#monitoring aspect
@app.route('/show_charts')
def show_charts(chartID='chart_ID', chart_type='spline', chart_height=500):
    data_cursor = rc.find({'node':'Alieus-MacBook-Pro.local'})
    cpu_user = []
    mem_per = []
    disk_usage = []
    json_data =[]
    for data in data_cursor:
        #json_data.append(data)
        date = data['dt']
        date_str = date.strftime('%Y-%m-%d %H:%M')
        disk_usage.append([date_str, data['disk']])
        mem_per.append([date_str, data['memory']])
        cpu_user.append([date_str, data['cpu']['user']])

        #json_cpu.append(cpu_user)
    json_data = json.dumps(cpu_user, default=json_util.default)

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    credits = { }
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
    title = {"text": 'CPU Usage'}
    xAxis = {"type": 'datetime', "label": "datetime"}
    yAxis = {"title": {"text": 'Usage Percent'}}

    return render_template('graphs.html', chartID=chartID, chart= chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


@app.route('/charts/show_data')
def load_data():

    data_cursor = rc.find({'node':'aj-hadoop-master'})
    cpu_user = []
    mem_per = []
    disk_usage = []
    json_data =[]
    for data in data_cursor:
        #json_data.append(data)
        date = data['dt']
        date_str = date.strftime('%Y-%m-%d %H:%M')
        #disk_usage.append([date, data['disk']])
        #mem_per.append([date, data['memory']])
        cpu_user.append([date_str, data['cpu']['user']])

        #json_cpu.append(cpu_user)
        json_data = json.dumps(cpu_user, default=json_util.default)

    return json_data

@app.route('/')
def home():
    nodes = nc.count()

    return render_template('home.html', vm = nodes)

@app.route('/awscost')
def awscost():
    computedCost = []
    machineList = [machine for machine in nc.find({},{'_id': False})]

    for machine in machineList:
        flavor = getMatchingInstanceInAWS(AWS_FLAVORS, machine['cpu'], ceil(float(machine['memory'])))
        instanceCost = read_EC2_ondemand_instance_prices(1, "us-east-1", flavor[0], machine['os'].lower())
        storageCost = aws_storage_prices("us-east-1", ceil(float(machine['disk'])))
        monthlyCost = instanceCost + storageCost
        computedCost.append(monthlyCost)
    return render_template('getAWSCost.html', data=zip(machineList,computedCost))

@app.route ('/nodecost')
def nodecosts():
    return 'This show individual node cost'


@app.route('/gcecost')
def gcecost():
    computedCost = []
    machineList = [machine for machine in nc.find({},{'_id':False})]

    for machine in machineList:
        flavor = getMatchingInstanceInGCE(GC_FLAVORS, machine['cpu'], ceil(float(machine['memory'])))
        instanceCost = gce_price(1,"regular", "us", flavor[0], ceil(float(machine['disk'])), machine['os'] , 0)
        computedCost.append(instanceCost)
    return render_template('getGCCost.html', data=zip(machineList,computedCost))

@app.route('/nodes')
def nodes():
    machineList= [machine for machine in nc.find({},{'_id':False})]
    #my_keys = ['node','os','cpu', 'memory', 'disk']
    return render_template('nodes.html', data=machineList, ceil=ceil)

    #return  page
if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
