from flask import Blueprint
from flask_restful import Api

from app.api.v1.views import Build, Status

blueprint = Blueprint("v1", __name__)

api = Api(blueprint)

api.add_resource(Build, '/build')
api.add_resource(Status, '/status/<string:job_name>')
