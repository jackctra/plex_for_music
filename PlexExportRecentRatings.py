# This script exports user ratings given in the last days,weeks or months from plex into the tags of the pertinent mp3-,flac and m4a-files. 
# NEW: In this version (0.2) the user can decide what to do with unsupported formats like .ape
# You have to install necessary requirements, prepare a config.ini and modify the filepaths according to your setup. Check if your software uses a different rating approach than mediamonkey, adapt if necessary. 

import plexapi
from plexapi.server import PlexServer
import re
import os
import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

# Connect to the plex server
with open("config.ini", "r") as f:
    config = f.read()
print(config)
exec(config)
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# Define the subset based on user input
timespan = input("The ratings of which timespan back from now are to be exported? (2d, 1w, 2w, 1m): ")

# Define the filter based on the timespan
if timespan == "2d":
    subset = library.search(filters={'track.lastRatedAt>>': '2d'}, libtype='track') 
elif timespan == "1w":
    subset = library.search(filters={'track.lastRatedAt>>': '1w'}, libtype='track') 
elif timespan == "2w":
    subset = library.search(filters={'track.lastRatedAt>>': '2w'}, libtype='track', limit=500) 
elif timespan == "1m":
    subset = library.search(filters={'track.lastRatedAt>>': '1mon'}, libtype='track', limit=500)
else:
    print("Invalid timespan entered.")
    exit()

print(f"{subset} are in the subset.")
print(f"There are {len(subset)} tracks in the subset.No limit set.")

# Loop through the tracks in the subset
for track in subset:
    if track.userRating is None:
        continue
    # Get the rating from the plex database
    rating = track.userRating

    # Write the rating to the tag of the file with mutagen
    linux_path_file = track.media[0].parts[0].file
    # Convert the path to Windows format - only necessary if different os
    windows_path_file = os.path.normpath(r'M:' + linux_path_file.replace('/mnt/music', '')) # adapt the root of the path according to your setup

    # Get the file extension from the linux path
    file_ext = os.path.splitext(linux_path_file)[1]

    # Load the audio file according to its format
    if file_ext == ".flac":
        rating = int(rating * 10) # to make rating compatible with MediaMonkey, can be different with other software
        audio = FLAC(windows_path_file)
        # Use a custom tag for flac files
        audio["rating"] = str(rating)
    elif file_ext == ".mp3":
        ratingvalue = int(rating * 25.5) # to make rating compatible with MediaMonkey, can be different with other software
        audio = MP3(windows_path_file)
        # Use POPM tag for mp3 files
        audio["POPM"] = mutagen.id3.POPM(email="", rating=ratingvalue, count="")
    elif file_ext == ".m4a":
        ratingvalue = int(rating * 10) # to make rating compatible with MediaMonkey, can be different with other software
        audio = MP4(windows_path_file)
        # Use rate tag for mp4 files
        audio["rate"] = str(ratingvalue)
    else:
        # Unsupported format
        # Print the error message
        print(f"The format of {linux_path_file} is unsupported.")
        choice = input(" Do you want to stop the script (s) or continue (c) with the next item? ")
        if choice == "s":
            # Stop the execution
            break
        elif choice == "c":
            # Continue with the next item
            continue
        else:
            # Invalid input
            print("Invalid choice. Please enter s or c.")

    # Save the changes to the file
    audio.save()
