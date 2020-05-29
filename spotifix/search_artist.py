def search_artist(spotifyObject, deviceID):
    print()
    searchQuery = input("Ok, what's their name?: ")
    print()

    # Get search results
    searchResults = spotifyObject.search(searchQuery,1,0,"artist")

    # Artist details
    artist = searchResults['artists']['items'][0]
    print(artist['name'])
    print(str(artist['followers']['total']) + " followers")
    print(artist['genres'][0])
    print()
    artistID = artist['id']


    # Album and track details
    trackURIs = []
    trackArt = []
    z = 0

    # Extract album data
    albumResults = spotifyObject.artist_albums(artistID)
    albumResults = albumResults['items']

    for item in albumResults:
        print("ALBUM: " + item['name'])
        albumID = item['id']
        albumArt = item['images'][0]['url']

        # Extract track data
        trackResults = spotifyObject.album_tracks(albumID)
        trackResults = trackResults['items']

        for item in trackResults:
            print(str(z) + ": " + item['name'])
            trackURIs.append(item['uri'])
            trackArt.append(albumArt)
            z+=1
        print()

    return(trackURIs)