from flask import Flask
from restaurantApp import config
from restaurantApp.persistence import add_default_data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.data["upload_folder"]


#from restaurantApp.router import views, jsonEndpoints, xmlEndpoints

from restaurantApp.router import jsonEndpoints, xmlEndpoints


log = 'test'
