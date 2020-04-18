from flask import Blueprint
from flask_restful import Api

from app.api.v1.views import BuildView, StatusView

blueprint = Blueprint("v1", __name__)

api = Api(blueprint)

api.add_resource(BuildView, '/build')
api.add_resource(StatusView, '/status/<string:job_name>')
