# Usage: For searching purposes, it might come handy to use the field "record label" (internally called studio) with text. You can do that in the plex UI
# but only for albums one by one or, if for a multitude for albums, by substituting the old text completely. With this script, you preserve the existing text
# even if you change several album fields at once. in this example, I collected albums in flac codec in a collection and added the codec to the field "record label".

# Requirements: You have to collect the albums you want to change in a collection first and insert the name of the collection below. Also, you have to change the additional text and
# complete the config.ini.

from plexapi.server import PlexServer

# read config.ini. In config.ini, insert your personal PlexUrl and PlexToken.
with open("config.ini", "r") as f:
    config = f.read()
print(config)
exec(config)

library = plex.library.section("") # fill out the name of your library
collection = library.collection("") # fill out the name of the collection the albums are in
albums = collection.items()

for album in albums:
    oldlabel = album.studio
    newlabel = f"{oldlabel} flac" # change additional text to your liking
    album.edit(**{"studio.value": newlabel})
    print(f"Changed label of album '{album.title}' from '{oldlabel}' to '{newlabel}'")