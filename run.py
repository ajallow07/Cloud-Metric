from flask import Flask,request, render_template, jsonify
import config
import json
from config import DATABASE as db, NODE_COLLECTION as nc

app = Flask(__name__)

@app.route('/')
def home():
    nodes = nc.count()
    with open('machines.json', 'w') as output:
        data = json.dumps([machine for machine in nc.find({},{'_id':False})])
        output.write(data)
        output.close()

    return render_template('home.html', vm = nodes)

@app.route('/cost')
def cost():
    return render_template('getCost.html')

@app.route('/showInstanceDetails')
def showInstanceDetails():
    #for machine in nc.find({},{'_id':False}):
    return jsonify(machines=[machine for machine in nc.find({},{'_id':False})])

if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
