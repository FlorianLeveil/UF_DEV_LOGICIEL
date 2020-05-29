import threading
import sys
import spotipy

from os import system, name, environ, remove
from time import sleep
from json.decoder import JSONDecodeError

from search_artist import search_artist
from lecteur import lecteur
from search_playlist import search_playlist
from setting_playlist import print_all_playlist,know_rules_playlist, print_rules, munu_playlist_setting, create_new_playlist


#for connexion to spotify with a big scope
environ["SPOTIPY_CLIENT_SECRET"] = ""
environ["SPOTIPY_CLIENT_ID"] = ""
environ["SPOTIPY_REDIRECT_URI"] ='http://localhost:9090/callback'
scope = 'ugc-image-upload user-follow-read user-follow-modify user-read-recently-played user-top-read user-read-playback-position user-library-read user-library-modify user-read-playback-state user-read-currently-playing user-modify-playback-state playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private streaming app-remote-control user-read-email user-read-private'


# Get the username from terminal
username = sys.argv[1]

# Erase cache and prompt for user permission
try:
    token = spotipy.util.prompt_for_user_token(username, scope) # add scope
except (AttributeError, JSONDecodeError):
    remove(f".cache-{username}")
    token = spotipy.util.prompt_for_user_token(username, scope) # add scope

# Create our spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)

# Get current device
devices = spotifyObject.devices()
deviceID = devices['devices'][0]['id']


# User information
user = spotifyObject.current_user()
displayName = user['display_name']
followers = user['followers']['total']

# Loop
while True:
    # Main Menu
    _ = system('clear')
    print()
    print(">>> Welcome " + displayName + "!")
    print(">>> You have " + str(followers) + " followers.")
    print()
    print("0 - Search for an artist")
    print("1 - Search for a playlist")
    print("2 - Play one of my playlist")
    print("3 - Resume")
    print("4 - Setting playlist")
    print("5 - exit")
    print()
    choice = input("Your choice: ")
    global return_for_resume

    #Search for an artist
    if choice == "0":
        result_search_artist = search_artist(spotifyObject, deviceID)
        songSelection = input("Enter a song number to see album art and play the song (x to exit): ") # and play the song
        trackSelectionList = []
        trackSelectionList.append(result_search_artist[int(songSelection)])
        _ = system("clear")
        type_use = "play_one_song"
        spotifyObject.start_playback(deviceID, None, trackSelectionList)
        sleep(0.3)
        return_for_resume = lecteur(spotifyObject,playlist=None, deviceID=None, trackSelectionList=trackSelectionList, type_use=type_use)
    
    #Search for a playlist
    if choice == '1':
        result_search_playlist = search_playlist(spotifyObject, deviceID)
        _ = system("clear")
        type_use = "play_playlist"
        spotifyObject.start_playback(deviceID, result_search_playlist["uri"])
        sleep(1)
        return_for_resume = lecteur(spotifyObject,playlist=result_search_playlist,deviceID=deviceID,type_use=type_use)

    #Play one of my playlist
    if choice == "2":
        _ = system("clear")
        all_playlist = spotifyObject.user_playlists(user["id"], limit=50)
        items = all_playlist["items"]
        print("Names :")
        compteur = 0
        for one_playlist in items:
            print(compteur, ":", one_playlist["name"])
            compteur += 1

        commande = input("Enter number of playlist: ") # and play the song
        commande = int(commande)
        type_use = "my_playlist"
        _ = system("clear")
        spotifyObject.start_playback(deviceID, items[commande]["uri"])
        sleep(0.2)
        return_for_resume = lecteur(spotifyObject,playlist=items[commande],deviceID=deviceID, type_use=type_use)


    #Resume
    if choice == '3':
        current_track = spotifyObject.currently_playing() 

        if return_for_resume == 'play_one_song':
            progress_ms = current_track["progress_ms"]
            trackSelectionList = []
            trackSelectionList.append(current_track["item"]["uri"])
            _ = system("clear")
            type_use = "play_one_song"
            spotifyObject.start_playback(deviceID, None, trackSelectionList, position_ms=progress_ms)
            sleep(0.3)
            return_for_resume
            return_for_resume = lecteur(spotifyObject,playlist=None, deviceID=None, trackSelectionList=trackSelectionList, type_use=type_use)

        if return_for_resume == 'my_playlist':
            type_use = "my_playlist"
            _ = system("clear")
            position_track = int(current_track['progress_ms'])
            spotifyObject.start_playback(deviceID,current_track["context"]["uri"],offset={"uri": current_track["item"]["uri"]},position_ms=position_track)
            sleep(0.2)
            return_for_resume = lecteur(spotifyObject,playlist=items[commande],deviceID=deviceID, type_use=type_use)

        if return_for_resume == 'play_playlist':
            pass
    
    #Setting playlist
    if choice == "4":
        user_choice = munu_playlist_setting()
        if user_choice == '1':
            playlist_to_set = print_all_playlist(spotifyObject, user)
            know_rules = know_rules_playlist(playlist_to_set, user)
            print_rules(spotifyObject,know_rules, playlist_to_set, user)
        elif user_choice == '2':
            create_new_playlist(spotifyObject,user)
        elif user_choice == '3':
            pass

    #Exit    
    if choice == "5":
        break
                 
            


