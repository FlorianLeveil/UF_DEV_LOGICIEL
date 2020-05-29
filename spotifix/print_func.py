ENDC = '\033[0m'
OKGREEN = '\033[92m'

def print_play_my_playlist(playlist_name, name_song, artist, total_time, prefix, bar, percent, suffix):
    print("\033[F"*13)
    print(
        f'{playlist_name} | {name_song} | {artist} | {total_time[:7]}',
        f'{prefix}|{OKGREEN}{bar}{ENDC}|{percent[:7]} {suffix}',
        f'',
        f'p : Pause',
        f'l : Play',
        f'+ / - : Volume',
        f's : Shuffle',
        f'n : Next Song',
        f'b : Previous Song',
        f'x : exit',
        f'',
        f'',
        sep="\n"
    )

def print_play_one_song(name_song, artist, total_time, prefix, bar, percent, suffix):
    print("\033[F"*13)
    print(
        f'{name_song} | {artist} | {total_time[:7]}',
        f'{prefix}|{OKGREEN}{bar}{ENDC}|{percent[:7]} {suffix}',
        f'',
        f'p : Pause',
        f'l : Play',
        f'+ : Up Volume',
        f'- : Down Volume',
        f'r : Add to a playlist',
        f'x : exit',
        f'',
        f'',
        f'',
        sep="\n"
    )

def print_play_playlist(playlist_name, name_song, artist, total_time, prefix, bar, percent, suffix):
    print("\033[F"*13)
    print(
        f'{playlist_name} | {name_song} | {artist} | {total_time[:7]}',
        f'{prefix}|{OKGREEN}{bar}{ENDC}|{percent[:7]} {suffix}',
        f'',
        f'p : Pause',
        f'l : Play',
        f'+ / - : Volume',
        f's : Shuffle',
        f'n : Next Song',
        f'b : Previous Song',
        f'a : Follow this playlist',
        f'x : exit',
        f'',
        sep="\n"
    )