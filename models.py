import sys, os, json, requests, datetime, platform, random, markdown, pygments
import mdConverter
from dotenv import load_dotenv
load_dotenv()

def fileContent(fileName, mdConverterEnabled=False):
    if mdConverterEnabled:
        with open(os.path.join(os.getcwd(), fileName), 'r') as f:
            f_content = f.read()
            return mdConverter.convert(f_content)
    else:
        with open(os.path.join(os.getcwd(), fileName), 'r') as f:
            f_content = f.read()
            return f_content

def generateAuthToken():
    letters_lst = ['a', 'e', 'w', 't', 'a', 'u', 'o', 'p', '2', '5', '6', '3', '8', '4']
    authTokenString = ''
    while len(authTokenString) < 10:
        authTokenString += random.choice(letters_lst)
    return authTokenString

def zshCommandOutput(command):
    return os.popen(command).read()

def checkAuthTokenValidity(authToken, validAuthTokens):
    isValid = False
    for timeKey in validAuthTokens:
        if validAuthTokens[timeKey] == authToken:
            isValid = True
    if not isValid:
        return "<h1>Invalid auth token. Please obtain a new auth token by making a password check request.</h1>", 401
    return True

def safeBootProcess():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        for envVariable in ['deepLensPwd', 'DLAccessCode', 'RuntimePort', 'LoggingEnabled', 'DebugMode']:
            if envVariable not in os.environ:
                print("SAFE BOOT ENCOUNTERED AN ERROR: {} environment variable is not set".format(envVariable))
                sys.exit(1)

        if sys.version_info[0] < 3:
            print(sys.version_info[0])
            print("Python version is too old. Please install Python 3.8 or higher.")
            sys.exit(1)

        for file in ['about.md', 'main.py', 'api.py', 'dlmAdmin.py', 'session.py', 'assets.py', 'activation.py', 'copyright.js', 'index.html', 'mdConverter.py', 'requirements.txt']:
            if not os.path.exists(file):
                print("SAFE BOOT ENCOUNTERED AN ERROR: Required file `{}` not found.".format(file))
                sys.exit(1)

        # Install required libraries
        for library in ['flask', 'flask_cors', 'requests', 'datetime', 'mdConverter', 'dotenv', 'pygments', 'markdown', 'random']:
            try:
                __import__(library)
            except ImportError:
                print("SAFE BOOT ENCOUNTERED AN ERROR: Required library `{}` not found.".format(library))
                print()
                print("Automatically installing libraries required for the system...")
                print()
                os.system("pip install -r requirements.txt")
                print()
                print("Please re-boot the system.")
                sys.exit(1)
                
        print("Safe boot success!")
    else:
        print("SAFE BOOT ENCOUNTERED AN ERROR: OS not supported (OS is not the AWS DeepLens' Linux.)")
        sys.exit(1)
        
class Logger:
    '''## Intro
    A class offering silent and quick logging services.

    Explicit permission must be granted by setting `LoggingEnabled` to `True` in the `.env` file. Otherwise, all logging services will be disabled.
    
    ## Usage:
    ```
    Logger.setup() ## Optional

    Logger.log("Hello world!") ## Adds a log entry to the logs.txt database file, if permission was granted.
    ```

    ## Advanced:
    Activate Logger's management console by running `Logger.manageLogs()`. This will allow you to read and destroy logs in an interactive manner.
    '''
    
    bootPath = os.path.join(os.getcwd(), "logs.txt")
    
    @staticmethod
    def checkPermission():
        if "LoggingEnabled" in os.environ and os.environ["LoggingEnabled"] == 'True':
            return True
        else:
            return False

    @staticmethod
    def setup():
        if Logger.checkPermission():
            try:
                if not os.path.exists(Logger.bootPath):
                    with open(Logger.bootPath, "w") as f:
                        f.write("{}UTC {}\n".format(datetime.datetime.now(datetime.timezone.utc).isoformat(), "LOGGER: Logger database file setup complete."))
            except Exception as e:
                print("LOGGER SETUP ERROR: Failed to setup logs.txt database file. Setup permissions have been granted. Error: {}".format(e))

        return

    @staticmethod
    def log(message, debugPrintExplicitDeny=False):
        if "DebugMode" in os.environ and os.environ["DebugMode"] == 'True' and (not debugPrintExplicitDeny):
            print("LOG: {}".format(message))
        
        if Logger.checkPermission():
            try:
                with open(Logger.bootPath, "a+") as f:
                    f.write("{}UTC {}\n".format(datetime.datetime.now(datetime.timezone.utc).isoformat(), message))
            except Exception as e:
                print("LOGGER LOG ERROR: Failed to log message. Error: {}".format(e))
        
        return
    
    @staticmethod
    def destroyAll():
        try:
            if os.path.exists(os.path.join(os.getcwd(), Logger.bootPath)):
                os.remove(Logger.bootPath)
        except Exception as e:
            print("LOGGER DESTROYALL ERROR: Failed to destroy logs.txt database file. Error: {}".format(e))

    @staticmethod
    def readAll():
        if not Logger.checkPermission():
            return "ERROR: Logging-related services do not have permission to operate."
        try:
            if os.path.exists(os.path.join(os.getcwd(), Logger.bootPath)):
                with open(Logger.bootPath, "r") as f:
                    logs = f.readlines()
                    for logIndex in range(len(logs)):
                        logs[logIndex] = logs[logIndex].replace("\n", "")
                    return logs
            else:
                return []
        except Exception as e:
            print("LOGGER READALL ERROR: Failed to check and read logs.txt database file. Error: {}".format(e))
            return "ERROR: Failed to check and read logs.txt database file. Error: {}".format(e)
      
    @staticmethod
    def manageLogs():
        permission = Logger.checkPermission()
        if not permission:
            print("LOGGER: Logging-related services do not have permission to operate. Set LoggingEnabled to True in .env file to enable logging.")
            return
    
        print("LOGGER: Welcome to the Logging Management Console.")
        while True:
            print("""
Commands:
    read <number of lines, e.g 50 (optional)>: Reads the last <number of lines> of logs. If no number is specified, all logs will be displayed.
    destroy: Destroys all logs.
    exit: Exit the Logging Management Console.
""")
    
            userChoice = input("Enter command: ")
            userChoice = userChoice.lower()
            while not userChoice.startswith("read") and (userChoice != "destroy") and (userChoice != "exit"):
                userChoice = input("Invalid command. Enter command: ")
                userChoice = userChoice.lower()
    
            if userChoice.startswith("read"):
                allLogs = Logger.readAll()
                targetLogs = []

                userChoice = userChoice.split(" ")

                # Log filtering feature
                if len(userChoice) == 1:
                    targetLogs = allLogs
                elif userChoice[1] == ".filter":
                    if len(userChoice) < 3:
                        print("Invalid log filter. Format: read .filter <keywords>")
                        continue
                    else:
                        try:
                            keywords = userChoice[2:]
                            for log in allLogs:
                                logTags = log[32::]
                                logTags = logTags[:logTags.find(":")].upper().split(" ")

                                ## Check if log contains all keywords
                                containsAllKeywords = True
                                for keyword in keywords:
                                    if keyword.upper() not in logTags:
                                        containsAllKeywords = False
                                        break
                                
                                if containsAllKeywords:
                                    targetLogs.append(log)
                                
                            print("Filtered logs with keywords: {}".format(keywords))
                            print()
                        except Exception as e:
                            print("LOGGER: Failed to parse and filter logs. Error: {}".format(e))
                            continue
                else:
                    logCount = 0
                    try:
                        logCount = int(userChoice[1])
                        if logCount > len(allLogs):
                            logCount = len(allLogs)
                        elif logCount <= 0:
                            raise Exception("Invalid log count. Must be a positive integer above 0 lower than or equal to the total number of logs.")
                        
                        targetLogs = allLogs[-logCount::]
                    except Exception as e:
                        print("LOGGER: Failed to read logs. Error: {}".format(e))
                        continue

                logCount = len(targetLogs)
                print()
                print("Displaying {} log entries:".format(logCount))
                print()
                for log in targetLogs:
                    print("\t{}".format(log))
            elif userChoice == "destroy":
                Logger.destroyAll()
                print("LOGGER: All logs destroyed.")
            elif userChoice == "exit":
                print("LOGGER: Exiting Logging Management Console...")
                break
    
        return