from os import system
from time import sleep
from progress_bar import start_progress_bar, runing_false
from setting_playlist import print_all_playlist, know_rules_playlist


#A lecteur with option and progress bar
def lecteur(spotifyObject, playlist=None, deviceID= None, trackSelectionList=None, type_use=None):
    current_payback = spotifyObject.current_playback()
    paused = False
    runing = False
    first = True
    single_track = False
    shuffle = current_payback["shuffle_state"]

    #Set volume
    volume_round = round((current_payback["device"]["volume_percent"]/10))*10
    spotifyObject.volume(volume_round, deviceID)
    volume = volume_round
    the_playlist = playlist

    if playlist == None:
        single_track = True

    #Run thread progress bar
    progress_bar = start_progress_bar(spotifyObject, the_playlist, running = runing, type_use=type_use)

    #The menu
    while True:

        #Jump up for input
        if first == False:
            print("\033[F"*2)
        the_input = input('''Your commande: 
        ''')
        print("\033[F"*3)
        first = False

        #Pause
        if the_input == 'p' and not paused:
            paused = True
            spotifyObject.pause_playback(deviceID)
            progress_bar.paused_x(spotifyObject, single_track)

        #Follow a playlist when you play a playlist
        elif the_input == 'a'and type_use == 'play_playlist':
            spotifyObject.user_playlist_follow_playlist(the_playlist["owner"]["id"], the_playlist["id"])       

        #Play
        elif the_input == 'l'and paused:
            paused = False
            current_track = spotifyObject.currently_playing()                
            progress_bar.paused_x(current_track, single_track, trackSelectionList)
            print("\n"*1, end="")

        #Exit
        elif the_input == 'x':
            runing_false()
            spotifyObject.pause_playback(deviceID)
            sleep(0.02)
            _ = system('clear')
            return type_use
        
        # Add your current song to a playlist
        elif the_input == 'r':
            runing_false()
            sleep(0.2)
            paused = True
            spotifyObject.pause_playback(deviceID)
            progress_bar.paused_x(spotifyObject, single_track)
            user = spotifyObject.current_user()
            _ = system("clear")
            while True:
                playlist_to_set = print_all_playlist(spotifyObject, user)
                know_rules = know_rules_playlist(playlist_to_set, user)
                current_track = spotifyObject.current_playback()
                id_track = str(current_track["item"]["id"])
                if know_rules == True:
                    the_track = [id_track]
                    spotifyObject.user_playlist_add_tracks(user["id"],playlist_to_set["id"],the_track)
                    _ = system("clear")
                    break
                else:
                    print()
                    print("You are not the owner of this playlist !")
                    print()
                    pass
            break
        
        # next song when you play a playlist
        elif the_input == 'n' and single_track == False:
            runing_false()
            sleep(0.2)
            spotifyObject.next_track(deviceID)
            _ = system('clear')
            print("\033[F"*13)
            progress_bar = start_progress_bar(spotifyObject, the_playlist, running = runing, type_use=type_use)

        # previous song when you play a playlist
        elif the_input == 'b' and single_track == False:
            runing_false()
            sleep(0.2)
            spotifyObject.previous_track(deviceID)
            _ = system('clear')
            print("\033[F"*13)
            progress_bar = start_progress_bar(spotifyObject, the_playlist, running = runing, type_use=type_use)

        # Volume down
        elif the_input == '-':
            _ = system('clear')
            if volume - 10 > 0:
                volume -= 5
                spotifyObject.volume(volume, deviceID)

        # Volume Up
        elif the_input == '+':
            _ = system('clear')
            if volume + 10 < 96:
                volume += 5
                spotifyObject.volume(volume, deviceID)
        
        # shuffle option when you play a playlist
        elif the_input == 's' and (type_use == 'play_playlist' or type_use == 'my_playlist'):
            if shuffle == False:
                spotifyObject.shuffle(True, deviceID)
            else:
                spotifyObject.shuffle(False, deviceID)

        # If it's a bad input you jump up 3 line
        else:
            print("\033[F"*3)
            pass
