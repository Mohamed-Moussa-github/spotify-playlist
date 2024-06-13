from spotifyapi import *
from sys import exit
from spotifysecreats import discover_weekly_id
from datetime import date
import webbrowser
from refreshtoken import *
import os
import traceback
from config import CONFIG_VALUES
import logging
from time import localtime, strftime


def initlogger():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), r"log")):
        os.makedirs(os.path.join(os.path.dirname(__file__), r"log"))

    today = strftime("%d-%m-%Y-%H-%M-%S")
    loggingFP = os.path.join(os.path.dirname(__file__), rf"log\log.log")
    # print(loggingFP)
    logging.basicConfig(
        level=logging.DEBUG,
        filename=loggingFP,
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
    )
    logging.info("Created log file")


# reads from text file where you copy paste entire playlist from youtube


def readfilefromyoutubeplaylist(filename):
    logging.info(f"Reading file from youtube with file name: {filename}")
    namearray = [None] * 201
    i = 0
    EOF = False
    file = open(filename, "r", encoding="utf-8")

    while not EOF:
        try:
            namearray[i] = file.readline().strip()
            # namearray[i] = namearray[i].split("\n")
            # namearray[i] = namearray[i][0]
            i += 1
        except:
            EOF = True
    y = 0
    actualname = [None] * 40
    for i in range(3, 201, 5):
        actualname[y] = namearray[i]
        y += 1
    file.close()
    logging.info("Read file successfully")
    return actualname


# reads from text file where you write each song-artist


def readfilenormally(filename):
    logging.info(f"Reading file with file name: {filename}")
    songlist = [None] * 100
    i = 0
    EOF = False

    try:
        file = open(filename, "r", encoding="utf-8")
    except FileNotFoundError as e:
        traceback.print_exception(e)
        print("Enter full path to file!")
        return readfilenormally(input("File path: "))

    songlist = file.read()
    songlist = songlist.split("\n")
    songlist.sort()

    for i in range(len(songlist)):
        if songlist[i] == "":
            songlist.remove(songlist[i])
        else:
            break

    file.close()
    # print(songlist)
    logging.info("Read file successfully")
    return songlist


# prints the values of dictionaries


def printdicvalues(dictionary):
    for i in dictionary.values():
        print(i)


# prints the names of dictionaries


def printdicnames(dictionary):
    y = 1
    for i in dictionary:
        print(f"{y}) {i}")
        y += 1


# prints the contents of lists


def printlists(list):
    for i in list:
        print(i)


# converts a list to a dictionary


def listtodic(list):
    return {list[i]: list[i + 1] for i in range(0, len(list), 2)}


# converts ms to minute:seconds


def mstominsec(ms):
    min = ms // 1000 // 60
    sec = ms // 1000
    sec = sec - min * 60
    return f"{min}:{sec}"


# searchs for a song with a name, returns 10 songs in a list


def searchforsongwithid(name):
    logging.info(
        f"Searching for song {name} with a limit of {CONFIG_VALUES['ReturnedLimit']}"
    )
    songlist = Songhandler.searchforidwithlimit(name, CONFIG_VALUES["ReturnedLimit"])
    if songlist != False:
        y = 1
        # print(songlist)
        # print(type(songlist))
        if not isinstance(songlist, str) and not isinstance(songlist, bool):
            for i in songlist:
                print(f"{y}) {i[0]} - {i[1]} - {i[2]} - {mstominsec(i[3])} - {i[4]}")
                y += 1

            print("'end' to end the search, 's' to skip to song")
            answer = input("Choose song: ")

            try:
                answer = int(answer)
                if answer > 0 and answer < y:
                    print(
                        f"You chose: {songlist[int(answer-1)][0]} - {songlist[int(answer-1)][1]} - {songlist[int(answer-1)][2]} - {mstominsec(songlist[int(answer-1)][3])} - {songlist[int(answer-1)][4]}"
                    )
                    songchose = songlist[int(answer - 1)]
                    logging.info(f"Retuned song {songchose}")
                    return songchose
                askquestions(songlist)
            except IndexError:
                print("Choose a song from the list nigger")
                logging.info("Wrong index when choosing song")
                return False
            except ValueError:
                if answer.strip().lower() == "end":
                    logging.info("Ended")
                    exit()
                elif answer.strip().lower() == "s":
                    logging.info("Skipped")
                    next
                else:
                    return False


def searchforsongwithidSINGE(name):
    logging.info(
        f"Searching for single song {name} with a limit of {CONFIG_VALUES['ReturnedLimit']}"
    )
    songlist = Songhandler.searchforidwithlimit(name, CONFIG_VALUES["ReturnedLimit"])
    y = 1
    if not isinstance(songlist, str) and not isinstance(songlist, bool):
        for i in songlist:
            print(f"{y}) {i[0]} - {i[1]} - {i[2]} - {mstominsec(i[3])} - {i[4]}")
            y += 1
        print("'end' to end the search")
        return askquestions(songlist)


# was continuation for function above
def askquestions(songlist):
    logger.info("In askquestions")
    answer = input("Choose song: ")

    try:
        answer = int(answer)
        if answer > 0 and answer < 10:
            print(
                f"You chose: {songlist[int(answer-1)][0]} - {songlist[int(answer-1)][1]} - {songlist[int(answer-1)][2]} - {mstominsec(songlist[int(answer-1)][3])} - {songlist[int(answer-1)][4]}"
            )
            songchose = songlist[int(answer - 1)]
            return songchose
        return askquestions(songlist)
    except IndexError:
        print("Choose a song from the list nigger")
        logging.info("Wrong index when choosing song")
        return askquestions(songlist)
    except ValueError:
        if answer.strip().lower() == "end":
            logging.info("Ended")
            exit()
        else:
            logging.info(f"Entered {answer} should forced exit and return False")
            return False


# prints the user's current playlists


def showplaylists():
    playlists = Songhandler.getplaylist()
    logging.info("Showing playlists")
    for i in playlists:
        print(i)


# inputs the playlist number, used with above function


def chooseplaylist():
    logging.info(f"Displaying first {CONFIG_VALUES['ReturnedLimit']} playlists")
    playlistlist = Songhandler.getplaylist(CONFIG_VALUES["ReturnedLimit"])
    y = 1
    for i in playlistlist:
        print(f"{y}) {i[0]}")
        y += 1
    try:
        ans = input("Playlist number: ").lower().strip()
        logging.info(f"Choose playlist number {ans}")
        ans = int(ans)
        if ans > 0 and ans < y:
            logging.info("Within rage")
            return playlistlist[ans - 1]
        else:
            logging.info("Not within range")
            return chooseplaylist()
    except ValueError as e:
        logging.info("Not integer")
        if ans == "end":
            logging.info("Ended")
            exit()
        return chooseplaylist()


# adds 1 song to a playlist with given song uri and playlist id


def addtoplaylistsingle(songuri, playlistid):
    logging.info(f"Adding song {songuri} to playlist {playlistid}")
    listofsong = Songhandler.getplaylistitems(playlistid)
    print("Checking if the song is in the playlist...")
    found = False

    for i in listofsong:
        if songuri == i[-1]:
            found = True

    if found:
        print("Song is already in playlist..")
    else:
        Songhandler.addtoplaylist(playlistid, songuri)
        logging.info("Added successfully")
    print("Done")


# truns list of song name from a text file


def addtoplayliststxtfile():
    logging.info("Adding to playlist with file")
    list = readfilenormally(input("Enter filename: "))
    songnamelist = [None]
    songnamelist.pop()

    for i in list:
        print(i)
        songnamelist.append(searchforsongwithid(i))

    return songnamelist


# creates a playlist with given name, returns playlist id


def createplaylist(name):
    logging.info(f"Creating playlist with name {name}")
    return Songhandler.createplaylist(name)


# gets the songs from the discover weekly playlist


def getdiscoverweeklyitems():
    logging.info("Getting discover weekly playlist's tracks")
    songlist = Songhandler.getplaylistitems(discover_weekly_id)
    # print(songlist)
    y = 1
    for i in songlist:
        print(f"{y}) {i[0]} - {i[1]} - {i[2]} - {mstominsec(i[3])} - {i[4]}")
        y += 1
    logging.info("Successfull")
    return songlist


def openwebspotify():
    logging.info("Opening web spotify")
    url = "https://open.spotify.com/"

    brave = webbrowser.Chrome(
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
    )
    brave.open_new_tab(url)

    logging.info("Successsfull")


listofaction = {
    "Add song": searchforsongwithidSINGE,
    "Add songs with text file": "Add songs with text file",
    "View current playlists": showplaylists,
    "View current discover weekly songs": getdiscoverweeklyitems,
    "Create new playlist": createplaylist,
    "Open spotify browser": openwebspotify,
    "Exit": exit,
}


def mainmenulist():
    printdicnames(listofaction)
    logging.info("Entering option for mainmenulist")
    option = input("Option: ")
    try:
        option = int(option)
        assert option > 0 and option < 8, "choose from list bro"
        mainmenuaction(option)
    except ValueError as e:
        logging.info("Not integer")
        mainmenulist()
    except AssertionError as e:
        logging.info("Not within range")
        mainmenulist()


def mainmenuaction(option):
    logging.info("Inside mainmenuaction")
    assert option > 0 and option < 8, "Choose from list bro"

    if option == 1:
        logging.info("Chose add song")
        songchose = listofaction["Add song"](input("Enter song name: "))
        # print(songchose)
        if songchose != False and songchose != None:

            ans = input("Add to playlist? (Y/N): ").strip().upper()

            if ans == "Y":
                playlist = chooseplaylist()
                addtoplaylistsingle(songchose[-1], playlist[-1])

    elif option == 2:
        logging.info("Chose add songs with text file")
        songlist = addtoplayliststxtfile()
        if songlist != False and songlist[0] != None:
            ans = input("Add to playlist? (Y/N): ").strip().upper()

            if ans == "Y":
                playlist = chooseplaylist()

                for i in songlist:
                    addtoplaylistsingle(i[-1], playlist[-1])

    elif option == 3:
        logging.info("Chose to display current playlists")
        playlist = chooseplaylist()
        ans = input("Show songs in playlist? (Y/N): ").strip().upper()

        if ans == "Y":
            listofsong = Songhandler.getplaylistitems(playlist[-1])
            y = 1
            for i in listofsong:
                print(f"{y}) {i[0]} - {i[1]} - {i[2]} - {mstominsec(i[3])} - {i[4]}")
                y += 1

    elif option == 4:
        logging.info("Chose to display current discover weekly")
        songlist = listofaction["View current discover weekly songs"]()
        ans = input("Save? (Y/N): ").upper().strip()

        if ans == "Y":
            today = date.today()
            today = today.strftime("%d/%m/%Y")
            playlist = createplaylist(f"{today}'s discover weekly")
            print(playlist)

            for i in songlist:
                addtoplaylistsingle(i[-1], playlist[-1])

    elif option == 5:
        logging.info("Chose to create new playlist")
        listofaction["Create new playlist"](input("Enter name of playlist: "))

    elif option == 6:
        logging.info("Chose to open web spotify")
        listofaction["Open spotify browser"]()

    else:
        logging.info("Ended")
        exit()

    mainmenulist()


# check if first time doing it


def checknewfag():
    logging.info("Checking if new fag")
    program_dir = os.path.dirname(__file__)

    # if not os.path.exists(os.path.join(program_dir, r"data\spotifysecrets.txt")):
    if not os.path.exists(os.path.join(program_dir, "data")):
        os.mkdir(os.path.join(program_dir, "data"))
        logging.info(f"Created dir at {os.path.join(program_dir, 'data')}")

    TokenHandler = Token()

    logging.info("Getting user authorization")
    code = TokenHandler.Request_User_Authorization()
    logging.info("Got user authorization")
    logging.info("Requesting access token")
    accesstoken, refreshtoken = TokenHandler.Request_Access_Token(code)

    filename = os.path.join(program_dir, r"data\spotifysecrets.txt")
    logging.info(rf"Creating txt file at {filename}")
    file = open(filename, "w")

    file.writelines(f"Code: {code}\n")
    file.writelines(f"Access token: {accesstoken}\n")
    file.writelines(f"Refresh token: {refreshtoken}\n")

    file.close()
    logging.info("Done with file")
    access_token, refresh_token = resettokens()

    global Songhandler
    Songhandler = SaveSongs()
    Songhandler.setspotifytoken(access_token)
    Songhandler.setrefreshtoken(refresh_token)

    adduseridanddiscordidtofile()


def adduseridanddiscordidtofile():
    logging.info("Inside adduseridtodiscovertofile")
    filename = os.path.join(os.path.dirname(__file__), r"data\spotifysecrets.txt")
    logging.info(f"Into file {filename}")
    file = open(filename, "a")
    user_id = Songhandler.get_user_id()
    discoverweekly_id = Songhandler.getdiscoverweeklyid()
    file.write(f"User id: {user_id}\n")
    file.write(f"Discover weekly id: {discoverweekly_id}\n")
    file.close()
    logging.info("Done with file")

    global discover_weekly_id

    access_token, refresh_token, user_id, discover_weekly_id = gettokens()


def main():
    initlogger()
    if not os.path.exists(
        os.path.join(os.path.dirname(__file__), r"data\spotifysecrets.txt")
    ):
        checknewfag()
    else:
        global Songhandler
        Songhandler = SaveSongs()
    mainmenulist()

    
if __name__ == "__main__":
    main()
