from flask import Flask, render_template, jsonify, redirect, request, flash
import json, database, base64
from random import choice
from datetime import datetime
import person
import os, binascii
from flask_mqtt import Mqtt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'gfgfgghghgfhgfhgfhgfhfgghghghghghg'
app.config["TEMPLATES_AUTO_RELOAD"] = True
logged_in = {}
api_loggers = {}
mydb = database.db('root', 'Localhost', 'Love123bgbg@', 'ARMS')

app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 0.5
mqtt = Mqtt(app)
#test api key aGFja2luZ2lzYWNyaW1lYXNmc2FmZnNhZnNhZmZzYQ==
# ROUTING FOR TEMPALTE
#this link is for the main dashboard of the website
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='HOME - Landing Page')

#register
@app.route("/register", methods=['GET', 'POST'])
def register():
    error = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            error = "Username and password are required."
        else:
            new_user = person.user(username, password)
            api_key = str(binascii.b2a_hex(os.urandom(15)));
            try:
                result = new_user.db.add_user(
                    username,
                    password,
                    "",  
                    "",
                    "",
                    "",
                    api_key  
                )
                if result == "success":
                    new_user.authenticated = True
                    flash("Registration successful! Please log in.", "success")
                    return redirect('/login')
                else:
                    flash("Error registering user.", "error")
            except Exception as e:
                flash(f"Error: {str(e)}", "error")

    return render_template('authentication/register.html', error=error)   

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST': 
        
        user = person.user(request.form['username'], request.form['password'])
        if user.authenticated:
            user.session_id = str(binascii.b2a_hex(os.urandom(15)))
            logged_in[user.username] = {"object": user}
            return redirect('/overview/{}/{}'.format(request.form['username'], user.session_id))
        else:
            error = "invalid Username or Passowrd"
       
    return render_template('authentication/Login.html', error=error)

# MQTT message handling function
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    mqtt.subscribe('device')
    
@mqtt.on_message()
def handle_message(client, userdata, message):
    data = json.loads(message.payload)
    for username in logged_in:
        print(username)
        if(data.get('deviceType') == "sensor"):
            deviceID = data.get('deviceId')
            device_type = data.get('deviceType')
            device_value = f"{data.get('temp')} {data.get('humid')}"
        else:
            deviceID = data.get('deviceId')
            device_type = data.get('deviceType')
            device_value = data.get('deviceValue')
        # Add or update the device in the database
        result = mydb.add_device(username, deviceID, device_type, device_value)
        print(result)
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    
    
@app.route('/overview/<string:username>/<string:session>', methods=['GET', 'POST'])
def overview(username, session):
    
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username" : username,
            "image":"/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session" : session
        }
        return render_template('dashboard/overview.html', title='Overview', user=user)
    
    else:
        return redirect('/login')
        
#this location will get to the api setting
@app.route('/apisettings/<string:username>/<string:session>', methods=['GET', 'POST'])
def apisettings(username, session):
    
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username" : username,
            "image":"/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session" : session
        }
        return render_template('dashboard/api_settings.html', title='API-Settings', user=user)
    
    else:
        return redirect('/login')


#this part is for the profile view
@app.route('/profile/<string:username>/<string:session>', methods=['GET', 'POST'])
def profile(username, session):
    
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username" : username,
            "image":"/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session" : session,
            "firstname": logged_in[username]["object"].first,
            "lastname": logged_in[username]["object"].last,
            "email":logged_in[username]["object"].email,
            "phone":logged_in[username]["object"].phone,
            "lastlogin":logged_in[username]["object"].last_login,
        }

        return render_template('dashboard/profile.html', title='API-Settings', user=user)
    
    else:
        return redirect('/login')


@app.route('/logout/<string:username>/<string:session>', methods=['GET', 'POST'])
def logout(username, session):
    
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        logged_in.pop(username)
        # print("logged out")
        return redirect('/')
    else:
        return redirect('/login')


#this links is for devices
@app.route('/devices/<string:username>/<string:session>', methods=["GET", "POST"])
def Dashboard(username, session):
    global logged_in
    
    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username" : username,
            "image":"/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session" : session
        }

        devices = logged_in[username]["object"].get_devices()
        sensor_count = 0
        led_count = 0

        # Iterate over the devices and count the types.
        for device in devices:
            if device['device_type'].lower() == 'sensor':
                sensor_count += 1
            elif device['device_type'].lower()  == 'led':
                led_count += 1
        return render_template('dashboard/device_dashboard.html', title='Device', user=user, devices=devices, sensor_count=sensor_count, led_count=led_count)
    
    else:
        return redirect('/login')

@app.route('/devices/<string:deviceID>/info/<string:username>/<string:session>')
def get_device_info(username, session, deviceID):
    global logged_in
    
    if username in logged_in and (logged_in[username]['object'].session_id == session):
        device = logged_in[username]["object"].get_device_by_id(deviceID)
        return ""
    else:
        return redirect('/login')

@app.route('/devices/add/<string:username>/<string:session>',methods = ["GET"])
def see_unabled_device(username, session):
    global logged_in
    
    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username" : username,
            "image":"/static/images/amanSingh.jpg", 
            "api": logged_in[username]["object"].api,
            "session" : session
        }
        addable_devices = logged_in[username]["object"].get_addable_device()
        return render_template('dashboard/add_device.html', title='Device Add', addable_devices = addable_devices, user = user)
    else:
        return redirect('/login')

@app.route('/devices/<string:deviceID>/add/<string:username>/<string:session>',methods = ["POST"])
def add_unabled_device(username, session):
    global logged_in
    
    if username in logged_in and (logged_in[username]['object'].session_id == session):
        deviceID = request.form['deviceID']
        logged_in[username]["object"].enable_device(deviceID)
        return redirect('/devices/<string:username>/<string:session>')
    else:
        return redirect('/login')
    
@app.route('/devices/<string:deviceID>/edit/<string:username>/<string:session>',methods = ["PUT"])
def edit_device_info(username, session, deviceID):
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        device = logged_in[username]["object"].update_device_info(deviceID)
        return jsonify(device)
    else:
        return redirect('/login')
    
@app.route('/devices/<string:deviceID>/delete/<string:username>/<string:session>', methods = ["DELETE"])
def delete_device(username, session, deviceID):
    global logged_in
    
    if username in logged_in and (logged_in[username]['object'].session_id == session):
        device = logged_in[username]["object"].disable_device(deviceID)
        return ""
    else:
        return redirect('/login')

    
# #this is the testing for api 
# @app.route("/api/<string:apikey>/test", methods=["GET", "POST"])
# def apitest (apikey):
#     return {"data":"working Fine Connected to the api server"}


#get all the devices information from the usser
# @app.route("/api/<string:apikey>/listdevices", methods=['GET', 'POST'])
# def listdevices(apikey):
#     global api_loggers
#     global mydb
#     if not(apikey in api_loggers):
#         try:
#             query = "select username from users where api_key = '{}'".format(apikey)
#             mydb.cursor.execute(query)
#             username = mydb.cursor.fetchall()
#             username = username[0][0]
#             apiuser = person.user(username, "dummy")
#             apiuser.authenticated = True
#             devices_list = apiuser.get_devices()
#             api_loggers[apikey] = {"object" : apiuser}
#             return jsonify(devices_list)
#         except Exception as e:
#             print (e)
#             return jsonify({"data":"Oops Looks like api is not correct"})
    
#     else:
#         data = api_loggers[apikey]["object"].get_devices()
#         return jsonify (data)

# randlist = [i for i in range(0, 100)]

# @app.route('/api/<string:apikey>/deviceinfo/<string:deviceID>', methods=['GET', 'POST'])
# def device_info (apikey, deviceID):
#     global api_loggers
#     global mydb
#     if not(apikey in api_loggers):
#         try:
#             query = "select username from users where api_key = '{}'".format(apikey)
#             mydb.cursor.execute(query)
#             username = mydb.cursor.fetchall()
#             username = username[0][0]
#             apiuser = person.user(username, "dummy")
#             apiuser.authenticated = True
#             data = apiuser.dev_info(deviceID)
#             api_loggers[apikey] = {"object" : apiuser}
#             #this part is hard coded so remove after fixing the issue
#             data = list(data)
#             return jsonify(data)
#         except Exception as e:
#             print (e)
#             return jsonify({"data":"Oops Looks like api is not correct"})
    
#     else:
#         data = api_loggers[apikey]["object"].dev_info(deviceID)

#         data = list(data)
#         return jsonify (data)

# @app.route('/api/<string:apikey>/fieldstat/<string:fieldname>', methods=['GET', 'POST'])
# def fieldstat (apikey, fieldname):
    
#     global api_loggers
#     global mydb
#     if not(apikey in api_loggers):
#         try:
#             query = "select username from users where api_key = '{}'".format(apikey)
#             mydb.cursor.execute(query)
#             username = mydb.cursor.fetchall()
#             username = username[0][0]
#             apiuser = person.user(username, "dummy")
#             apiuser.authenticated = True
#             data = apiuser.field_values(fieldname)
#             api_loggers[apikey] = {"object" : apiuser}
#             return jsonify(data)
#         except Exception as e:
#             print (e)
#             return jsonify({"data":"Oops Looks like api is not correct"})
    
#     else:
#         data = api_loggers[apikey]["object"].field_values(fieldname)
#         return jsonify (data)


# @app.route('/api/<string:apikey>/devicestat/<string:fieldname>/<string:deviceID>', methods=['GET', 'POST'])
# def devicestat (apikey, fieldname, deviceID):
    
#     global api_loggers
#     global mydb
#     if not(apikey in api_loggers):
#         try:
#             query = "select username from users where api_key = '{}'".format(apikey)
#             mydb.cursor.execute(query)
#             username = mydb.cursor.fetchall()
#             username = username[0][0]
#             apiuser = person.user(username, "dummy")
#             apiuser.authenticated = True
#             data = apiuser.device_values(fieldname, deviceID)
#             api_loggers[apikey] = {"object" : apiuser}
#             return jsonify(data)
#         except Exception as e:
#             print (e)
#             return jsonify({"data":"Oops Looks like api is not correct"})
    
#     else:
#         data = api_loggers[apikey]["object"].device_values(fieldname, deviceID)
#         return jsonify (data)

# @app.route('/api/<string:apikey>/update/<string:data>', methods=['GET','POST'])
# def update_values(apikey, data):
#     global mydb
#     try:
#         data = decode(data)
#         output = mydb.get_apikeys()
#         if apikey in output:
#             if (len(data) == 6) and (type(data) is list):
#                 fieldname = data[0]
#                 deviceID = data[1]
#                 temp = data[2]
#                 humidity = data[3]
#                 moisture = data[4]
#                 light = data[5]
#                 mydb.update_values(apikey, fieldname, deviceID, temp, humidity, moisture, light)
#                 return ("Values Updated")
#             else:
#                 return "Data Decoding Error!"
#         else:
#             return "Api key invalid"

#     except Exception as e:
#         print (e)
#         return jsonify({"data":"Oops Looks like api is not correct"})


# @app.route("/api/<string:apikey>/temperature", methods=["GET", "POST"])
# def get_temperature(apikey):
    
#     randData = choice(randlist)
#     time = datetime.now()
#     time = time.strftime("%H:%M:%S")
#     response = [time, randData]
#     return jsonify(response)

# @app.route("/api/<string:apikey>/moisture", methods=["GET", "POST"])
# def get_moisture(apikey):
    
#     randData = choice(randlist)
#     time = datetime.now()
#     time = time.strftime("%H:%M:%S")
#     response = [time, randData]
#     return jsonify(response)

# @app.route("/api/<string:apikey>/humidity", methods=["GET", "POST"])
# def get_humidity(apikey):
    
#     randData = choice(randlist)
#     time = datetime.now()
#     time = time.strftime("%H:%M:%S")
#     response = [time, randData]
#     return jsonify(response)

# @app.route("/api/<string:apikey>/light", methods=["GET", "POST"])
# def get_light(apikey):
    
#     randData = choice(randlist)
#     time = datetime.now()
#     time = time.strftime("%H:%M:%S")
#     response = [time, randData]
#     return jsonify(response)


# def encode(data):
#     data = json.dumps(data)
#     message_bytes = data.encode('ascii')
#     base64_bytes = base64.b64encode(message_bytes)
#     base64_message = base64_bytes.decode('ascii')
#     return base64_message

# def decode(base64_message):
#     base64_bytes = base64_message.encode('ascii')
#     message_bytes = base64.b64decode(base64_bytes)
#     message = message_bytes.decode('ascii')
#     return json.loads(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = "80", debug=True)