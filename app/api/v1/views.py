import json

from flask import request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from requests import HTTPError, Timeout

from app.utils.jenkins import Jenkins


def authorization_header_required(f):
    def decorator(*args, **kwargs):
        if request.authorization is None:
            res = ({"message": "The authorization failed because of missing Authorization header"}, 400)
            return res
        return f(*args, **kwargs)

    return decorator


class BaseView(Resource):
    decorators = (authorization_header_required,)

    @classmethod
    def _build_response(cls, response, job_name):
        try:
            response.raise_for_status()
            res = cls._build_success_response(response, job_name)
        except HTTPError as e:
            if e.response.status_code in [401, 403]:
                res = ({"message": 'Authentication failed'}, response.status_code)
            elif e.response.status_code == 404:
                res = ({"message": f'Could not find job: {job_name}'}, response.status_code)
            elif e.response.status_code >= 500:
                res = ({"message": 'Something went wrong with Jenkins'}, response.status_code)
            else:
                res = ({"message": f'Client Error for job: {job_name}'}, response.status_code)
        except Timeout:
            res = ({"message": 'Request Timeout'}, response.status_code)
        except (KeyError, ValueError):
            res = ({"message": f"Could not parse JSON info for job: {job_name}"}, 500)

        return res

    @classmethod
    def _build_success_response(cls, response, job_name):
        raise NotImplementedError


class TriggerBuildView(BaseView):
    parser = RequestParser()
    parser.add_argument("job_name", type=str, required=True, help="job_name must be a string")
    parser.add_argument("parameters", type=dict, default={}, help="parameters must be a dict")

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

        response = cls._build_response(response, job_name)

        return response

    @classmethod
    def _build_success_response(cls, response, job_name):
        res = ({"job_name": job_name, "status": "SUBMITTED"}, response.status_code)
        return res


class FetchBuildStatusView(BaseView):
    @classmethod
    def get(cls, job_name):
        authorization = request.authorization

        username = authorization.username
        token = authorization.password

        jenkins = Jenkins(username, token)
        response = jenkins.job_info(job_name)
        response = cls._build_response(response, job_name)
        return response

    @classmethod
    def _build_success_response(cls, response, job_name):
        content = json.loads(response.text)
        status = content['result']
        status = status or "RUNNING"
        res = ({"job_name": job_name, "status": status}, response.status_code)
        return res
