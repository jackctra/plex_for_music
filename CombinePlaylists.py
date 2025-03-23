'''This script takes two or more playlists from a Plex server and combines them into a new playlist. Tracks can be sorted in different ways. You have to enter your plex credentials first.'''

from plexapi.server import PlexServer
from plexapi.exceptions import NotFound
import random
from datetime import datetime

# get plex instance
# PLEX_URL = "http://your-plex-server:32400"
# PLEX_TOKEN = "your-plex-token" 

def get_plex_connection():
    """Connect to the Plex server."""
    try:
        plex = PlexServer(PLEX_URL, PLEX_TOKEN)
        return plex
    except Exception as e:
        print(f"Error connecting to Plex: {e}")
        exit(1)

def list_playlists(plex):
    """Retrieve all playlists from the Plex server."""
    playlists = plex.playlists()
    if not playlists:
        print("No playlists found.")
        exit(1)
    
    print("\nAvailable Playlists:")
    for idx, playlist in enumerate(playlists, 1):
        print(f"{idx}. {playlist.title}")
    
    return playlists

def choose_playlists(playlists):
    """Prompt user to select two or more playlists."""
    selected_indexes = input("\nEnter playlist numbers (comma-separated): ")
    selected_indexes = [int(i.strip()) - 1 for i in selected_indexes.split(",") if i.strip().isdigit()]

    if len(selected_indexes) < 2:
        print("You must select at least two playlists.")
        exit(1)

    return [playlists[i] for i in selected_indexes]

def reorder_tracks(playlists):
    """Prompt user to select the order of tracks."""
    user_input = input("\nKeep sequence of playlists ('k'), sort tracks by last play date (ascending, 'a') or shuffle randomly ('r') : ")
    return user_input.lower()
def create_combined_playlist(plex, selected_playlists, seq):
    """Combine multiple playlists into a new one."""
    all_items = []
    for playlist in selected_playlists:
        all_items.extend(playlist.items())

    if seq == 'r':
        random.shuffle(all_items)
    elif seq == 'a':
        # check if all items have lastViewedAt attribute, if None, put item to the beginning of the list
        proxy_date = datetime(1900, 1, 1)
        all_items.sort(key=lambda x: x.lastViewedAt if x.lastViewedAt else proxy_date)
        print("Tracks sorted by last play date:")
        for idx, item in enumerate(all_items, 1):
            print(f"{idx}. {item.title} - {item.lastViewedAt}")

    new_playlist_name = input("Enter name for the new combined playlist: ")
    
    try:
        plex.createPlaylist(new_playlist_name, items=list(all_items))
        print(f"New playlist '{new_playlist_name}' created successfully!")
    except Exception as e:
        print(f"Error creating playlist: {e}")

def main():
    plex = get_plex_connection()
    playlists = list_playlists(plex)
    selected_playlists = choose_playlists(playlists)
    seq = reorder_tracks(selected_playlists)
    create_combined_playlist(plex, selected_playlists, seq)

if __name__ == "__main__":
    main()
