# This script exports plex user ratings to the tags in the pertinent files of one album or a range of albums identified by their first letter or number. You can
# specify an album name or the beginning of album name(s) OR
# specify a range of first characters with  an arrow "->"" and everything inbetween will be processed (A->C)
# But:
# Regex cannot recognize the alphabetical order of strings. Therefore you cannot start or end a range with a string of characters. 
# Also for albums beginning with special characters, a range is not possible. You have to process them seperately. Moreover some, as '+' will not work if not as the first letter of a string (i.e. +justments)
# This version 0.2 includes a progress bar, lets user decide what to do with unsupported formats like ape and decapitalizes file endings to avoid errors if the ending is written with capital letters.
# Before Usage install necessary requirements, create a config.ini and adapt the filepaths according to your setup (here the plex server runs on linux wheras the script is executed on a windows PC. You can probably skip some steps if you are running the script on the same machine)
# Check if your software uses a different rating approach than mediamonkey. If so, adapt lines accordingly.
  
import plexapi
from plexapi.server import PlexServer
import re
import os
import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from tqdm import tqdm # library for progress bar
import json

# Connect to the plex server
with open("config.ini", "r") as f:
    config = f.read()
print(config)
exec(config)
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# Ask the user to specify the subset of albums
print("The track ratings of which albums should be exported to its ID3-tags?")
print("Specify by typing either a number, letter or special character the albums to be processed begin with or a range with an arrow inbetween (ranges of letters or numbers, i.e. \"A->D\"):")
user_input = input()

# Check if the user input contains '->'
if '->' in user_input:
    start, end = user_input.split('->')
    
    # If the start and end are single digits or letters, create a range pattern
    if (start.isdigit() and end.isdigit()) or (start.isalpha() and end.isalpha()):
        regex = "^[" + start + "-" + end + "].*"
    else:
        # Convert the start and end into regex patterns
        start = "^" + re.escape(start) + ".*"
        end = "^" + re.escape(end) + ".*"
        
        # The final regex pattern will match anything that starts with the start pattern
        # and ends with the end pattern
        regex = "(" + start + "|" + end + ")"
else:
    # If the user input does not contain '->', proceed as before
    regex = re.escape(user_input) # Escape all special characters
    regex = "^" + regex # Add a start anchor
    regex = regex + ".*" # Add a dot star at the end

print(regex)

input("Press any key to continue...")


# Get the subset of albums that match the regex
subset = [album for album in library.albums() if re.match(regex, album.title)]

# Load the processed set from a file or create an empty set
try:
    with open("processed.json", "r") as f:
        processed = set(json.load(f))
except FileNotFoundError:
    processed = set()

# Loop through the tracks in the subset
for album in tqdm(subset):
    for track in album.tracks():
        # Skip the track if it has been processed
        if track.ratingKey in processed:
            continue
        if track.userRating is None:
            continue
        # Get the rating from the plex database
        rating = track.userRating

        # Write the rating to the tag of the file with mutagen
        linux_path_file = track.media[0].parts[0].file
        # Convert the path to Windows format - conversion only necessary if os differs
        windows_path_file = os.path.normpath(r'M:' + linux_path_file.replace('/mnt/music', '')) # adapt root to your setup

        # Get the file extension from the linux path
        file_ext = os.path.splitext(linux_path_file)[1]

        # Load the audio file according to its format
        if file_ext.lower() == ".flac":
            rating = int(rating * 10) # to make rating compatible with MediaMonkey, might have to be changed if you use other software.
            audio = FLAC(windows_path_file)
            # Use a custom tag for flac files
            audio["rating"] = str(rating)
        elif file_ext.lower() == ".mp3":
            ratingvalue = int(rating * 25.5) # to make rating compatible with MediaMonkey, might have to be changed if you use other software.
            audio = MP3(windows_path_file)
            # Use POPM tag for mp3 files
            audio["POPM"] = mutagen.id3.POPM(email="", rating=ratingvalue, count="")
        elif file_ext.lower() == ".m4a":
            ratingvalue = int(rating * 10) # to make rating compatible with MediaMonkey, might have to be changed if you use other software.
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
        tqdm.write(f" Currently processing {linux_path_file}")
        audio.save()

        # Add the track to the processed set and save it to a file
        processed.add(track.ratingKey)
        with open("processed.json", "w") as f:
            json.dump(list(processed), f)
