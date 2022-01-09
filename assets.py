from main import *

## Assets endpoints
@app.route('/assets/copyright')
def copyright():
    return fileContent('copyright.js')

@app.route('/assets/indexJS')
def indexJS():
    return fileContent('index.js')

@app.route('/assets/homeJS')
def homeJS():
    return fileContent('supportFiles/home.js')

@app.route('/assets/baseJS')
def baseJS():
    return fileContent('supportFiles/base.js')

@app.route('/assets/zshJS')
def zshJS():
    return fileContent('supportFiles/zsh.js')