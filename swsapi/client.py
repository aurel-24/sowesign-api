import requests
from requests import Session
from requests.exceptions import HTTPError

from .auth import BearerToken, SoWeSignAuthBase
from .url import URLManager


class SoWeSign:
    def __init__(self, auth_token=None, auth_manager=None, response_format='json', session=None):
        """

        :param str auth_token: un jeton d'authentification
        :param SoWeSignAuthBase auth_manager: un gestionnaire d'authentification
        :param str response_format:
        :param Session session: une session pour les requêtes HTTP
        """
        if isinstance(session, Session):
            self._session = session
        else:
            self._session = Session()

        self.auth_token = auth_token
        self.auth_manager = auth_manager
        self.format = response_format

    def _get_auth(self):
        if self.auth_token:
            return BearerToken(self.auth_token)
        elif self.auth_manager:
            return BearerToken(self.auth_manager.get_access_token())
        else:
            raise Exception("Aucun moyen d'authentification spécifié")

    def __to_format(self, response: requests.Response):
        if self.format == 'json':
            return response.json()
        else:
            return response.content

    def _http_call(self, method, url, params=None, payload=None):
        self._session.auth = self._get_auth()
        self._session.headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"

        try:
            response = self._session.request(method, url, params, payload)
            response.raise_for_status()

            return response

        except HTTPError as http_error:
            print(http_error)

    def courses(self, start, end):
        """
        Retourne tous les cours compris dans l'intervalle de temps donné.

        :param str start: la date de début au format AAAA-MM-JJ
        :param str end: la date de fin au format AAAA-MM-JJ
        :return:
        """
        return self._http_call("GET", URLManager.get_courses_url(), params={'from': start, 'to': end}).json()

    def future_courses(self, limit=10):
        """
        Retourne les prochains cours de l'utilisateur connecté.

        :param int limit: le nombre de cours à retourner
        :return:
        """
        return self._http_call("GET", URLManager.get_future_courses_url(), params={"limit": limit}).json()
