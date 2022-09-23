import os

import requests

from bot.logger import logger


class ApiRequest:
    """Making requests to app API"""
    request_function = None

    @classmethod
    def make_request(cls, *url_parts, **kwargs) -> requests.Response:
        url = os.getenv("INNOID_API_URL") + "/" + "/".join(map(str, url_parts))
        headers = {"Authorization": "Bearer {}".format(os.getenv("INNOID_API_SERVICE_APP_TOKEN"))}
        response = cls.request_function(url, headers=headers, **kwargs)
        if response.status_code == 401:
            logger.error("InnoID API returned 401 (unauthorized)")
        return response


class ApiGet(ApiRequest):
    request_function = requests.get


class ApiPost(ApiRequest):
    request_function = requests.post


class ApiPut(ApiRequest):
    request_function = requests.put


class ApiDelete(ApiRequest):
    request_function = requests.delete
