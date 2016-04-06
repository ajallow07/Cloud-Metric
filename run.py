from flask import Flask,request, render_template, jsonify
import config
import json
from config import DATABASE as db, NODE_COLLECTION as nc

app = Flask(__name__)


@app.route('/')
def home():
    nodes = nc.count()

    return render_template('home.html', vm = nodes)

@app.route('/awscost')
def awscost():
    return render_template('getAWSCost.html')

@app.route('/gcecost')
def gcecost():
    return render_template('getGCCost.html')

@app.route('/nodes')
def nodes():
    machineList= [machine for machine in nc.find({},{'_id':False})]
    #my_keys = ['node','os','cpu', 'memory', 'disk']
    return render_template('nodes.html', data=machineList)

    """
    for machine in nc.find({},{'_id':False}):
        machineList.append(machine)
    return render_template('nodes.html', data = machineList)


    with open('machines.json', 'w') as output:
        machienList =json.dump([machine for machine in nc.find({},{'_id':False})], output)
        #output.write(data)

    """
    #return  page




if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
