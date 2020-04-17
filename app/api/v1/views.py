import jenkins
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.task.task import submit_async_job


class Submit(Resource):
    parser = RequestParser()
    parser.add_argument("token", type=str)
    parser.add_argument("job_name", type=str)
    parser.add_argument("parameters", type=dict)

    @classmethod
    def post(cls):
        args = cls.parser.parse_args()
        submit_async_job.apply_async(args=args)

        return {"status": "submitted"}


class Status(Resource):
    @classmethod
    def get(cls, job_name):
        server = jenkins.Jenkins('http://localhost:8080')
        job_info = server.get_job_info('build_name')
        current_build_number = job_info['currentBuildNumber']
        build_info = server.get_build_info(job_name, current_build_number)

        return {"job_name": job_name, "status": build_info['result']}
