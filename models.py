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
        for envVariable in ['deepLensPwd', 'DLAccessCode']:
            if envVariable not in os.environ:
                print("SAFE BOOT ENCOUNTERED AN ERROR: {} environment variable is not set".format(envVariable))
                sys.exit(1)

        if sys.version_info[0] < 3:
            print(sys.version_info[0])
            print("Python version is too old. Please install Python 3.8 or higher.")
            sys.exit(1)

        for file in ['about.md', 'main.py', 'copyright.js', 'index.html', 'mdConverter.py', 'requirements.txt']:
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