from flask import Blueprint, Flask, render_template, jsonify, redirect, request, flash
import json, database, base64
from random import choice
from datetime import datetime
import person
import os, binascii

api_blueprint = Blueprint('api', __name__)

#get all the devices information from the user
@api_blueprint.route("/api/<string:apikey>/listdevices", methods=['GET', 'POST'])
def listdevices(apikey):
    global api_loggers
    global mydb
    if not(apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = person.user(username, "dummy")
            apiuser.authenticated = True
            devices_list = apiuser.get_devices()
            api_loggers[apikey] = {"object" : apiuser}
            return jsonify(devices_list)
        except Exception as e:
            print (e)
            return jsonify({"data":"Oops Looks like api is not correct"})
    
    else:
        data = api_loggers[apikey]["object"].get_devices()
        return jsonify (data)

randlist = [i for i in range(0, 100)]

@api_blueprint.route('/api/<string:apikey>/deviceinfo/<string:deviceID>', methods=['GET', 'POST'])
def device_info (apikey, deviceID):
    global api_loggers
    global mydb
    if not(apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = person.user(username, "dummy")
            apiuser.authenticated = True
            data = apiuser.dev_info(deviceID)
            api_loggers[apikey] = {"object" : apiuser}
            #this part is hard coded so remove after fixing the issue
            data = list(data)
            data[2] = "Rosegarden"
            return jsonify(data)
        except Exception as e:
            print (e)
            return jsonify({"data":"Oops Looks like api is not correct"})
    
    else:
        data = api_loggers[apikey]["object"].dev_info(deviceID)

        #this part is hard coded so remove after fixing the issue
        data = list(data)
        data[2] = "Rosegarden"
        return jsonify (data)

@api_blueprint.route('/api/<string:apikey>/fieldstat/<string:fieldname>', methods=['GET', 'POST'])
def fieldstat (apikey, fieldname):
    
    global api_loggers
    global mydb
    if not(apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = person.user(username, "dummy")
            apiuser.authenticated = True
            data = apiuser.field_values(fieldname)
            api_loggers[apikey] = {"object" : apiuser}
            return jsonify(data)
        except Exception as e:
            print (e)
            return jsonify({"data":"Oops Looks like api is not correct"})
    
    else:
        data = api_loggers[apikey]["object"].field_values(fieldname)
        return jsonify (data)


@api_blueprint.route('/api/<string:apikey>/devicestat/<string:fieldname>/<string:deviceID>', methods=['GET', 'POST'])
def devicestat (apikey, fieldname, deviceID):
    
    global api_loggers
    global mydb
    if not(apikey in api_loggers):
        try:
            query = "select username from users where api_key = '{}'".format(apikey)
            mydb.cursor.execute(query)
            username = mydb.cursor.fetchall()
            username = username[0][0]
            apiuser = person.user(username, "dummy")
            apiuser.authenticated = True
            data = apiuser.device_values(fieldname, deviceID)
            api_loggers[apikey] = {"object" : apiuser}
            return jsonify(data)
        except Exception as e:
            print (e)
            return jsonify({"data":"Oops Looks like api is not correct"})
    
    else:
        data = api_loggers[apikey]["object"].device_values(fieldname, deviceID)
        return jsonify (data)

@api_blueprint.route('/api/<string:apikey>/update/<string:data>', methods=['GET','POST'])
def update_values(apikey, data):
    global mydb
    try:
        data = decode(data)
        output = mydb.get_apikeys()
        if apikey in output:
            if (len(data) == 6) and (type(data) is list):
                fieldname = data[0]
                deviceID = data[1]
                temp = data[2]
                humidity = data[3]
                moisture = data[4]
                light = data[5]
                mydb.update_values(apikey, fieldname, deviceID, temp, humidity, moisture, light)
                return ("Values Updated")
            else:
                return "Data Decoding Error!"
        else:
            return "Api key invalid"

    except Exception as e:
        print (e)
        return jsonify({"data":"Oops Looks like api is not correct"})


@api_blueprint.route("/api/<string:apikey>/temperature", methods=["GET", "POST"])
def get_temperature(apikey):
    
    randData = choice(randlist)
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    response = [time, randData]
    return jsonify(response)

@api_blueprint.route("/api/<string:apikey>/moisture", methods=["GET", "POST"])
def get_moisture(apikey):
    
    randData = choice(randlist)
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    response = [time, randData]
    return jsonify(response)

@api_blueprint.route("/api/<string:apikey>/humidity", methods=["GET", "POST"])
def get_humidity(apikey):
    
    randData = choice(randlist)
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    response = [time, randData]
    return jsonify(response)

@api_blueprint.route("/api/<string:apikey>/light", methods=["GET", "POST"])
def get_light(apikey):
    
    randData = choice(randlist)
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    response = [time, randData]
    return jsonify(response)

def encode(data):
    data = json.dumps(data)
    message_bytes = data.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

def decode(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    return json.loads(message)