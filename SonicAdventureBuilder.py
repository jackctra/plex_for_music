'''This script prompts user to enter two tracks as endpoints for a 
Sonic Adventure in plex and saves that to a playlist. Other than in plexamp, it is possible to further filter the 
intermediate tracks chosen for the Sonic Adventure by specifying either a genre, whether they are still unplayed or whether they have been
rated at least with 4 stars. Filtering can lead to a much shorter playlist though. If no filter is activated, the length of the playlist will be roundabout an hour or so.
--> Enter your Plex-Url, Token and name of your music library before running'''

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

def ensure_start_end_in_tracks(tracks, start_track, end_track):
    # Überprüfen, ob der Starttrack in der Liste ist
    if start_track not in tracks:
        tracks.insert(0, start_track)  # Füge den Starttrack an die erste Stelle hinzu
    # Überprüfen, ob der Endtrack in der Liste ist
    if end_track not in tracks:
        tracks.append(end_track)  # Füge den Endtrack an die letzte Stelle hinzu
    return tracks


def create_sonic_adventure_playlist(start_track, end_track, genre=None, unplayed=False, min_rating=False):
    
    # prepare the filtering kwargs
    kwargs = {}
    if genre:
        kwargs['Genre__tag'] = genre
    if unplayed:
        kwargs['viewCount'] = int(0)
    if min_rating:
        kwargs['userRating__gte'] = 8.0  # Plex uses a scale from 1 to 10, __gte stands for greater or equal
    
    adventure_tracks = library.sonicAdventure(start=start_track, end=end_track, **kwargs)
    
    if not adventure_tracks:
        print("No tracks found for the SonicAdventure.")
        return

    # check if start and endtrack are still included
    adventure_tracks = ensure_start_end_in_tracks(adventure_tracks, start_track, end_track)

    # for debugging
    for track in adventure_tracks:
        print(f'\n{track.grandparentTitle}-{track.title}-{track.genres}-{track.userRating}')

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

    genre = input("Enter a genre to filter by for all tracks (or leave blank): ")
    unplayed_input = input("Include only unplayed tracks? (yes/leave blank): ").strip().lower()
    unplayed = unplayed_input == 'yes' or unplayed_input == 'y'
    min_rating_input = input("Include only tracks with at least 4 stars) (yes/leave blank): ").strip().lower()
    min_rating = min_rating_input == 'yes' or min_rating_input == 'y'


    create_sonic_adventure_playlist(start_track, end_track, genre if genre else None, unplayed, min_rating)

if __name__ == "__main__":
    main()
