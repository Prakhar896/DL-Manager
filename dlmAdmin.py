from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os, sys, json, requests, subprocess, platform
from models import *

adminApp = Flask(__name__)
CORS(adminApp)

@adminApp.route('/')
def home():
    return fileContent('admin/home.html')

if __name__ == "__main__":
    adminApp.run(host='0.0.0.0', port=8000)
