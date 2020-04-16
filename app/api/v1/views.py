from flask.views import MethodView


class Submit(MethodView):
    @classmethod
    def post(cls):
        return "SUCCESS!"


class Status(MethodView):
    @classmethod
    def get(cls, job_id):
        return f"{job_id} info"
