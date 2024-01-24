import json
from base64 import b64encode
from requests import Session
from requests.auth import AuthBase
from requests.exceptions import HTTPError


class JBAuthCode(AuthBase):

    def __init__(self, code):
        self.code = code

    def __call__(self, r):
        r.headers["Authorization"] = f"JBAuth {self.code}"

        return r


class BearerToken(AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"

        return r


class SoWeSignAuthBase:
    def get_access_token(self):
        pass


class SoWeSignAuth(SoWeSignAuthBase):
    SOWESIGN_TOKEN_URL = "https://app.sowesign.com/api/portal/authentication/token"

    def __init__(self, service_code, id_code, pin_code, session=None):
        if isinstance(session, Session):
            self._session = session
        else:
            self._session = Session()

        self.service_code = service_code
        self.id_code = id_code
        self.pin_code = pin_code

    def get_access_token(self):
        code = b64encode(f"{self.service_code}{self.id_code}{self.pin_code}".encode()).decode()
        self._session.auth = JBAuthCode(code)
        self._session.headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"

        try:
            with open(".cache.json", "r") as cache_file:
                return json.load(cache_file)["token"]
        except Exception:
            pass

        try:
            response = self._session.post(self.SOWESIGN_TOKEN_URL)
            response.raise_for_status()
            with open(".cache.json", "w") as cache_file:
                json.dump(response.json(), cache_file, indent=4)

            return response.json()["token"]

        except HTTPError as http_error:
            raise
