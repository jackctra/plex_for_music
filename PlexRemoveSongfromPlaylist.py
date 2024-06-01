''' Script to identify a track and remove it from non-smart playlists.
Fill in plexurl, token, library name and install requirements. PySimpleGui is free for personal use, but requires a registration.'''

import plexapi
import os
from plexapi.server import PlexServer
import PySimpleGUI as sg

plexurl = ''
token = ''
library_name = ''

# 3. Connect to the Plex server
plex = PlexServer(plexurl, token)
library = plex.library.section(library_name)

def prompt_for_artist_and_title():
    layout = [
        [sg.Text('Enter artist and track title')],
        [sg.Text('Artist', size=(15, 1)), sg.InputText(key='-ARTIST-')],
        [sg.Text('Track Title', size=(15, 1)), sg.InputText(key='-TITLE-')],
        [sg.Button('Search'), sg.Button('Cancel')]
    ]   
    window = sg.Window('Search for Track', layout)
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            window.close()
            return None, None
        if event == 'Search':
            artist = values['-ARTIST-']
            title = values['-TITLE-']
            window.close()
            return artist, title

def search_track(plex, artist, title):
    tracks = plex.library.search(title=title, libtype='track')
    matching_tracks = [track for track in tracks if (track.originalTitle and track.originalTitle.lower() == artist.lower()) or
                                                  (track.grandparentTitle and track.grandparentTitle.lower() == artist.lower())]
    if not matching_tracks:
        sg.popup('No matching tracks found.')
        return None
    return matching_tracks

def show_playlists_including_track(library, track):
    playlists = library.playlists()
    # Filter out smart playlists
    playlists = [playlist for playlist in playlists if not playlist.smart]
    for playlist in playlists:
        including_playlists = [playlist for playlist in playlists if any(item.ratingKey == track.ratingKey for item in playlist.items())]
    if not including_playlists:
        return []
    
    layout = [
        [sg.Text('Select the playlists that include the track')],
        [sg.Column([[sg.Checkbox(playlist.title, key=f'-PLAYLIST-{i}-')] for i, playlist in enumerate(including_playlists)])],
        [sg.Button('Go'), sg.Button('Cancel')]
    ]
    window = sg.Window('Playlists Including Track', layout)
    
    selected_playlists = []
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        if event == 'Go':
            selected_indices = [i for i in range(len(including_playlists)) if values.get(f'-PLAYLIST-{i}-')]
            selected_playlists = [including_playlists[i] for i in selected_indices]
            break

    window.close()
    return selected_playlists

def delete_track_from_playlists(track, playlists):
    for playlist in playlists:
        try:
            if track in playlist.items():
                playlist.removeItem(track)
                sg.popup(f'Removed "{track.title}" from "{playlist.title}"')
        except Exception as e:
            sg.popup(f'Error removing {track.title} from {playlist.title}: {e}')

# Main 
artist, title = prompt_for_artist_and_title()
if artist and title:
    matching_tracks = search_track(plex, artist, title)
    if matching_tracks:
        for track in matching_tracks:
            selected_playlists = show_playlists_including_track(library, track)
            delete_track_from_playlists(track, selected_playlists)
