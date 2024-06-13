import json
import requests
from spotifysecreats import *
from refreshtoken import Token
import traceback
from time import sleep
import logging

logger = logging.getLogger(__name__)


class SaveSongs:
    def __init__(self):
        self.user_id = user_id
        self.playlists = [None]
        self.spotify_token, self.refresh_token = access_token, refresh_token
        logger.info("Inited successfully")

    def setspotifytoken(self, ntoken):
        self.spotify_token = ntoken

    def setrefreshtoken(self, ntoken):
        self.resfresh_token = ntoken

    def searchforid(self, searchq):
        logger.info(f"Searching for song {searchq}")
        print(f"Searching for song {searchq}...")

        query = "https://api.spotify.com/v1/search?type=track"

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}",
            },
            params={"q": f"{searchq}", "limit": 1},
        )
        response_json = response.json()

        # print(response_json["tracks"]["items"])
        try:
            for i in response_json["tracks"]["items"]:
                songuri = (
                    i["artists"][0]["name"],
                    i["name"],
                    i["album"]["name"],
                    i["duration_ms"],
                    i["album"]["release_date"],
                    i["id"],
                )
                return songuri
        except:
            self.call_resfresh()
            return self.searchforid(searchq)

    def searchforidwithlimit(self, searchq, limit):
        logger.info(f"Searching for song {searchq} with limit {limit}")
        print(f"Searching for song {searchq}...")

        url = "https://api.spotify.com/v1/search"
        try:
            response = requests.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.spotify_token}",
                },
                params={"q": searchq, "type": "track", "limit": limit},
            )
            response_json = response.json()

            # print(response_json)
            try:
                if response_json["error"]["status"] == 400:
                    print("No such song exists")
                    logger.info(response_json["error"])
                    return False
                if response_json["error"]["status"] == 401:
                    logger.info("Must refresh token")
                    self.call_resfresh()
                    logger.info("Done")
                    print("Getting new access token...")
                    return self.searchforidwithlimit(searchq, limit)
            except:
                try:
                    arraysize = min(
                        response_json["tracks"]["total"],
                        response_json["tracks"]["limit"],
                    )
                    songuri = [None] * arraysize
                    for j in range(arraysize):
                        songuri[j] = (
                            response_json["tracks"]["items"][j]["artists"][0]["name"],
                            response_json["tracks"]["items"][j]["name"],
                            response_json["tracks"]["items"][j]["album"]["name"],
                            response_json["tracks"]["items"][j]["duration_ms"],
                            response_json["tracks"]["items"][j]["album"][
                                "release_date"
                            ],
                            response_json["tracks"]["items"][j]["uri"],
                        )
                    return songuri

                except KeyError:
                    self.call_resfresh()
                    print("Getting new access token...")
                    return self.searchforidwithlimit(searchq, limit)
        except requests.exceptions.ConnectTimeout as e:
            logger.error("No internet connection")
            print("No internet connection")
            sleep(60)
            return self.searchforidwithlimit(searchq, limit)

    def createplaylist(self, name):
        logger.info(f"Creating playlists {name}")
        print("Creating playlist...")

        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

        playlistbody = json.dumps(
            {
                "name": f"{name}",
                "public": False,
            }
        )

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}",
            },
            data=playlistbody,
        )

        response_json = response.json()
        # print(response_json)
        try:
            songuri = response_json["name"], response_json["id"]
            print(f"Playlist {name} created!")
            logger.info(
                f"Created playlist {name} successfully with id {response_json['id']}"
            )
            return songuri
        except KeyError:
            logger.info("Must refresh token")
            self.call_resfresh()
            logger.info("Done")
            print("Getting new access token...")
            return self.createplaylist(name)
        except ConnectionError:
            logger.error("No internet")
            print("No internet connection, you nigger")

    def getplaylist(self, limit):
        logger.info(f"Getting last {limit} playlist(s) ")
        print("Getting playlist(s)...")

        url = "https://api.spotify.com/v1/me/playlists"

        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}",
            },
            params={
                "limit": limit,
            },
        )

        response_json = response.json()
        self.playlists = [None]
        self.playlists.pop()
        try:
            for i in response_json["items"]:
                self.playlists.append((i["name"], i["id"]))
            logger.info("Successfully got all playlists")
        except KeyError:
            logger.info("Must refresh token")
            self.call_resfresh()
            logger.info("Done")
            print("Getting new access token...")
            return self.getplaylist(limit)
        return self.playlists

    def addtoplaylist(self, playlist_id, data):
        logger.info(f"Adding song {data} to playlist {playlist_id} ")
        print("Adding to playlist")

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={data}"
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}",
            },
        )
        logger.info("Successful")

    def call_resfresh(self):
        print("Reshreshing token...")
        at, rt = resettokens()
        self.refresh_token = self.setrefreshtoken(rt)
        # print(rt)
        tokenfeet = Token()
        tokenfeet.setrefreshtoken(self.refresh_token)
        self.spotify_token = tokenfeet.RefreshToken(rt)
        # print(self.spotify_token)

    def get_user_id(self):
        logger.info("Getting user id")
        url = "https://api.spotify.com/v1/me"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}",
            },
        )
        response_json = response.json()
        # print(self.spotify_token)
        # print(response_json)
        logger.info("Successfully got user id")
        return response_json["uri"].split(":")[2]

    def getplaylistitems(self, playlist_id):
        logger.info(f"Getting tracks from playlist {playlist_id}")
        print("Getting songs from playlist... ")
        # print(playlist_id)
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        try:
            response = requests.get(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.spotify_token}",
                },
            )
        except ConnectionError:
            print("No internet connection, you nigger")
            logger.error("No internet")
        response_json = response.json()
        # print(response_json)
        try:
            listofplaylist = [None] * response_json["total"]
            for j in range(len(listofplaylist)):
                listofplaylist[j] = (
                    response_json["items"][j]["track"]["album"]["artists"][0]["name"],
                    response_json["items"][j]["track"]["name"],
                    response_json["items"][j]["track"]["album"]["name"],
                    response_json["items"][j]["track"]["duration_ms"],
                    response_json["items"][j]["track"]["album"]["release_date"],
                    response_json["items"][j]["track"]["uri"],
                )
            return listofplaylist
        except KeyError:
            logger.info("Must refresh token")
            self.call_resfresh()
            logger.info("Done")
            return self.getplaylistitems(playlist_id)

    def getdiscoverweeklyid(self):
        logger.info("Getting discover weekly playlist id")
        url = "https://api.spotify.com/v1/search?type=playlist"
        searchq = "discover weekly"
        limit = 1
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.spotify_token}",
            },
            params={"q": searchq, "type": "track", "limit": limit},
        )
        response_json = response.json()
        logger.info("Successfully got discover weekly id")
        return response_json["playlists"]["items"][0]["id"]


"""
    def removeplaylistitems(self, playlist_id, uri):

        print("Removing duplicate songs... ")
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.delete(
            url,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self.spotify_token}"
                     },
            data={
                "tracks": '{"uri":"spotify:track:6OInnmvWZstmJzAM1XmItt"}',
            },
        )
        response_json = response.json()
        print(response_json) 
"""
