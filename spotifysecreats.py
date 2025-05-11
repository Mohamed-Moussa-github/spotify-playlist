import os
import base64
import logging

logger = logging.getLogger(__name__)


def gettokens():
    logger.info("Checking if spotifysecrects.txt exists")
    program_dir = os.path.dirname(__file__)
    if os.path.exists(os.path.join(program_dir, r"data\spotifysecrets.txt")):
        logger.info("spotifysecrets.txt exists")
        filename = os.path.join(os.path.dirname(__file__), r"data\spotifysecrets.txt")
        file = open(filename, "r")
        EOF = False
        token_arr = [None] * numoflinesofthefile
        i = 0
        while not EOF:
            try:
                token_arr[i] = file.readline()
                i += 1
            except:
                EOF = not EOF
        # print(token_arr)
        access_token = token_arr[1].split("Access token: ")[1][:-1]
        refresh_token = token_arr[2].split("Refresh token: ")[1][:-1]
        user_id = token_arr[3].split("User id: ")[1][:-1]
        discover_weekly_id = token_arr[4].split("Discover weekly id: ")[1][:-1]
        logger.info("Successfully got tokens, ids")
        return access_token, refresh_token, user_id, discover_weekly_id
    else:
        logger.info(
            "Doesn't exists - Don't panic if this is the first time running program"
        )
        return 1, 1, 1, 1


def setnaccesstoken(naccesstoken):
    logger.info("Setting new tokens")
    filename = os.path.join(os.path.dirname(__file__), r"data\spotifysecrets.txt")
    logger.info(f"Opening file {filename} for read")
    file = open(filename, "r")
    EOF = False
    token_arr = [None] * numoflinesofthefile
    i = 0
    while not EOF:
        try:
            token_arr[i] = file.readline()
            i += 1
        except:
            EOF = not EOF
    file.close()
    logger.info(f"Closed file {filename}")
    logger.info(f"Opening file {filename} for write")
    file = open(filename, "w")
    for i in token_arr:
        if i[:14] == "Access token: ":
            file.write(f"Access token: {naccesstoken}\n")
        else:
            file.write(i)
    file.close()
    logger.info(f"Closed file {filename}")


def resettokens():
    logger.info("Reseting tokens")
    filename = os.path.join(os.path.dirname(__file__), r"data\spotifysecrets.txt")
    file = open(filename, "r")
    EOF = False
    token_arr = [None] * numoflinesofthefile
    i = 0
    while not EOF:
        try:
            token_arr[i] = file.readline()
            i += 1
        except:
            EOF = not EOF
    # print(token_arr)
    access_token = token_arr[1].split("Access token: ")[1][:-1]
    refresh_token = token_arr[2].split("Refresh token: ")[1][:-1]
    logger.info("Got tokens only")
    return access_token, refresh_token


client_id = r""  # your client id here
client_secrets = r""  # your client secrets here
clientsex = f"{client_id}:{client_secrets}"
base_64 = str(base64.b64encode(clientsex.encode("utf-8")), "utf-8")
website = r"https://localhost:8888/callback"
websiteurlencoded = r"https%3A%2F%2Flocalhost%3A8888%2Fcallback"
scopes = r"playlist-read-private%20playlist-modify-public%20playlist-modify-private%20user-read-currently-playing"

numoflinesofthefile = 5

access_token, refresh_token, user_id, discover_weekly_id = gettokens()
