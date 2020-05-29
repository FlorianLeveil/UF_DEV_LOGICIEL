OKBLUE = '\033[94m'
ENDC = '\033[0m'

def search_playlist(spotifyObject, deviceID):
    print()
    searchQuery = input("Ok, what's their name?: ")
    print()

    # Get search results
    searchResults = spotifyObject.search(searchQuery,50,0,"playlist")
 
    i = 0

    print(f'{OKBLUE}{"-"*126}{ENDC}')
    print("{3}|{4}{0:3} {3}|{4} {2:4} {3}|{4} {1:110} {3}|{4}".format('N°', 'Name', 'Numb',OKBLUE,ENDC))
    print(f'{OKBLUE}{"-"*126}{ENDC}')

    #Print all playlist
    for item in searchResults["playlists"]["items"]:
        if item == []:
            break
        print("{3}|{4}{0:3} {3}|{4} {2:4} {3}|{4} {1:110} {3}|{4}".format(i, item["name"], item["tracks"]["total"],OKBLUE,ENDC))
        print(f'{OKBLUE}{"-"*126}{ENDC}')
        i+= 1
    print()

    while True:
        playlistSelection = input("Enter a playlist number for play the playlist (x to exit): ")
        try:
            playlistSelection = int(playlistSelection)

            if playlistSelection < 50:
                return(searchResults["playlists"]["items"][playlistSelection])
            else:
                print("Less than 50 please.")

        except ValueError:

            if playlistSelection =='x':
                return(None)
            else:
                print("Bad input")
                pass

