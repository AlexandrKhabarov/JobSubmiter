import json

import requests
from flask import request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.utils.jenkins import Jenkins


class Build(Resource):
    parser = RequestParser()
    parser.add_argument("job_name", type=str, required=True)
    parser.add_argument("parameters", type=dict, default={})

    @classmethod
    def post(cls):
        authorization = request.authorization

        username = authorization.username
        token = authorization.password

        args = cls.parser.parse_args(request)

        job_name = args['job_name']
        parameters = args['parameters']

        jenkins = Jenkins(username, token)
        response = jenkins.build_job(job_name, parameters)

        response = cls._create_response(response)

        return response

    @classmethod
    def _create_response(cls, response):
        try:
            response.raise_for_status()
            res = ({"message": "Submitted"}, response.status_code)

        except requests.RequestException as e:
            res = ({"message": str(e)}, e.response.status_code)

        return res


class Status(Resource):
    @classmethod
    def get(cls, job_name):
        authorization = request.authorization

        username = authorization.username
        token = authorization.password

        jenkins = Jenkins(username, token)
        response = jenkins.job_info(job_name)
        response = cls._create_response(response)
        return response

    @classmethod
    def _create_response(cls, response):
        try:
            response.raise_for_status()
            content = json.loads(response.text)
            res = ({"status": content['result'] or "Running"}, response.status_code)

        except requests.RequestException as e:
            res = ({"message": str(e)}, e.response.status_code)

        return res
