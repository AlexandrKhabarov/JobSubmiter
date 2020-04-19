import base64
import functools
import json
import unittest
from unittest.mock import patch, MagicMock

from requests import HTTPError, Timeout

from app.base import init
from config.config import Mode


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
                "text": '{\n    "result": "RUNNING"\n}\n'
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


class TestApi(unittest.TestCase):
    def setUp(self) -> None:
        app = init(Mode.TEST)
        self.client = app.test_client()

    def _open_with_authorization(self, path, method, data=None, headers=None):
        headers = headers or {}
        headers.update({'Authorization': f"Basic {base64.b64encode(b'name:pass').decode('utf8')}"})

        response = self.client.open(path=path, method=method, headers=headers, data=data)
        return response

    def _assert_response(self, actual_response, expected_status_code, expected_content):
        self.assertEqual(actual_response.status_code, expected_status_code)
        self.assertDictEqual(actual_response.json, expected_content)


class TestBuildApi(TestApi):
    open_with_authorization = functools.partialmethod(TestApi._open_with_authorization,
                                                      path="/api/v1/build",
                                                      method="POST",
                                                      headers={"Content-Type": "application/json"})

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_build_job(self):
        job_name = "job"
        response = self.open_with_authorization(data=json.dumps({"job_name": job_name}))
        expected_status_code = 201
        expected_message = {"job_name": job_name, "status": "SUBMITTED"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_build_job_with_params(self):
        job_name = "job_with_parameters"
        response = self.open_with_authorization(data=json.dumps({"job_name": job_name,
                                                                 "parameters": {"param": "value"}}))
        expected_status_code = 201
        expected_message = {"job_name": job_name, "status": "SUBMITTED"}
        self._assert_response(response, expected_status_code, expected_message)


class TestStatusApi(TestApi):
    open_with_authorization = functools.partialmethod(TestApi._open_with_authorization, method="GET")

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_success_job_status(self):
        job_name = "success_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 200
        expected_message = {"job_name": job_name, "status": "SUCCESS"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_failed_job_status(self):
        job_name = "failed_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 200
        expected_message = {"job_name": job_name, "status": "FAILED"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_running_job_status(self):
        job_name = "running_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 200
        expected_message = {"job_name": job_name, "status": "RUNNING"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_authentication_error(self):
        job_name = "authentication_error_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 401
        expected_message = {"message": 'Authentication failed'}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_not_found_error(self):
        job_name = "not_found_error_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 404
        expected_message = {"message": f'Could not find job: {job_name}'}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_jenkins_error(self):
        job_name = "jenkins_error_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 500
        expected_message = {"message": 'Something went wrong with Jenkins'}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_client_error(self):
        job_name = "client_error_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 405
        expected_message = {"message": f'Client Error for job: {job_name}'}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_timeout_error(self):
        job_name = "timeout_error_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 408
        expected_message = {"message": 'Request Timeout'}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_parsing_error(self):
        job_name = "parsing_error_job"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 500
        expected_message = {"message": f"Could not parse JSON info for job: {job_name}"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_missing_authorization(self):
        job_name = "missing_authorization_job"
        response = self.client.get(path=f"/api/v1/status/{job_name}")
        expected_status_code = 400
        expected_message = {"message": "The authorization failed because of missing Authorization header"}
        self._assert_response(response, expected_status_code, expected_message)
