'''Simple script to check track genres of an album. Replace all 'XXX'  with your username, password, server- and library name) '''

import plexapi
from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
import FreeSimpleGUI as sg

# enter your credentials and the name of the library
username = 'XXX'
password = 'XXX'
server_name = 'XXX'
library_name = 'XXX'

# connect to plex
account = MyPlexAccount(username, password)
plex = account.resource(server_name).connect()
# define library
library = plex.library.section(library_name) # necessary conversion from the string

def parse_user_input():
    user_input = input("Enter album title: \n")
    album_title = user_input
    albums = library.searchAlbums(title=album_title)
    if len(albums) == 0:
        print(f"No album found with title '{album_title}'")
    elif len(albums) > 1:
        print(f"Multiple albums found with title '{album_title}'. Please choose one \n(path taken from the first track):")
        for i, album in enumerate(albums):
            print(f"{i+1}. {album.parentTitle} - {album.title}")
        album_choice = int(input("Enter your choice: "))
        album = albums[album_choice-1]
    else:
        album = albums[0]
    return album

def display_album_info(album):
    # Create a PySimpleGUI window
    sg.theme("DarkBlue3")
    
    # Initialize the track layout with a list
    track_layout = []

    # Add track information to the layout
    for track in album.tracks():
        track_info = f"{track.index} - {track.title}"
        if track.grandparentTitle == "Various Artists":
            track_info += f" ({track.originalTitle})"
        genre_info = track.genres
        genre_names = [g.tag for g in genre_info]
        genre_string = "; ".join(genre_names)
              
        # Create Track-Info and Genres Elements
        track_text = sg.Text(track_info, size=(60, 1), pad=((0, 0), 0, 0))
        genre_text = sg.Text(f"Genres: {genre_string}", size=(40, 1), pad=((0, 80), 0, 0))

        # Append all elements to one line
        track_layout.append([sg.Column([[track_text]], justification='left'), 
                            sg.Column([[genre_text]], justification='left'), 
                            ])
    # Create a layout with a Scrollable Frame
    layout = [
        [sg.Text(f"Album: '{album.title}'", font=("Helvetica", 14, "bold")), sg.Button("Exit", pad=((200,0), 0))],
        [sg.Text(f"Artist: '{album.parentTitle}'", font=("Helvetica", 12))],
        [sg.Text("Tracks:", font=("Helvetica", 12))],
        [sg.HorizontalSeparator()],  
        [sg.Column(track_layout, size=(800, 380), scrollable=True, vertical_scroll_only=True)]
    ]
    window = sg.Window("Track Genres of Album", layout, finalize=True, size=(800, 500))
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
    window.close()
def main():
    album = parse_user_input()
    display_album_info(album)
main()












