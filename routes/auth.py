from flask import Blueprint, Flask, render_template, jsonify, redirect, request, flash
import json, database, base64
from random import choice
from datetime import datetime
import person
import os, binascii


auth_blueprint = Blueprint('auth', __name__)

logged_in = {}
api_loggers = {}
mydb = database.db('root', 'Localhost', 'Love123bgbg@', 'ARMS')

@auth_blueprint.route("/login", methods=['GET', 'POST'])
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
       
    return render_template('Login.html', error=error)

@auth_blueprint.route("/register", methods=['GET', 'POST'])
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

    return render_template('register.html', error=error)   

@auth_blueprint.route('/logout/<string:username>/<string:session>', methods=['GET', 'POST'])
def logout(username, session):
    
    global logged_in

    if username in logged_in and (logged_in[username]['object'].session_id == session):
        logged_in.pop(username)
        # print("logged out")
        return redirect('/')
    else:
        return redirect('/login')

