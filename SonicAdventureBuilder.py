'''This script PlexSonicAdventure prompts user to enter two tracks as endpoints for a 
Sonic Adventure in plex and saves that to a playlist.
---> Enter your Plex-Url, Token and name of your music library before running'''

from plexapi.server import PlexServer

PLEX_URL = 'http://xxx.xxx.xx.xx:32400'
PLEX_TOKEN = 'xxxxxxcxxxxxx'
plex = PlexServer(PLEX_URL, PLEX_TOKEN)
library = plex.library.section("xxx")

def find_track(track_title):
    tracks = library.search(track_title, libtype='track')
    if not tracks:
        print(f"Track '{track_title}' not found.")
        return None
    if len(tracks) == 1:
        return tracks[0]
    # if multiple tracks offer choice:
    print(f"Multiple tracks found for '{track_title}':")
    for idx, track in enumerate(tracks, start=1):
        if track.grandparentTitle == 'Various Artists':
            artist_title = track.originalTitle
        else:
            artist_title = track.grandparentTitle
        print(f"{idx}. {artist_title} - {track.title}")

    selected_index = int(input("Enter the number of the correct track: ")) - 1
    if 0 <= selected_index < len(tracks):
        return tracks[selected_index]
    else:
        print("Invalid selection.")
        return None

def create_sonic_adventure_playlist(start_track, end_track):
    adventure_tracks = library.sonicAdventure(start=start_track, end=end_track)

    if not adventure_tracks:
        print("No tracks found for the SonicAdventure.")
        return

    playlist_name = f"SonicAdventure from {start_track.title} to {end_track.title}"
    playlist = plex.createPlaylist(playlist_name, items=adventure_tracks)
    print(f"Playlist '{playlist_name}' created successfully with {len(adventure_tracks)} tracks.")

def main():
    start_track_title = input("Enter the title of the start track: ")
    end_track_title = input("Enter the title of the end track: ")

    start_track = find_track(start_track_title)
    if not start_track:
        return

    end_track = find_track(end_track_title)
    if not end_track:
        return

    create_sonic_adventure_playlist(start_track, end_track)

if __name__ == "__main__":
    main()
