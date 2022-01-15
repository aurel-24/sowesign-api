import base64

import requests
from requests.auth import AuthBase


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers[
            "Authorization"] = "Bearer " + self.token

        return r


class URLs:
    def __init__(self):
        self.base_url = "https://app.sowesign.com/api/"

        # authentication
        self.token = "portal/authentication/token"

        # student app
        # self.students = "student-app/{}".format(self.student_id)
        self.courses = "student-app/courses"
        self.future_courses = "student-app/future-courses"

    def token_url(self):
        return self.base_url + self.token

    """def students_url(self):
        return self.base_url + self.students"""

    def courses_url(self):
        return self.base_url + self.courses

    def future_courses_url(self):
        return self.base_url + self.future_courses


class SWS:
    def __init__(self, group_code, id_code, pin_code, auth_token=None, response_format='json'):
        self.url = URLs()

        self.auth_token = auth_token
        self.group_code = group_code
        self.id_code = id_code
        self.pin_code = pin_code
        self.format = response_format

        self.auth = None
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}

    def __create_auth(self):
        auth = base64.b64encode((str(self.group_code) + str(self.id_code) + str(self.pin_code)).encode()).decode()
        self.headers['authorization'] = "JBAuth " + auth
        if not self.auth:
            token = requests.post(self.url.token_url(), headers=self.headers).json()['token']
            self.auth = BearerAuth(token)

    def __to_format(self, response: requests.Response):
        if self.format == 'json':
            return response.json()
        else:
            return response.content

    def __get_data(self, url: str, params: dict):
        self.__create_auth()
        return self.__to_format(requests.get(url, auth=self.auth, headers=self.headers, params=params))

    def get_courses(self, start: str, end: str):
        self.__create_auth()
        return self.__get_data(self.url.courses_url(), params={'from': start, 'to': end})

    def get_future_courses(self, limit: int):
        self.__create_auth()
        return self.__get_data(self.url.future_courses_url(), {'limit': limit})
