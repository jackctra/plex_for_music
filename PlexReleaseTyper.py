'''This code writes the Releasetag to the tags of one or more album's tracks and refreshes the album(s) in plex so that the plex database is also updated.
	NEW in V0.2: code to check and fix several albums.
Change filepaths to your music files and to the configfile as needed'''

from plexapi.server import PlexServer, CONFIG
import os
from mutagen.id3 import ID3, TXXX
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
import configparser

# 2. Identify current folder as working folder
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)


config = configparser.ConfigParser()


# config_file_path = os.path.join(os.pardir, '..', 'Z helperfiles', 'Plexconfig.ini') # if in grandparentfolder
config_file_path = os.path.join(os.pardir, 'Z helperfiles', 'Plexconfig.ini') # if in parentfolder
# config_file_path = os.path.join('Z helperfiles', 'Plexconfig.ini') # if in same folder
if os.path.exists(config_file_path):
    config.read(config_file_path)
else:
    # If config not set, enter 
    plexurl = input('Enter Plex URL (example: http://192....32400): ')
    token = input('Enter token: ')
    library = input('Enter name of music library: ')

    # save to config.file
    config['plex'] = {
        'plexurl': plexurl,
        'token': token,
        'library': library
    }
    os.makedirs('Z helperfiles', exist_ok=True)
    with open(config_file_path, 'w') as f:
        config.write(f)

# Read from Plexconfig.ini    
plexurl = config.get('plex', 'plexurl')
token = config.get('plex', 'token')
library = config.get('plex', 'library')

# connect to plex
plex = PlexServer(plexurl, token)
# define library
library = plex.library.section(library)  # necessary conversion from the string

plex = PlexServer(plexurl, token)
library = plex.library.section("Musik")

def ask_user():
    releasetype = input("Choose releasetype-category: 'c' for album compilation, 'l' for live album, 's' for single or EP:\n")
    return releasetype

def convert_path(linux_path):
    file_path = os.path.normpath('M:' + linux_path.replace('/mnt/music', ''))
    return(file_path)

def convert_releasetype(releasetype):
    if releasetype == 'c':
        release_type = 'album;compilation'
        
    if releasetype == 'l':
        release_type = 'album;live'
        
    if releasetype == 's':
        release_type = 'single'
    return release_type

def check_items(albums_to_check):
    albums_to_tag = []  # Initialize an empty list to store albums to tag
    for album in albums_to_check:
        print(f"Checking album: {album.title} ({album.parentTitle})")
        tag_missing = False  # Flag to indicate if RELEASETYPE tag is missing in any track of the album
        for track in album.tracks():
            # Determine the file type of the track
            if track.media[0].parts[0].file:
                file_path = track.media[0].parts[0].file
                file_path = convert_path(file_path)
                file_extension = file_path.split('.')[-1].lower()

                # Check if the file type is supported (mp3, flac, mp4)
                if file_extension in ['mp3', 'flac', 'mp4']:
                    # Load the metadata of the track
                    if file_extension == 'mp3':
                        audio = MP3(file_path)
                    elif file_extension == 'flac':
                        audio = FLAC(file_path)
                    elif file_extension == 'mp4' or 'm4a':
                        audio = MP4(file_path)

                    # Check if RELEASETYPE tag is missing
                    if 'RELEASETYPE' not in audio:
                        # print(f"RELEASETYPE tag missing in track: {track.title}")
                        tag_missing = True
                else:
                    print(f"Unsupported file format: {file_extension} for track: {track.title}")
            else:
                print(f"No file path found for track: {track.title}")

def check_items(albums_to_check):
    albums_to_tag = []  # Initialize an empty list to store albums to tag
    for album in albums_to_check:
        print(f"Checking album: {album.title} ({album.parentTitle})")
        if album.parentTitle == "Various Artists":
            print("Various Artists compilation, not processed")
            continue
        tag_missing = False  # Flag to indicate if RELEASETYPE tag is missing in any track of the album
        for track in album.tracks():
            # Determine the file type of the track
            if track.media[0].parts[0].file:
                file_path = track.media[0].parts[0].file
                file_path = convert_path(file_path)
                file_extension = file_path.split('.')[-1].lower()

                # Check if the file type is supported (mp3, flac, mp4)
                if file_extension in ['mp3', 'flac', 'mp4']:
                    # Load the metadata of the track
                    if file_extension == 'mp3':
                        audio = MP3(file_path)
                    elif file_extension == 'flac':
                        audio = FLAC(file_path)
                    elif file_extension == 'mp4' or 'm4a':
                        audio = MP4(file_path)

                    # Check if RELEASETYPE tag is missing
                    if 'RELEASETYPE' not in audio and 'TXXX:releasetype' not in audio:
                        print(f"RELEASETYPE tag missing in track: {track.title}")
                        tag_missing = True
                else:
                    print(f"Unsupported file format: {file_extension} for track: {track.title}")
            else:
                print(f"No file path found for track: {track.title}")

        # If RELEASETYPE tag is missing in any track of the album
        if tag_missing:
            print("RELEASETYPE tag missing.")
            while True:
                add_album = input(f"Do you want to add the album '{album.title}' ({album.parentTitle}) to the list to tag? (yes/no): ").lower()
                if add_album == 'y':
                    albums_to_tag.append(album)
                    break  # Exit the loop and proceed to the next album
                elif add_album == 'n':
                    break  # Exit the loop and proceed to the next album
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

    return albums_to_tag

    return albums_to_tag


def categorize(release_type, file_path):
    if file_path.endswith('.mp3'):
        audio = MP3(file_path, ID3=ID3)
        for tag in audio.tags.getall("TXXX:RELEASETYPE"):
            del audio["TXXX:RELEASETYPE"]
            audio.save()
        audio.tags.add(TXXX(encoding=3, desc="releasetype", text=release_type))
        audio.save()
    elif file_path.endswith('.flac'):
        audio = FLAC(file_path)
        audio["releasetype"] = release_type
        audio.save()
    elif file_path.endswith('.mp4') or file_path.endswith('.m4a'):
        audio = MP4(file_path)
        if "----:com.apple.iTunes:RELEASETYPE" in audio:
            del audio["----:com.apple.iTunes:RELEASETYPE"]
            audio.save()
        audio["----:com.apple.iTunes:releasetype"] = [release_type.encode('utf-8')]
        audio.save()
    else:
        print("Unknown format:", file_path)

def loop_thru_albums(album, releasetype): 
    tracks = album.tracks()
    for track in tracks:
        if track.media and track.media[0].parts:
            file_path = track.media[0].parts[0].file
            if os.name == 'nt':
                file_path = convert_path(file_path)
            release_type = convert_releasetype(releasetype)
            categorize(release_type, file_path) 

    # refresh album metadata in plex
    album.refresh()

releasetype = ask_user()

inp = input("Enter album title:\n")
tq = library.search(inp, libtype="album")

# Check if any albums were found
if not tq:
    print("No album found.")
else:
    # If more than one album is found, prompt the user to choose the correct one
    if len(tq) > 1:
        print("More than one album found, please choose a number to fix one album or 'l' to list all")
        for idx, album in enumerate(tq, start=1):
            print(f"{idx}. {album.title} ({album.parentTitle})")
        selection = input("Please enter the number of the correct album or 'l' for loop through all albums: ")
        if selection.isdigit() and 1 <= int(selection) <= len(tq):
            tq = [tq[int(selection) - 1]]
            album = tq[0]
            loop_thru_albums(album, releasetype)
        elif selection.lower() == 'l':
            # create a list with all items for further checks
            albums_to_tag = check_items(tq)
            for album in albums_to_tag:
                loop_thru_albums(album, releasetype)

        else:
            print("Invalid input, please enter a valid number.")
            

       
print("Any key to exit")
exit()
