# This script accesses a music-tracks collection in plex, lists the moods appended to the tracks and allows for the deletion of an entry for all tracks in that collection. 
# Enter baseurl, token to access plex, enter name of music library in plex. 

from plexapi.server import PlexServer
import os

baseurl = 'http://xxx.xxx.xxx.xx:32400'
token = 'xxxxxxxxxxxxx'

plex = PlexServer(baseurl, token)

collection_name = input('Enter the name of the collection: ')
# mood_to_delete = input('Enter the mood to delete: ')

collection = plex.library.section('xxxx').collection(collection_name)
moods = set()
for track in collection.items():
    moods.update(track.moods)

print('Moods in tracks within collection:')
# for mood in moods:
#     print(mood)

for track in collection.items():
    mood_strings = [str(mood) for mood in track.moods]
    print(f"{track.title}: {', '.join(mood_strings)}")

# Create a .txt file with the original title, track title, and associated moods for each track in the collection
filename = f"{collection_name}_moods.txt"
with open(filename, 'w', encoding='utf-8') as f:
    for track in collection.items():
        mood_strings = [str(mood) for mood in track.moods]
        f.write(f"{track.originalTitle} - {track.title}: {', '.join(mood_strings)}\n")

# Open the .txt file in an editor instance
os.startfile(filename)

mood_to_delete = input('Enter the mood to delete: ')

for track in collection.items():
    moods = track.moods
    for mood in moods:
        if mood.tag == mood_to_delete:
            track.removeMood(mood, locked=True)
