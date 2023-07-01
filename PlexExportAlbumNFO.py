# This script exports (backups) the album review (in plex terms album.summary) and the Recording year of the album
#  (plex field: "originally AvailableAt") to an album.nfo file in the folder path. 
# For large libraries, this can take some time, be patient. 
# requires plexapi and a config.ini in the working folder and is written for windows.

import os
from plexapi.server import PlexServer

# read config.ini. In config.ini, insert your personal PlexUrl and PlexToken.
with open("config.ini", "r") as f:
    config = f.read()
print(config)
exec(config)

plex = PlexServer(PLEX_URL, PLEX_TOKEN)
albums = library.albums()

for album in albums:
    # Get the path of the first track in the album to localize the album
        track = album.tracks()[0]
        linux_path = os.path.dirname(track.media[0].parts[0].file)
        # Convert the path to Windows format
        windows_path = os.path.normpath('M:' + linux_path.replace('/mnt/music', ''))# Get the path of the first track in the album
        track = album.tracks()[0]
        # Convert the path to Windows format
        windows_path = os.path.normpath('M:' + linux_path.replace('/mnt/music', ''))
    # Create the albuminfos subfolder if it doesn't exist
        info_path = os.path.join(windows_path, 'albuminfos')
        if not os.path.exists(info_path):
            os.makedirs(info_path)
            # Create the album.nfo file with the album summary and original release date
        with open(os.path.join(info_path, 'album.nfo'), 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n')
            f.write('<album>\n')
            f.write(f'  <review>{album.summary}</review>\n')
            if album.originallyAvailableAt:
                f.write(f'  <originalreleasedate>{album.originallyAvailableAt.strftime("%Y-%m-%d")}</originalreleasedate>\n')
            f.write('</album>')