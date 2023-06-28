from flask import Blueprint, Response
from flask_cors import cross_origin

from api.queries import get_json_data

api_routes = Blueprint("api", __name__)


@api_routes.route("/api/all", methods=["GET"])
@cross_origin()
def api_all():
    response = Response(get_json_data("select_all"))
    return response
