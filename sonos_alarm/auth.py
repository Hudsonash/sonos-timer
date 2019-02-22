import requests

class Authentication(object):
    def __init__(self, client_pub_key, client_priv_key, redirect_uri):
        self.base_url = "https://api.sonos.com/login/v3/oauth"
        self.token_url = self.base_url + '/access'
        self.client_pub_key = client_pub_key
        self.client_priv_key = client_priv_key
        self.redirect_uri = redirect_uri
        self.auth_code = None
        self.token = None


    def get_auth_url(self):
        """
        Creates a link to sign-in. Will be updated to automatically retrieve
        the code, but this is currently out of the scope of this project
        """
        auth_params = {
            "client_id": self.client_pub_key,
            "response_type": "code",
            "scope": "playback-control-all",
            "state": 1000000,
            "redirect_uri": self.redirect_uri
        }
        r = requests.get(self.base_url, params=auth_params)
        return r.url


    def get_auth_token(self):
        """
        creates the access token given the authentication code
        """

        if self.auth_code is None:
            raise ValueError("You must provide the authentication code first.")
        post_params = {
            "grant_type": "authorization_code",
            "code": self.auth_code,
            "redirect_uri": self.redirect_uri
        }
        r = requests.post(self.token_url,
                          auth = requests.auth.HTTPBasicAuth(self.client_pub_key,
                                                             self.client_priv_key),
                          data=post_params)
        if r.ok:
            self.token = r.json()
            return self.token
        else:
            raise ValueError("The request failed.")


    def renew_auth_token(self):
        """
        Creates a new token if the first has expired
        """

        if self.token is None:
            raise ValueError("The token is not yet created.")
        post_params = {
            "refresh_token": self.token['refresh_token'],
            "grant_type": "refresh_token"
        }
        r = requests.post(self.token_url,
                          auth = requests.auth.HTTPBasicAuth(self.client_pub_key,
                                                             self.client_priv_key),
                          data=post_params)
        if r.ok:
            self.token = r.json()
            return self.token
        else:
            raise ValueError("The request failed.")
