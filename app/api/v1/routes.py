from flask import Blueprint
from flask_restful import Api

from app.api.v1.views import Submit, Status

blueprint = Blueprint("v1", __name__)

api = Api(blueprint)

api.add_resource(Submit, '/submit')
api.add_resource(Status, '/status/<string:job_id>')
