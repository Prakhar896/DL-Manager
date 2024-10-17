## File contains api routes
from main import *

@app.route('/api/zshCommand', methods=['POST'])
def zshCommand():
    for reqHeader in ['DLAccessCode', 'Content-Type']:
        if reqHeader not in request.headers:
            return "ERROR: {} header is not set.".format(reqHeader), 400
    if request.headers['DLAccessCode'] != os.environ['DLAccessCode']:
        return "ERROR: Access code is incorrect.", 401
    elif request.headers['Content-Type'] != 'application/json':
        return "ERROR: Content-Type is not set to application/json.", 400
    if 'command' not in request.json:
        return "ERROR: `command` field is not present in request JSON body.", 400
    if not isinstance(request.json["command"], str):
        return "ERROR: `command` field in request JSON body is not a string.", 400
    
    command: str = request.json["command"].strip()
    
    if command == "":
        return "ERROR: `command` field in request JSON body is empty.", 400
    
    if command.startswith("cd"):
        Logger.log("ZSHCOMMAND CD: {}".format(command))
        if command == "cd":
            currentUser = zshCommandOutput('echo $USER')
            currentUser = currentUser[:len(currentUser)-1]

            if platform.system() == "Darwin":

                try:
                    os.chdir('/Users/{}'.format(currentUser))
                except FileNotFoundError as not_found:
                    return "ERROR: {}!".format(not_found), 200

            elif platform.system() == "Linux":

                try:
                    os.chdir('/home/{}'.format(currentUser))
                except FileNotFoundError as not_found:
                    return "ERROR: {}!".format(not_found), 200

            else:

                return "Failed to CD to home directory.", 200

            return "Successfully changed directory to home directory.", 200
        else:

            try:
                os.chdir(command.split(" ")[1])
            except FileNotFoundError as not_found:
                return "ERROR: {}!".format(not_found), 200

            return "Changed directory to {}".format(command.split(" ")[1]), 200

    Logger.log("ZSHCOMMAND: {}".format(command))
    output = zshCommandOutput(command)

    if output == "":
        return "WARNING: EMPTY COMMAND OUTPUT", 200
    else:
        return output, 200

@app.route('/api/cwd', methods=['POST'])
def fetchCWD():
    for reqHeader in ['DLAccessCode']:
        if reqHeader not in request.headers:
            return "ERROR: {} header is not set.".format(reqHeader), 400
    if request.headers['DLAccessCode'] != os.environ['DLAccessCode']:
        return "ERROR: Access code is incorrect.", 401
    
    return zshCommandOutput("pwd"), 200