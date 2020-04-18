from urllib.parse import urlencode

import requests


class Jenkins:
    _URL = ""

    _JOB_INFO = 'job/{job_name}/lastBuild/api/json'
    _BUILD_JOB = 'job/{job_name}/build'
    _BUILD_JOB_WITH_PARAMETERS = 'job/{job_name}/buildWithParameters'

    def __init__(self, username, token):
        self.username = username
        self.token = token
        self._server = self._URL

    @classmethod
    def init_url(cls, url):
        cls._URL = url

    def build_job(self, job_name, parameters):
        request_url = self._create_build_job_url(job_name, parameters)
        response = self._request("post", request_url)
        return response

    def job_info(self, job_name):
        request_url = self._create_job_info_url(job_name)
        response = self._request("get", request_url)
        return response

    def _create_job_info_url(self, job_name):
        url = self._build_url(self._JOB_INFO, job_name)
        return url

    def _create_build_job_url(self, job_name, parameters):
        if parameters:
            url = self._build_url(self._BUILD_JOB_WITH_PARAMETERS, job_name)
            url = url + '?' + urlencode(parameters)
        else:
            url = self._build_url(self._BUILD_JOB, job_name)
        return url

    def _build_url(self, suffix, job_name):
        url = self._URL + "/" + suffix.format(job_name=job_name)
        return url

    def _request(self, method, request):
        response = requests.request(method, request, auth=(self.username, self.token))
        return response
