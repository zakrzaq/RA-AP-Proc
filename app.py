import sys
from flask import Flask
from flask_cors import CORS

from routes.client import client_routes
from routes.api import api_routes

from utils.startup import check_process_files
from utils.helpers import use_logger


use_logger()
try:
    check_process_files()
except Exception as Argument:
    print(Exception)
    sys.exit(1)


app = Flask(__name__)
CORS(app)

# Routes

app.register_blueprint(client_routes)
app.register_blueprint(api_routes)

