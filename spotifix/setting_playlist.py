from os import system
from time import sleep 

def print_all_playlist(spotifyObject, user):
    _ = system('clear')
    all_playlist = spotifyObject.user_playlists(user["id"], limit=50)
    items = all_playlist["items"]
    compteur = 0
    print("{0:2} | {1:80} | {2:20}".format('N°', 'Name', 'Owner'))
    print(f'{"-"*112}')

    for one_playlist in items:
        print("{0:2} | {1:80} | {2:20}".format(compteur, one_playlist["name"], one_playlist["owner"]["display_name"]))
        compteur += 1
    print()
    commande = input("Enter number of playlist: ")
    commande = int(commande)
    return(items[commande])


def know_rules_playlist(the_playlist, user):
    owner_id = the_playlist["owner"]["id"]
    if owner_id == user["id"]:
        return True
    else:
        return False

def munu_playlist_setting():
    _ = system('clear')
    print('>>> What do you want to do ?')
    print()
    print("1 : Modify playlist")
    print("2 : Create a new playlist")
    print("3 : Back")
    while True:
        print()
        commande = input("Enter your choice: ")
        if commande == "1":
            return commande
        elif commande == "2":
            return commande
        elif commande == "3":
            return commande
        else:
            print("Bad input !")

def create_new_playlist(spotifyObject, user):
    _ = system('clear')
    while True:
        name = input("Enter a name for your playlist: ")
        print()
        while True:
            wanna_description = input("Do you want a description ? y/n:")
            if wanna_description == 'y' or wanna_description == 'yes':
                print()
                description = input("Write your description: ")
                break

            elif wanna_description == 'n' or wanna_description == 'no':
                description = ""
                break
            else:
                print("Bad input !")
                print()

        while True:
            public_private = input("Do you wanna a public or a private playlist ? public / private : ")
            if public_private == 'public':
                public_private = True
                break
            elif public_private == 'private':
                public_private = False
                break
            else:
                print("Bad input !")
                print()

        _ = system('clear')
        print("Your playlist name is: ",name)
        print()
        print("Your description: ", description)
        print()
        print("Your playst is ", public_private)
        print()
        while True:
            confirm = input("Did you confirm that ? y/n")
            if confirm == 'y' or confirm == 'yes':
                break
            elif confirm == 'n' or confirm == 'no':
                break
            else:
                print("Bad input !")
                print()

        if confirm == 'y' or confirm == 'yes':
            spotifyObject.user_playlist_create(user["id"],name,public_private,description)
            break
        elif confirm == 'n' or confirm == 'no':
            pass






def print_rules(spotifyObject, know_rules,the_playlist,user):
    _ = system('clear')
    if know_rules == True:
        while True:
            _ = system('clear')
            the_playlist = spotifyObject.playlist(the_playlist["id"])
            print('>>> Playlist: ', the_playlist["name"] )
            print('>>> What do you want to do ?')
            print()
            print("1 : Remove Song")
            print("2 : Change Name")
            print("3 : Change State")
            print("4 : Change Description")
            print("5 : Back")
            print()
            commande = input("Enter commande: ")

            if commande == '1':
                cancel = False
                _ = system("clear")
                all_track = spotifyObject.playlist_tracks(the_playlist["id"],limit=100)
                compteur = 0
                print("{0:2} | {1:80}".format('N°', 'Name'))
                print(f'{"-"*112}')
                for item in all_track["items"]:
                    print("{0:2} | {1:80}".format(compteur,item["track"]["name"]))
                    compteur+=1
                while True:
                    print()
                    choise_song = input("Enter number of song: ")
                    print("x : Cancel")
                    try:
                        int_choise_song = int(choise_song)
                        if int_choise_song <= compteur:
                            break
                        else:
                            print("Bad input !")
                            pass

                    except ValueError:
                        if choise_song == 'x':
                            cancel == True
                            break
                        else:
                            print("Bad input !")
                            pass
                if cancel == False:
                    the_track = [all_track["items"][int_choise_song]["track"]["id"]]
                    spotifyObject.user_playlist_remove_all_occurrences_of_tracks(user["id"],the_playlist["id"],the_track)
                    sleep(0.1)

            elif commande == '2':
                print()
                new_name = input("Enter your new name: ")
                spotifyObject.user_playlist_change_details(user["id"],the_playlist["id"],name=new_name)
                sleep(0.2)
                _ = system("clear")
            elif commande == '3':
                print()
                print("Your state is public:", the_playlist["public"])
                while True:
                    print()
                    change_state = input("Do you wanna change ? y/n  ")
                    if change_state == 'y' or change_state == 'yes':
                        if the_playlist["public"] == True:
                            spotifyObject.user_playlist_change_details(user["id"],the_playlist["id"],public=False)
                            sleep(0.2)
                        else:
                            spotifyObject.user_playlist_change_details(user["id"],the_playlist["id"],public=True)
                            sleep(0.2)

                        break
                    elif change_state == 'n' or change_state == 'no':
                        break
                    else:
                        print("Bad input !")
                        print()
                
            elif commande == '4':
                if the_playlist["description"] == '':
                    print("Your description is empty !")

                else:
                    print("Your description:")
                    print(the_playlist["description"])
                
                while True:
                    print()
                    change_description = input("Do you wanna change ? y/n")

                    if change_description == 'y' or change_description == 'yes':
                        print()
                        change_description2 = input("Enter your description: ")
                        spotifyObject.user_playlist_change_details(user["id"],the_playlist["id"],description=change_description2)
                        sleep(0.2)
                        break
                    elif change_description == 'n' or change_description == 'no':
                        break
                    else:
                        print("Bad input !")
                        print()
            elif commande == '5':
                break
            else:
                _ = system('clear')
                print("Bad input !")
                print()


    else:
        while True:
            print('>>> Playlist: ', the_playlist["name"] )
            print('>>> What do you want to do ?')
            print()
            print("1 : UnFollow playlist")
            print("2 : Add a song to another playlist: ")
            print("3 : Back")
            print()
            commande = input("Enter commande: ") # and play the song           
            if commande == '1':
                spotifyObject.user_playlist_unfollow(user["id"],the_playlist["id"])
                break
            elif commande == '2':
                _ = system("clear")
                all_track = spotifyObject.playlist_tracks(the_playlist["id"],limit=None)
                compteur = 0
                print("{0:2} | {1:80}".format('N°', 'Name'))
                print(f'{"-"*112}')
                for item in all_track["items"]:
                    print("{0:2} | {1:80}".format(compteur,item["track"]["name"]))
                    compteur+=1
                while True:
                    print()
                    choise_song = input("Enter number of song: ")
                    try:
                        int_choise_song = int(choise_song)
                        if int_choise_song <= compteur:
                            break
                        else:
                            print("Bad input !")
                            pass

                    except ValueError:
                        print("Bad input !")
                        pass
                while True:
                    playlist_to_set = print_all_playlist(spotifyObject, user)
                    know_rules = know_rules_playlist(playlist_to_set, user)
                    if know_rules == True:
                        the_track = [all_track["items"][int_choise_song]["track"]["id"]]
                        spotifyObject.user_playlist_add_tracks(user["id"],playlist_to_set["id"],the_track)
                        _ = system("clear")
                        break
                    else:
                        print()
                        print("You are not the owner of this playlist !")
                        print()
                        pass


            elif commande == '3':
                break
            else:
                _ = system('clear')
                print("Bad input !")
                print()



