import jenkins
from flask import request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.task.task import submit_async_job


class Submit(Resource):
    parser = RequestParser()
    parser.add_argument("username", type=str, required=True)
    parser.add_argument("password", type=str, required=True)
    parser.add_argument("job_name", type=str, required=True)
    parser.add_argument("parameters", type=dict, default={})

    @classmethod
    def post(cls):
        args = cls.parser.parse_args(request)
        submit_async_job.apply_async(kwargs={"args": args})

        return {"status": "submitted"}, 202


class Status(Resource):
    @classmethod
    def get(cls, job_name):
        try:
            server = jenkins.Jenkins('http://localhost:8080', "admin", "admin")
            job_info = server.get_job_info(job_name)
            last_build = job_info['lastBuild']
            if last_build is None:
                raise jenkins.JenkinsException(f"Job {job_name} have not been built")
            current_build_number = last_build['number']
            build_info = server.get_build_info(job_name, current_build_number)
        except jenkins.JenkinsException as e:
            return {"message": str(e)}, 404
        else:
            return {"job_name": job_name, "status": build_info['result']}, 200
