from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_cors import CORS
import os, sys, json, requests, subprocess, platform
import datetime
from models import *
from activation import *
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

safeBoot = True
if 'safeBoot' in os.environ:
    try:
        safeBoot = bool(int(os.environ['safeBoot']))
    except:
        print("BOOT ENCOUNTERED AN ERROR: safeBoot environment variable is not set to a valid value. Please set it to 1 or 0.")
        print("Having safeBoot env variable is optional in the .env file. Safe boot is enabled in main.py by default.")

bootDirectory = os.getcwd()

validAuthTokens = {}
if not os.path.isfile('authTokens.txt'):
    with open('authTokens.txt', 'w') as f:
        f.write("{}")
else:
    with open('authTokens.txt', 'r') as f:
        validAuthTokens = json.load(f)

if not os.path.exists('supportFiles/sshCode.md'):
    with open('supportFiles/sshCode.md', 'w') as f:
        f.write("""
        # SSH Code
        ```bash
        ssh aws_cam@DL-IP-ADDRESS

        Pass: DL-PASSWORD
        ```
        """)

def expireAuthTokens():
    global validAuthTokens
    for timeCreated in list(validAuthTokens):
        timeCreatedDateObj = datetime.datetime.strptime(timeCreated, '%Y-%m-%d %H:%M:%S.%f')
        if (datetime.datetime.now() - timeCreatedDateObj).total_seconds() > 86400:
            del validAuthTokens[timeCreated]
            json.dump(validAuthTokens, open('authTokens.txt', 'w'))
            
@app.before_request
def beforeRequest():
    # If a non-API request is being made, force-reset the working directory to the boot directory
    if not request.path.startswith("/api"):
        print("Non-API request.")
        if os.getcwd() != bootDirectory:
            print("Forcing working directory to boot directory...")
            Logger.log("OSCHDIR: Forcing working directory to boot directory to maintain system integrity...")
            os.chdir(bootDirectory)
        else:
            print("Working directory is already set to boot directory.")

@app.route('/')
def index():
    return fileContent('index.html')

@app.route('/about')
def about():
    return fileContent('about.md', mdConverterEnabled=True)

@app.route('/passwordCheck', methods=['POST'])
def passwordAuth():
    for reqHeader in ['DLAccessCode', 'Content-Type']:
        if reqHeader not in request.headers:
            return "ERROR: {} header is not set.".format(reqHeader), 400
    if request.headers['DLAccessCode'] != os.environ['DLAccessCode']:
        return "ERROR: Access code is incorrect.", 401
    elif request.headers['Content-Type'] != 'application/json':
        return "ERROR: Content-Type is not set to application/json.", 400
    if 'data' not in request.json:
        return "ERROR: data field not present.", 400
    if 'password' not in request.json['data']:
        return "ERROR: password field not present.", 400
    if request.json['data']['password'] != os.environ['deepLensPwd']:
        return "ERROR: Password is incorrect.", 401

    newToken = generateAuthToken()
    validAuthTokens[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")] = newToken
    json.dump(validAuthTokens, open('authTokens.txt', 'w'))
    return "SUCCESS: Auth token is {}".format(newToken), 200

from session import *

from api import *

from assets import *

if __name__ == "__main__":
    # Check activation
    activationCheck = checkForActivation()
    if activationCheck == True:
        print("DL Manager is activated!")
    elif activationCheck == False:
        print("MAIN: This copy of DeepLens Manager is not activated! Triggering copy activation now...")
        print()
        version = None
        if not os.path.isfile(os.path.join(os.getcwd(), 'version.txt')):
            print("MAIN: Could not find version.txt file.")
            version = input("Please enter the version of DeepLens Manager that you are using: ")
            print()
        else:
            version = open('version.txt', 'r').read()
        try:
            initActivation("ejoap9y0", version)
        except Exception as e:
            print("MAIN: Failed to activate this copy of DLM. Error: {}".format(e))
            print("Aborting boot...")
            sys.exit(1)
    else:
        print("MAIN: This copy's license key needs to be re-verified. Triggering license key verification request...")
        print()
        version = None
        if not os.path.isfile(os.path.join(os.getcwd(), 'version.txt')):
            print("MAIN: Could not find version.txt file.")
            version = input("Please enter the version of DeepLens Manager that you are using: ")
            print()
        else:
            version = open('version.txt', 'r').read()
        try:
            makeKVR("ejoap9y0", version)
        except Exception as e:
            print("MAIN: Failed to verify this copy's license key. Error: {}".format(e))
            print("Aborting boot...")
            sys.exit(1)


    if safeBoot:
        print("Safe booting...")
        safeBootProcess()
        print()
    try:
        app.run(host='0.0.0.0', port=int(os.environ['RuntimePort']))
    except:
        print("ERROR ENCOUNTERED: Unable to start the server. Try booting in safe mode.")