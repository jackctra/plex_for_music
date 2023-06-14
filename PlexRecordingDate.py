#  Plex notes the Release Date of Recordings. However, it is much more useful to have the recording date at hand. With this script, it is possible to update the Release date field of albums in a given collection by comparing the plex entry with a discogs entry or by searching in allmusic.com. Recordings which have been checked get a mood tag to ensure that they do not come up again. 

# Requirements: You have to install plexapi and discogs_client (pip install python3-discogs-client)
# Requirements: You have to collect the albums you want to change in a collection first. 
# The remove flac block is only necessary if you have flac recordings with a pertinent album title. 
# Complete config.ini and config_discogs.ini and put them in the working folder.



# 0. Basics
from plexapi.server import PlexServer
import tqdm
# read config.ini. In config.ini, insert your personal PlexUrl and PlexToken.
with open("config.ini", "r") as f:
    config = f.read()
print(config)
exec(config)

# library = plex.library.section("") # fill out the name of your library if not already in config.ini

# Initialize the possibility to add -h and -n flags
import argparse
parser = argparse.ArgumentParser("""To update The YEAR in plex by comparing it with discogs entries.\nIn the case of Greatest Hits Compilations, it is better to use a proxy for the decennial, the tracks had been recorded.\n\nRequirements: \n- You have to install plexapi and discogs_client (pip install python3-discogs-client)\- You have to collect the albums you want to change in a collection first. You may want to use filtering, i.e. collect only those albums with Artists beginning with "A"\nand excluding those the accuratenes of the year has already been checked - that is achieved by excluding albums with the mood tag ".yearchecked".\n- Complete config.ini and config_discogs.ini and put them in the working folder.\n- Insert the name of the collection either by flagging it in the command line with -n r by typing it later. """)
parser.add_argument('-n', '--name', help='Name of the collection', default='')
args = parser.parse_args()

if args.name:
    collection_name = args.name
    print(f"Collection name: {collection_name}")
else:
    # ask user for collection name and define collection_name as collection class, not as string.       
    collection_name = input("Enter collection name: ")
    # handle wrong input (not implemented because missing: def collection_exists(collection_name):)
    # while not collection_exists(collection_name):
    #     print("The name of the collection does not exist in Plex. Do you want to enter again?")
    #     collection_name = input("Enter the name of the Plex collection: ")
        
    print(f"Collection name: {collection_name}")

collection = library.collection(collection_name)
albums = collection.items()

for album in albums:
    oldlabel = album.year
    # oldOA = album.originallyAvailableAt
    print(f"The year of album '{album.title}' by '{album.parentTitle}' in Plex is '{oldlabel}'.")
    # define 

import discogs_client
import webbrowser
import pyautogui


# read config.ini. In config.ini, you have to insert your personal PlexUrl and PlexToken.
with open("config_discogs.ini", "r") as f:
    config = f.read()
print("connect to discogs...")
exec(config)

# Initialize an empty list to store the results
results_list = []

# Initialize an empty dictionary to store the album titles
album_titles = {}

# Initialize a counter for the number of albums with changes
num_changes = 0
# Initialize empty lists to store the albums with and without deviations
deviating_albums = []
nondeviating_albums = []
updated_albums = []

# 1. Get the Data
# 1.1. Data from Plex
# Loop through each album
tq = tqdm.tqdm
for album in tq(albums):
    artist = album.parentTitle
    album_title = album.title

    # Check if the album title ends with "flac"
    if album_title.lower().endswith("flac"):
        # Remove "flac" from the end of the album title
        discogs_album_title = album_title[:-4].strip()
    else:
        discogs_album_title = album_title

    # Store the album titles in the dictionary
    album_titles[album_title] = discogs_album_title

# 1.2 Data from Discogs
    # 1.2.1 Search for the release on Discogs using the modified album title 
    results = discogs.search(f"{artist} {discogs_album_title}", type="release")

    # 1.2.2.Check if results were found
    if results:
        release = results[0]
    # 1.2.3. test - Check if results are valid
        # if release.year is not None:
        if release.year is not None and release.year != 0:
            newlabel_int = int(release.year)
        else:
        # Handle the case where release.year in Discogs is not assigned
            newlabel_int = 1110

        # Initialize a flag to track if any album has been updated
        album_updated = False

        # Handle the case where album.year in Plex is not assigned
        if album.year:
            oldlabel_int = album.year
        else:
            oldlabel_int = 1111

        # 2. Compare the old and new labels and update
        # 2.0 Create a dictionary for Block 3
        newnewlabel_dict = {}
        # 2.1. if identical
        if oldlabel_int == newlabel_int:
        
            result_str = f"'{artist}' - '{album_title}': Identical year: {oldlabel_int}. Do you want to correct anyway (ie for compilations? Enter year (yyyy),'p' to skip or search with 's' in allmusic: "
            user_input = input(result_str)
            # 2.1.1 no correction (p)
            if user_input.lower() == "p" or user_input == "":
                album.addMood([".yearchecked"], locked=True)
                nondeviating_albums.append(album)
            # 2.1.2 search loop (s)
            elif user_input.lower() == "s":
                # Open web browser and search for album on allmusic.com
                # search_url = f"https://www.allmusic.com/search/albums/{artist}+{discogs_album_title}"
                search_url = f"https://www.allmusic.com/search/albums/{discogs_album_title}"
                webbrowser.open(search_url)
                # Prompt user again for input
                result_str = f"Enter year (yyyy) to change to discogs or any other year, or 'p' to skip: "
                user_input = input(result_str)
                # close the webbrowser tab
                pyautogui.hotkey('alt', 'tab')
                pyautogui.hotkey('ctrl', 'w')
                pyautogui.hotkey('alt', 'tab')
                # 2.1.2.1 manual correction after search
                # if user_input.lower() != "p": ersetzt durch
                if user_input.isdigit():
                    newlabel = user_input
                    newlabel_int = int(newlabel)
                    deviating_albums.append(album)
                    num_changes += 1
                    album_updated = True
                    tq.write(f"{album.title} by {album.artist().title} will be updated")    
                    # 2.1.2.1.1. Convert newlabel to Plex format
                    newlabel_plex = f"{newlabel}-12-31"
                    # 2.1.2.1.2. Update album variables
                    album.edit(**{"originallyAvailableAt.value": newlabel_plex, "originallyAvailableAt.locked": 1})
                    album.edit(**{"year.value": newlabel, "year.locked": 1})
                    updated_albums.append(album)
                    newnewlabel_dict[album] = newlabel
                    # 2.1.2.1.3. update album moods with identifier ".yearchecked"
                    album.addMood([".yearchecked"], locked=True)
                    tq.write(f"The years of '{album.title}' by '{artist}' have been updated to {user_input}.")
                    # 2.1.2.2 after search do nothing: back to 2.1.1.
                else:
                    album.addMood([".yearchecked"], locked=True)
                    nondeviating_albums.append(album)


            # 2.1.3 manual correction the first time around (yyyy)
            elif user_input.isdigit():
                newlabel = user_input
                newlabel_int = int(newlabel)
                deviating_albums.append(album)
                num_changes += 1
                album_updated = True
                tq.write(f"{album.title} by {album.artist().title} will be updated")    
                # 2.1.2.1.1. Convert newlabel to Plex format
                newlabel_plex = f"{newlabel}-12-31"
                # 2.1.2.1.2. Update album variables
                album.edit(**{"originallyAvailableAt.value": newlabel_plex, "originallyAvailableAt.locked": 1})
                album.edit(**{"year.value": newlabel, "year.locked": 1})
                updated_albums.append(album)
                newnewlabel_dict[album] = newlabel
                # 2.1.2.1.3. update album moods with identifier ".yearchecked"
                album.addMood([".yearchecked"], locked=True)
                tq.write(f"The years of '{album.title}' by '{artist}' have been updated to {user_input}.")
            
            # 2.2 if not identical
        else:
            result_str = f"'{album_title}' by '{artist}' in Plex is: {oldlabel_int} , Discogs differs: {newlabel_int}. Do you want to update to Discogs (D), enter a new year (yyyy), skip (p)? or search first (s)"
            user_input = input(result_str)
            # 2.2.1 Update with Discogs year (d)
            if user_input.lower() == "d" or user_input == "":
                newlabel = str(newlabel_int)
                deviating_albums.append(album)
                num_changes += 1
                album_updated = True
                tq.write(f"{album.title} by {album.artist().title} will be updated")
                # 2.2.1.1. Convert newlabel to Plex format
                newlabel_plex = f"{newlabel}-12-31"
                # 2.2.1.2. Update album variables
                album.edit(**{"originallyAvailableAt.value": newlabel_plex, "originallyAvailableAt.locked": 1})
                album.edit(**{"year.value": newlabel, "year.locked": 1})
                updated_albums.append(album)
                newnewlabel_dict[album] = newlabel
                # 2.2.1.2.1.
                # enter code to update album moods with identifier ".yearchecked"
                album.addMood([".yearchecked"], locked=True)
                tq.write(f"The years of '{album.title}' by '{artist}' have been updated.")

            # NEW CODE
            # 2.1.1 no correction (p)
            elif user_input.lower() == "p":
                album.addMood([".yearchecked"], locked=True)
                nondeviating_albums.append(album)
            # 2.1.2 search loop (s)
            elif user_input.lower() == "s":
                # Open web browser and search for album on allmusic.com
                # search_url = f"https://www.allmusic.com/search/albums/{artist}+{discogs_album_title}"
                # search_url = f"https://www.allmusic.com/search/albums/{discogs_album_title}"
                search_url = f"https://www.allmusic.com/search/albums/{artist}"
                webbrowser.open(search_url)
                # Prompt user again for input
                result_str = f"Enter year (yyyy) to change to discogs or any other year, 'p' to skip: "
                user_input = input(result_str)
                pyautogui.hotkey('alt', 'tab')
                pyautogui.hotkey('ctrl', 'w')
                pyautogui.hotkey('alt', 'tab')
                # close the webbrowser tab
                # 2.1.2.1 manual correction after search
                if user_input.isdigit():
                    newlabel = user_input
                    newlabel_int = int(newlabel)
                    deviating_albums.append(album)
                    num_changes += 1
                    album_updated = True
                    tq.write(f"{album.title} by {album.artist().title} will be updated")    
                    # 2.1.2.1.1. Convert newlabel to Plex format
                    newlabel_plex = f"{newlabel}-12-31"
                    # 2.1.2.1.2. Update album variables
                    album.edit(**{"originallyAvailableAt.value": newlabel_plex, "originallyAvailableAt.locked": 1})
                    album.edit(**{"year.value": newlabel, "year.locked": 1})
                    updated_albums.append(album)
                    newnewlabel_dict[album] = newlabel
                    # 2.1.2.1.3. update album moods with identifier ".yearchecked"
                    album.addMood([".yearchecked"], locked=True)
                    tq.write(f"The years of '{album.title}' by '{artist}' have been updated to {user_input}.")
                
                    # 2.1.2.2 after search do nothing: back to 2.1.1.
            # 2.1.3 manual correction the first time around (yyyy)
            else:
                newlabel = user_input
                newlabel_int = int(newlabel)
                deviating_albums.append(album)
                num_changes += 1
                album_updated = True
                tq.write(f"{album.title} by {album.artist().title} will be updated")
                # 2.1.1.1. Convert newlabel to Plex format
                newlabel_plex = f"{newlabel}-12-31"
                # 2.1.1.2. Update album variables
                album.edit(**{"originallyAvailableAt.value": newlabel_plex, "originallyAvailableAt.locked": 1})
                album.edit(**{"year.value": newlabel, "year.locked": 1})
                updated_albums.append(album)
                newnewlabel_dict[album] = newlabel
                # 2.1.2.1.
                # enter code to update album moods with identifier ".yearchecked"
                album.addMood([".yearchecked"], locked=True)
                tq.write(f"The years of '{album.title}' by '{artist}' have been updated.")
                # 2.1.1.3. Convert newlabel to Plex format
                newlabel_plex = f"{newlabel}-12-31"

# 3. Cleaning up
# 3.1 Print message
print(f"Out of {len(deviating_albums)} deviating albums, {len(updated_albums)} has/ have been updated.")
print("List of updated albums:")
for album in updated_albums:
    # added newlabel
    # newlabel2_int = int(newlabel) 
    # newnewlabel = newnewlabel_dict[album]
    print(f"{album.title} by {album.parentTitle} now changed to ...")


print(" Exit with any key.")

# 3.3 Exit after any key stroke
input()
