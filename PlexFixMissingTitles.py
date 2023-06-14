# The script fixes missing track titles by fetching them from the filename.

from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
import time
import msvcrt

baseurl = 'http://xxx.xxxx.xxx.xx:32400'
token = 'xxxxxxxxxx'

plex = PlexServer(baseurl, token)

music_section = plex.library.section('xxxx')
tracks = music_section.searchTracks()

no_title_tracks = [track for track in tracks if not track.title]

print("The following tracks have no titles:")
for track in no_title_tracks:
    filepath = track.media[0].parts[0].file
    print(filepath.split('/')[-2] + '/' + filepath.split('/')[-1])

fix_tracks = input("Do you want to fix them (y/n)? ")

if fix_tracks.lower() == 'y':
    for track in no_title_tracks:
        filepath = track.media[0].parts[0].file
        filename = filepath.split('/')[-1]
        suggested_title = filename.split('-')[-1].split('.')[0]
        print(f"{filepath.split('/')[-2]}/{filename} is without a title. Do you want me to correct it to {suggested_title} (y/n or wait)?")
        user_input = ''
        start_time = time.time()
        while time.time() - start_time < 8:
            if msvcrt.kbhit():
                user_input = msvcrt.getch().decode()
                break
            time.sleep(1)
        
        if user_input == 'y' or user_input == '':
            track.edit(**{'title.value': suggested_title, 'title.locked': 1})
            print(f"Title fixed: title now is: {suggested_title}")
        elif user_input == 'n':
            new_title = input("Enter new title: ")
            track.edit(**{'title.value': new_title, 'title.locked': 1})
            print(f"Title fixed: title now is: {new_title}")
    print("All titles fixed.")
