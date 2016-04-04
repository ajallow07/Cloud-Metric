from flask import Flask,request, render_template, jsonify
from bson.json_util import dumps
import config
import json
from config import DATABASE as db, NODE_COLLECTION as nc

app = Flask(__name__)

@app.route('/')
def home():
    nodes = nc.count()
    return render_template('home.html', vm = nodes)

@app.route('/cost')
def cost():
    return render_template('getCost.html')

@app.route('/showInstanceDetails')
def showInstanceDetails():
    for machine in nc.find({},{'_id':False}):
        return jsonify(machine)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
