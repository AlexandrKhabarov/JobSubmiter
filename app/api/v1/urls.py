from flask import Blueprint
from flask_restful import Api

from app.api.v1.views import TriggerBuildView, FetchBuildStatusView

blueprint = Blueprint("v1", __name__)

api = Api(blueprint)

api.add_resource(TriggerBuildView, '/build')
api.add_resource(FetchBuildStatusView, '/build/<string:job_name>')
