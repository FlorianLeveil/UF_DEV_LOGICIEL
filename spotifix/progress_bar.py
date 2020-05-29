import datetime
import threading
import sys
import spotipy

from time import sleep
from os import system
from print_func import print_play_my_playlist, print_play_one_song, print_play_playlist

# print the progressBar
def printProgressBar (iteration, total, artist, total_time1, name_song=None,playlist_name=None, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r", type=None):

    #Calcul for the size of the progress bar
    percent = str(datetime.timedelta(seconds=iteration))
    total_time = str(datetime.timedelta(milliseconds=total_time1))
    filledLength = int(length * (iteration) // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    # print the progressBar and function type op play (playlist,song,myplaylist).
    if type == 'my_playlist':
        print_play_my_playlist(playlist_name, name_song, artist, total_time, prefix, bar, percent, suffix)
    elif type == 'play_one_song':
        print_play_one_song(name_song, artist, total_time, prefix, bar, percent, suffix)
    elif type == 'play_playlist':
        print_play_playlist(playlist_name, name_song, artist, total_time, prefix, bar, percent, suffix)

    if iteration+1 == total: 
        return False


#thread progress bar
class thread_progress_bar (threading.Thread):
    def __init__(self, total, playlist=None, artist=None, album=None, total_time1=None, name_song=None, spotifyObject=None, ms_now=None, deviceID=None, type_use=None):
        threading.Thread.__init__(self)
        self.i = 0
        self.playlist_object = playlist
        if self.playlist_object != None:
            self.name = self.playlist_object["name"]
        else:
            self.name = ''
        if ms_now == None:
            self.ms_now = 0
        else:
            self.ms_now = ms_now
        self.spotifyObject = spotifyObject
        self.name_song = name_song
        self.artist = artist
        self.album = album
        self.deviceID = deviceID
        self.total_time1 = total_time1
        self.items = list(range(0, (total*10)))
        self.max_items = len(self.items)
        self.etat = True
        self.paused = False
        self.type = type_use
        self.the_time = 0

    def run(self):
        print("\n"*12, end="")
        for self.i in self.items:
            if self.etat == True:
                sleep(0.1)
                the_progress_bar = printProgressBar((self.i +self.ms_now)/10, self.max_items/10, self.artist, self.total_time1, name_song=self.name_song, playlist_name=self.name, prefix = 'Progress:', suffix = 'Complete', length = 70, type=self.type)
                global runing
                if runing == False:
                    break
                if self.paused == True:
                    self.etat = False
                if the_progress_bar == False:
                    _ = system("clear")
                    start_progress_bar(self.spotifyObject, kill=True)
                    break
            if self.etat == False:
                while self.paused == True:
                    sleep(0.1)
                    if runing == False:
                        break
                    if self.paused == False:
                        self.etat = True
                        break
                if runing == False:
                    break

    def paused_x(self, current_track, single_track, trackSelectionList=None):
        if self.paused == True:
            position_track = int(current_track['progress_ms'])
            if single_track == False:
                self.spotifyObject.start_playback(self.deviceID,current_track["context"]["uri"],offset={"uri": current_track["item"]["uri"]},position_ms=position_track)
            else:
                self.spotifyObject.start_playback(self.deviceID,None,trackSelectionList,position_ms=position_track)

            self.paused = False

        else:
            self.paused = True


#kill the thread
def runing_false():
    global runing
    runing = False


def start_progress_bar(spotifyObject, playlist=None, kill=None, running=None, type_use=None):
    global runing

    if kill == True:
        runing = False
        sleep(0.5)
        _ = system('clear')
        runing = True

    if running == False:
        runing = True

    current_track = spotifyObject.current_playback()
    time_track_str = str(current_track["item"]["duration_ms"])
    time_track_concat = time_track_str[:-3]
    items = list(range(0,int(time_track_concat)))
    total = len(items)

    artists = current_track["item"]["artists"]
    artist = ''
    name_song = current_track["item"]["name"]
    for one_artist in artists:
        artist += ' ' + one_artist["name"]
    ms_now_str = str(current_track['progress_ms'])
    ms_now = int(ms_now_str[:-2])
    progress_bar = thread_progress_bar(total, playlist=playlist,name_song=name_song, artist=artist, total_time1=int(time_track_str), spotifyObject=spotifyObject, ms_now=ms_now, type_use=type_use)
    progress_bar.start()
    return progress_bar
