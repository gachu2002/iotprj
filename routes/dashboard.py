from flask import Blueprint, Flask, render_template, jsonify, redirect, request, flash
import json, database, base64
from random import choice
from datetime import datetime
import person
import os, binascii

dashboard_blueprint = Blueprint('dashboard', __name__)


#this link is for the main dashboard of the website
@dashboard_blueprint.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='HOME - Landing Page')

#this links is for device 1 
@dashboard_blueprint.route('/devices/<string:username>/<string:session>', methods=["GET", "POST"])
def Dashoboard(username, session):
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username" : username,
            "image":"/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session" : session
        }

        devices = [
            {"Dashboard" : "device1",
            "deviceID": "Device1"
            }
        ]
        return render_template('device_dashboard.html', title='Dashoboard', user=user, devices=devices)
    
    else:
        return redirect('/login')



@dashboard_blueprint.route('/overview/<string:username>/<string:session>', methods=['GET', 'POST'])
def overview(username, session):
    
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username" : username,
            "image":"/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session" : session
        }

        devices = [
            {"Dashboard" : "device1",
            "deviceID": "Device1"
            }
        ]
        return render_template('overview.html', title='Overview', user=user, devices=devices)
    
    else:
        return redirect('/login')
        
#this location will get to the api setting
@dashboard_blueprint.route('/apisettings/<string:username>/<string:session>', methods=['GET', 'POST'])
def apisettings(username, session):
    
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        user = {
            "username" : username,
            "image":"/static/images/amanSingh.jpg",
            "api": logged_in[username]["object"].api,
            "session" : session
        }

        devices = [
            {"Dashboard" : "device1",
            "deviceID": "Device1"
            }
        ]
        return render_template('api_settings.html', title='API-Settings', user=user, devices=devices)
    
    else:
        return redirect('/login')


#this part is for the profile view
@dashboard_blueprint.route('/profile/<string:username>/<string:session>', methods=['GET', 'POST'])
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

        devices = [
            {"Dashboard" : "device1",
            "deviceID": "device1"
            }
        ]
        return render_template('profile.html', title='API-Settings', user=user, devices=devices)
    
    else:
        return redirect('/login')