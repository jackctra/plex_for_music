"""This script assigns the same rating to all tracks in a playlist. 
It first creates a RemoteAccess.ini in the same folder as the script with your personal plex credentials for later use. You should delete this file after execution if you need to protect your data there, i.e. if this is not your machine. """


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

playlist_name = input('Enter exact name of playlist: ')

playlist = plex.playlist(playlist_name)

def get_working_folder():
    
    # Fetch path of the script
    script_path = os.path.abspath(__file__)

    # Fetch folder
    script_folder = os.path.dirname(script_path)

    return script_folder


user_input = input('Enter the rating to assign as a number between 1 and 10 (10 for full five stars, 9 for 4,5 stars and so forth):\n')
rating_to_assign = int(user_input)
for track in tqdm(playlist.items(), desc="Processing tracks...", unit="tracks", position=0, leave=True): # position and leave arguments to keep progress bar in current line and avoid scrolling
    track.rate(rating=rating_to_assign)

def main():
    
    working_folder = get_working_folder()
    os.chdir(working_folder)

main()
