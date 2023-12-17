"""This script allows to add a mood to all tracks in a playlist. """


from plexapi.server import PlexServer
import os
import configparser
from plexapi.myplex import MyPlexAccount
from tqdm import tqdm # library for progress bar


config = configparser.ConfigParser()
if os.path.exists('PlexRemoteAccess.ini'):
    config.read('PlexRemoteAccess.ini')
else:
    # If config not set, enter 
    username = input('Enter username: ')
    password = input('Enter password: ')
    server_name = input('Enter name of server: ')
    library = input('Enter name of music library: ')

    # save to config.file
    config['plex'] = {
        'username': username,
        'password': password,
        'server_name': server_name,
        'library': library
    }
    with open('PlexRemoteAccess.ini', 'w') as f:
        config.write(f)

# Read from PlexRemoteAccess.ini    
username = config.get('plex', 'username')
password = config.get('plex', 'password')
server_name = config.get('plex', 'server_name')
library = config.get('plex', 'library')

# connect to plex
account = MyPlexAccount(username, password)
plex = account.resource(server_name).connect()

playlist_name = input('Enter name of playlist: ')

playlist = plex.playlist(playlist_name)

def get_working_folder():
    
    # Fetch path of the script
    script_path = os.path.abspath(__file__)

    # Fetch folder
    script_folder = os.path.dirname(script_path)

    return script_folder


if input("Do you want to print a list of the tracks with their current moods first? (Y/n)?") in ('y', 'Y', 'j', 'J'):
    print('Current moods in playlist:')
    for track in playlist.items():
        mood_strings = [str(mood) for mood in track.moods]
        print(f"{track.title}: {', '.join(mood_strings)}")
else:
    pass


mood_to_add = input('Enter the mood to add: ')

for track in tqdm(playlist.items(), desc="Processing tracks...", unit="tracks", position=0, leave=True): # position and leave arguments to keep progress bar in current line
    track.addMood(mood_to_add, locked=True)

def main():
    
    working_folder = get_working_folder()
    os.chdir(working_folder)

main()
