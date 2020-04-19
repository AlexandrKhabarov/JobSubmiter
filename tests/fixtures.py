from unittest.mock import MagicMock

from requests import HTTPError, Timeout


def mocked_response_factory(mapping):
    mock = MagicMock()

    for attr, value in mapping.items():
        setattr(mock, attr, value)

    return mock


def raise_(ex):
    raise ex


class MockedJenkins:
    def __init__(self, username, token):
        self.username = username
        self.token = token

        self._expected_responses = {
            "job": mocked_response_factory({
                "status_code": 201,
                "text": '{\n    "message": "SUBMITTED"\n}\n'
            }),
            "job_with_parameters": mocked_response_factory({
                "status_code": 201,
                "text": '{\n    "message": "SUBMITTED"\n}\n'
            }),
            "success_job": mocked_response_factory({
                "status_code": 200,
                "text": '{\n    "result": "SUCCESS"\n}\n'
            }),
            "failed_job": mocked_response_factory({
                "status_code": 200,
                "text": '{\n    "result": "FAILED"\n}\n'
            }),
            "running_job": mocked_response_factory({
                "status_code": 200,
                "text": '{\n    "result": null\n}\n'
            }),
            "authentication_error_job": mocked_response_factory({
                "status_code": 401,
                "raise_for_status": lambda: raise_(HTTPError(
                    response=mocked_response_factory({
                        "status_code": 401
                    }))
                ),
            }),
            "not_found_error_job": mocked_response_factory({
                "status_code": 404,
                "raise_for_status": lambda: raise_(HTTPError(
                    response=mocked_response_factory({
                        "status_code": 404
                    }))
                ),
            }),
            "jenkins_error_job": mocked_response_factory({
                "status_code": 500,
                "raise_for_status": lambda: raise_(HTTPError(
                    response=mocked_response_factory({
                        "status_code": 500
                    }))
                ),
            }),
            "client_error_job": mocked_response_factory({
                "status_code": 405,
                "raise_for_status": lambda: raise_(HTTPError(
                    response=mocked_response_factory({
                        "status_code": 405
                    }))
                ),
            }),
            "timeout_error_job": mocked_response_factory({
                "status_code": 408,
                "raise_for_status": lambda: raise_(Timeout())
            }),
            "parsing_error_job": mocked_response_factory({
                "status_code": 200,
                "text": '{\n    "status": "RUNNING"\n}\n'
            }),
            "missing_authorization_job": mocked_response_factory({
                "status_code": 400,
                "authorization": None
            }),
        }

    def build_job(self, job_name, _):
        return self._expected_responses[job_name]

    def job_info(self, job_name):
        return self._expected_responses[job_name]
