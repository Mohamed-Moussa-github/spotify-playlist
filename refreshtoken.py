import requests
from spotifysecreats import *
import webbrowser
import logging

logger = logging.getLogger(__name__)


class Token:
    def __init__(self):
        self.access_token, self.refresh_token = access_token, refresh_token
        self.base_64 = base_64
        logger.info("Initied successfully")

    def setrefreshtoken(self, ntoken):
        self.refresh_token = ntoken

    def RefreshToken(self, refresh_token):
        logger.info("Refreshing token")
        url = "https://accounts.spotify.com/api/token"
        # print(refresh_token)
        response = requests.post(
            url,
            headers={
                "Authorization": f"Basic {self.base_64}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            params={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        )
        response_json = response.json()
        # (response_json)
        naccess_token = response_json["access_token"]
        logger.info("Successfull")
        setnaccesstoken(naccess_token)
        return naccess_token

    def Request_User_Authorization(self):
        logger.info("Requesting user autorization")
        url = "https://accounts.spotify.com/authorize?"
        actualurl = f"{url}client_id={client_id}&response_type=code&redirect_uri={websiteurlencoded}&scope={scopes}"
        webbrowser.open_new_tab(actualurl)
        logger.info("Open webbrowser")
        recalllink = input("Enter redirect url: ")
        logger.info(f"Recall link: {recalllink}")
        token = recalllink.split("code=")
        try:
            return token[1]
        except IndexError as e:
            logger.info(f"Didn't include 'code=' so had to recall")
            print("Enter the url that you got redirected to!")
            return self.Request_User_Authorization()

    def Request_Access_Token(self, token):
        logger.info("Requesting access token")
        url = "https://accounts.spotify.com/api/token?"
        respone = requests.post(
            url,
            headers={
                "Authorization": f"Basic {base_64}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            params={
                "grant_type": "authorization_code",
                "code": f"{token}",
                "redirect_uri": website,
            },
        )
        response_json = respone.json()
        logger.info("Successful")
        return response_json["access_token"], response_json["refresh_token"]
