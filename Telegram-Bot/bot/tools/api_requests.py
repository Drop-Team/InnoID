import os

import requests


class ApiRequest:
    """Making requests to app API"""
    request_function = None

    @classmethod
    def make_request(cls, *url_parts, **kwargs) -> requests.Response:
        url = os.getenv("INNOID_API_URL") + "/" + "/".join(map(str, url_parts))
        headers = {"Authorization": "Bearer {}".format(os.getenv("INNOID_API_SERVICE_APP_TOKEN"))}
        return cls.request_function(url, headers=headers, **kwargs)


class ApiGet(ApiRequest):
    request_function = requests.get


class ApiPost(ApiRequest):
    request_function = requests.post


class ApiPut(ApiRequest):
    request_function = requests.put


class ApiDelete(ApiRequest):
    request_function = requests.delete
