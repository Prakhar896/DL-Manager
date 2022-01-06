from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_cors import CORS
import os, sys, json, requests, subprocess
import datetime
from models import *
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

@app.route('/session/<authToken>/home')
def configHome(authToken):
    expireAuthTokens()
    check = checkAuthTokenValidity(authToken, validAuthTokens)
    if check == True:
        ## Generate required information
        ssid = ""
        if platform.system() == "Darwin":
            ## Get current SSID
            ssid = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'])
            ssid = ssid.decode('utf-8').split('\n')[12]
            ssid = ssid[len('           SSID: ')::]
        elif platform.system() == "Linux":
            ## Get current SSID
            ssid = subprocess.check_output(['iwgetid', '-r'])
            ssid = ssid.decode('utf-8').split('\n')[0]
        
        return render_template(
            'home.html', 
            loggedInUser=zshCommandOutput('whoami'), 
            homeRuntimeData={
                'ssid': ssid,
                'uptime': zshCommandOutput('uptime')
            })
    else:
        return check

@app.route('/session/<authToken>/home/extras/ssh')
def sshCode(authToken):
    expireAuthTokens()
    check = checkAuthTokenValidity(authToken, validAuthTokens)
    if check == True:
        return fileContent('supportFiles/sshCode.md', True)
    else:
        return check

from assets import *

if __name__ == "__main__":
    if safeBoot:
        print("Safe booting...")
        safeBootProcess()
        print()
    try:
        app.run(host='0.0.0.0', port=8890)
    except:
        print("ERROR ENCOUNTERED: Unable to start the server. Try booting in safe mode.")