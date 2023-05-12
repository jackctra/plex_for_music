from plexapi.server import PlexServer

 # read config.ini. In config.ini, you have to insert your personal PlexUrl and PlexToken.
with open("config.ini", "r") as f:
    config = f.read()
print(config)
exec(config)

library = plex.library.section("") # You have to fill out the name of your library
library.lockAllField("studio", libtype="album")
print ("Locked the studio field for all albums in music library")
