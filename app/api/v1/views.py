from flask_restful import Resource
from flask_restful.reqparse import RequestParser


class Submit(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument("username", type=str)
        self.parser.add_argument("password", type=str)

    @classmethod
    def post(cls):
        return "SUCCESS!"


class Status(Resource):
    @classmethod
    def get(cls, job_id):
        return f"{job_id} info"
