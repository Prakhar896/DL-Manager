from main import *

@app.route('/session/<authToken>/home')
def configHome(authToken):
    expireAuthTokens()
    check = checkAuthTokenValidity(authToken, validAuthTokens)
    if check == True:
        ## Generate required information
        # ssid = ""
        # if platform.system() == "Darwin":
        #     ## Get current SSID
        #     ssid = subprocess.check_output(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'])
        #     ssid = ssid.decode('utf-8').split('\n')[12]
        #     ssid = ssid[len('           SSID: ')::]
        # elif platform.system() == "Linux":
        #     ## Get current SSID
        #     ssid = subprocess.check_output(['iwgetid', '-r'])
        #     ssid = ssid.decode('utf-8').split('\n')[0]
        
        return render_template(
            'home.html', 
            loggedInUser=zshCommandOutput('whoami'), 
            homeRuntimeData={
                # 'ssid': ssid,
                'uptime': zshCommandOutput('uptime'),
                "port": os.environ['RuntimePort']
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

@app.route('/session/<authToken>/zsh')
def zsh(authToken):
    expireAuthTokens()
    check = checkAuthTokenValidity(authToken, validAuthTokens)
    if check == True:
        return render_template('zsh.html', cwd=zshCommandOutput('pwd'), loggedInUser=zshCommandOutput('whoami'))
    else:
        return check

@app.route('/session/<authToken>/sessionAdmin/logout')
def logout(authToken):
    expireAuthTokens()
    check = checkAuthTokenValidity(authToken, validAuthTokens)
    if check == True:
        for tokenKey in validAuthTokens:
            if validAuthTokens[tokenKey] == authToken:
                del validAuthTokens[tokenKey]
                json.dump(validAuthTokens, open('authTokens.txt', 'w'))
                
                if os.getcwd() != bootDirectory:
                    print("SESSIONLOGOUT: Forcing working directory to boot directory...")
                    Logger.log("OSCHDIR: Forcing working directory to boot directory to maintain system integrity...")
                    os.chdir(bootDirectory)
                
                return render_template('logout.html', currentUser=zshCommandOutput('whoami'))
    else:
        return check