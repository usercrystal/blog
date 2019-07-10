import requests, json, logging
import urllib
from .models import OauthUser

logger = logging.getLogger(__name__)


class OauthException(Exception):
    """oauth授权失败"""
    pass


class BaseOauth(object):
    def __init__(self, client_id, client_key, redirect_url):
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def _get(self, url, params):
        res = requests.get(url=url, params=params)
        logger.info(res.text)
        return res.text

    def _post(self, url, params):
        res =requests.post(url=url, params=params)
        logger.info(res.text)
        return res.text


class GithubOauth(BaseOauth):
    AUTH_URL = 'https://github.com/login/oauth/authorize'
    TOKEN_URL = 'https://github.com/login/oauth/access_token'
    INFO_URL = 'https://api.github.com/user'

    def __init__(self, access_token):
        self.access_token = access_token

    def get_auth_url(self):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_url,
            'scope': 'user.email',
        }
        url = self.AUTH_URL + '?' + urllib.parse.urlencode(params)
        return url

    def get_access_token(self, code):
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_key,
            'code': code,
            'redirect_url': self.redirect_url
        }
        res = self._post(self.TOKEN_URL, params)
        data = json.loads(res)
        if 'access_token' in data:
            self.access_token = str(data['access_token'])
            logger.info()
            return self.access_token
        else:
            raise OauthException

    def get_auth_user_info(self):
        params = {'access_token': self.access_token}
        res = self._get(self.INFO_URL, params)
        try:
            data = json.loads(res)
            user = OauthUser()
            user.type = 'github'
            if 'email' in data and data['email']:
                user.email = data['email ']
            return user
        except Exception as e:
            logger.error(e)
            logger.error('github oauth error.response:' + res)
            return None
