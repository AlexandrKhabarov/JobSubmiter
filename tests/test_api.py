import base64
import functools
import json
import unittest
from unittest.mock import patch

from app.base import init
from config.config import Mode


class DummyResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        pass


class MockedJenkins:
    def __init__(self, username, token):
        self.username = username
        self.token = token

        self._job_info_responses = {
            "success": DummyResponse(200, '{\n    "result": "SUCCESS"\n}\n'),
            "failed": DummyResponse(200, '{\n    "result": "FAILED"\n}\n'),
            "running": DummyResponse(200, '{\n    "result": "RUNNING"\n}\n'),
        }

        self._build_responses = {
            "job1": DummyResponse(201, '{\n    "message": "SUBMITTED"\n}\n'),
            "job2": DummyResponse(201, '{\n    "message": "SUBMITTED"\n}\n'),
        }

    def build_job(self, job_name, _):
        return self._build_responses[job_name]

    def job_info(self, job_name):
        return self._job_info_responses[job_name]


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
        response = self.open_with_authorization(data=json.dumps({"job_name": "job1"}))
        expected_status_code = 201
        expected_message = {"message": "SUBMITTED"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_build_job_with_params(self):
        response = self.open_with_authorization(data=json.dumps({"job_name": "job2", "parameters": {"param": "value"}}))
        expected_status_code = 201
        expected_message = {"message": "SUBMITTED"}
        self._assert_response(response, expected_status_code, expected_message)


class TestStatusApi(TestApi):
    open_with_authorization = functools.partialmethod(TestApi._open_with_authorization, method="GET")

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_success_job_status(self):
        job_name = "success"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 200
        expected_message = {"job_name": job_name, "status": "SUCCESS"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_failed_job_status(self):
        job_name = "failed"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 200
        expected_message = {"job_name": job_name, "status": "FAILED"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_running_job_status(self):
        job_name = "running"
        response = self.open_with_authorization(path=f"/api/v1/status/{job_name}")
        expected_status_code = 200
        expected_message = {"job_name": job_name, "status": "RUNNING"}
        self._assert_response(response, expected_status_code, expected_message)

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_authentication_error(self):
        pass

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_not_found_error(self):
        pass

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_jenkins_error(self):
        pass

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_client_error(self):
        pass

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_timeout_error(self):
        pass

    @patch("app.api.v1.views.Jenkins", new=MockedJenkins)
    def test_parsing_error(self):
        pass
