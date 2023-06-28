import sys
from flask import Flask, Response
from flask_cors import CORS, cross_origin

from routes.client import client_routes

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


app.register_blueprint(client_routes)


# API ROUTES
from api.queries import get_json_data


@app.route("/api/all")
@cross_origin()
def api_all():
    response = Response(get_json_data("select_all"))
    return response
