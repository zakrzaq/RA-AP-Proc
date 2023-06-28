import os
from flask import Blueprint, Response
from flask_cors import cross_origin

from utils.helpers import check_file
from api.queries import get_json_data

api_routes = Blueprint("api", __name__)


@api_routes.route("/api/all", methods=["GET"])
@cross_origin()
def api_all():
    response = Response(get_json_data("select_all"))
    return response


@api_routes.route("/api/action_log", methods=["GET"])
@cross_origin()
def api_action_log():
    action_log_path = os.path.join(os.environ["DIR_LOG"], "action_log.txt")
    check_file(action_log_path, create=True)
    with open(action_log_path, "r") as file:
        content = file.readlines()
    for c in content:
        c.replace("\n", "")
    return content
