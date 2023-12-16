"""Plex TrackRadio V1 is a script that takes user input and fetches the rating key either 
of a specific track or optionally the whole album. Needs plexapi 4.15.6 and an ini file. 
It fills the playlist with tracks from the artist who has recorded the source track, and tracks from albums of other artists and from compilations. 
Sonic Similarity of the tracks and the number of tracks in the Radio playlist can be adjusted. Duplicates are sorted out if the tracks are tagged as either Duplicate or X in the moods field.  
The user can choose to add a second source track to the playlist to find more tracks or for variation. 
Also, the rating is looked at and tracks with a rating lesser than ***1/2 are sorted out. """

import os
import re

from tqdm import tqdm # library for progress bar
from plexapi.server import PlexServer
import plexapi


 # read config.ini. In config.ini, you have to insert your personal PlexUrl and PlexToken.
with open("config.ini", "r") as f:
    config = f.read()
print(config)
exec(config)
# library = plex.library.section("test")
all_similar_tracks = []
sonically_similar_tracks = []
playlist_title = []


def get_working_folder():
    
    # Fetch script path
    script_path = os.path.abspath(__file__)

    # fetch folder
    script_folder = os.path.dirname(script_path)

    return script_folder

def get_track():
    # ask user for ratingKey or tracktitle
    # initialize playlist_title
    global playlist_title
    user_input = input("Identify track with ratingKey or enter track- and radiotitle: ")
    
    if user_input.isdigit():
        # !!!take input as ratingKey and search library for track!!!
        rating_key = int(user_input)
        if rating_key:
            # !!!search library for track with ratingKey!!!
            track = library.fetchItem(rating_key)
            playlist_title = track.title
    else:
        # search library for tracktitle
        playlist_title = user_input
        search_results = library.searchTracks(title=user_input)
        # put search results in a list
        search_results_list = list(search_results)
        # If the library has multiple editions of the same track, all but one can be tagged as Duplicates. This code block looks for duplicates in the mood tags and remove them from the list !!!Moods is a list of `mood` objects, not strings. Therefore the comparison `"Duplicate" not in item.moods` does not work, as it tries to compare a string with a list of `Mood` objects. You need to check the `tag` property of each `mood` object to see if it is "Duplicate"!!! 
        search_results_list = [item for item in search_results_list if not any(mood.tag == "Duplicate" for mood in item.moods)]
        
        # look for tracks with a rating lesser than ***1/2 and remove them from the list but keep all tracks with no rating
        # search_results_list = [item for item in search_results_list if item.userRating is None]
        search_results_list = [item for item in search_results_list if item.userRating is None or item.userRating in [-1, 7, 8, 9, 10]]
        # search_results_list = [item for item in search_results_list if item.userRating is None or item.userRating > 7.0]
        
        if len(search_results_list) > 1:
            # print search results, prepended by a number to choose
            for i, result in enumerate(search_results_list):
                
                print(f"{i+1}.{result.grandparentTitle}/{result.originalTitle} - {result.title}")	
            
            # ask user to choose the number of the track if there is more than one match
            choice = int(input("Choose the number of the track: "))
            
            # fetch track
            track = search_results_list[choice-1]
        elif len(search_results_list) == 1:
            # fetch the only track
            track = search_results_list[0]
        else:
            print("No matching track found.")
            get_track()
    
    # do something with the fetched track
    print(f"Fetched track: {track.title}")
	# append track to list of tracks
    all_similar_tracks.append(track)
    return track				

def find_sonically_similar_tracks(track):
    # plexapi now has a a new method, sonicallySimilar, to the Audio class. The similarity is measured in distance.
    # let user enter how many tracks should be fetched (parameter limit) and what the maximal Distance from the source track is (parameter maxDistance)
    limit_input = input("How many tracks in 10s should be fetched? -Default = 10 ")
    limit = 10 if limit_input.strip() == "" else int(limit_input)
    maxdistance_input = input("What is the maximal Distance from the source track? -0.0-1.0, default = 0.2 ")
    maxDistance = 0.2 if maxdistance_input.strip() == "" else float(maxdistance_input)
    # go to the audio class of the track and get the sonically similar tracks 	
    sonically_similar_tracks = track.sonicallySimilar(limit=limit, maxDistance=maxDistance)
    # filter out tracks which have a track.mood ‚Duplicate‘
    sonically_similar_tracks = [track for track in sonically_similar_tracks if not any(mood.tag == "Duplicate" for mood in track.moods)]

    # if no tracks are found, print "No similar tracks found" and go back to beginning of function
    if len(sonically_similar_tracks) == 0:
        print("No similar tracks found. Increase maxDistance.")
        find_sonically_similar_tracks(track)
    elif len(sonically_similar_tracks) < limit:
        print(f"Only {len(sonically_similar_tracks)} X-tracks found: ") # You can increase the number of tracks in your radio playlist
        # print the fetched tracks with artist and tracktitle
        for i, result in enumerate(sonically_similar_tracks):
            print(f"{i+1}. {result.grandparentTitle}/{result.originalTitle} - {result.title}")

        user_input = input(" Increase limit (and maxDistance), add a second sourcetrack from the list with 'a' and number (i.e. 'a2') or continue with 'c'.")
        # if user input is neither 'a' nor 'c', go back to beginning of function
        if user_input.startswith("a"):
            # print the fetched tracks with artist and tracktitle prepended by a number to choose
            all_similar_tracks.extend(sonically_similar_tracks)
            # fetch number of sourcetrack from splitted user input
            choice = int(user_input.split("a")[1])
            # fetch track and print as 2nd sourcetrack
            #print 2ndsourcetrack
            print(f"2nd source track: {sonically_similar_tracks[choice-1].title}")
            track = sonically_similar_tracks[choice-1]
            # go to function find_sonically_similar_tracks
            find_sonically_similar_tracks(track)

        elif user_input != "c":
            find_sonically_similar_tracks(track)
    else: 
        pass
    # print the fetched tracks with artist and tracktitle
    print('\n\nSimilar X-Tracks apart from the Source track are:')
    all_similar_tracks.extend(sonically_similar_tracks)
    for i, result in enumerate(all_similar_tracks):
        print(f"{i+1}. {result.grandparentTitle}/{result.originalTitle} - {result.title} , rated '{result.userRating}'")
    # check if user has chosen a 2nd source track, then sst should be shorter than all_similar_tracks minus the first source track
    if len(sonically_similar_tracks) < len(all_similar_tracks)-1 :
        print('and from the 2nd source track:')
        for i, result in enumerate(sonically_similar_tracks):
            print(f"{i+1}. {result.grandparentTitle}/{result.originalTitle} - {result.title}. rated '{result.userRating}'")	
    print('________________\n\n')
    
    # all_similar_tracks.extend(sonically_similar_tracks) - moved
    create_playlist(all_similar_tracks)
    exit()

def ask_again(sonically_similar_tracks):
    # ask user if they want to add further tracks to the playlist
    user_input = input("Do you want to add further tracks, enter the number of the new source track, else 'n' ")
    if user_input.isdigit():
        choice = int(user_input)
        # fetch track
        track = sonically_similar_tracks[choice-1]

        # go to function find_sonically_similar_tracks
        find_sonically_similar_tracks(track)
    else:
        print("No further tracks added.")
        pass  


def create_playlist(all_similar_tracks):
    # create a new playlist in Plexwith the name of choice of user + SonicSimPlaylist
    input_name = playlist_title
    # create a new playlist in Plex with the {input_name}postpended by "SonicSimPlaylist""
    plex.createPlaylist(f"Radio {input_name}", items = all_similar_tracks)
    # print the name of the created playlist
    print(f"Created playlist: Radio {input_name}")
    
				
												


def main():
    working_folder = get_working_folder()
    os.chdir(working_folder)
    global library
    
    track = get_track()  # Define the 'track' variable by calling the 'get_track' function
     
    sonically_similar_tracks = find_sonically_similar_tracks(track)
    ask_again(sonically_similar_tracks)

    


if __name__ == "__main__":
    main()
