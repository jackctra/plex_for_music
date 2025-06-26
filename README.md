# This Repository will be archived. Updated Scripts will be published in the new repository ‚PlexForMusic'
---




# plex-scripts for music libraries
Repository for Scripts helping optimize Music Libraries in Plex.
Plex is a great tool for listening to music especially with plexamp. However, there are some issues with keeping the database meaningful, correct and clean. As plex mostly is used for movies and tv shows, there are considerably less scripts for music libraries around.
These scripts were created for personal use to adress these issues with a windows machine and come with the warning that they need to be adapted for a different setting. 

For starters, I will also mention third party work and provide a link if I have personal experience with the code. All other stuff which might be helpful should be mentioned in "Discussions" which I opened exactly for that reason.

This is a continuing project. Possible Categories (found in the branches) are:
1. Metadata Maintenance
2. Playlists
3. Interoperability with other tools.
4. Plex Meta Manager configs for music libraries

Usage:
1. Most scripts point at a config.ini, in which you have to type your personal Plex configuration. The template is provided, has to be renamed to config.ini and completed. See the official documentation how to get your server-ip and token. You have to provide the name of your musiclibrary as well. 
2. In Windows, create a folder for that script. In this folder, put the script- and the ini-file. Then open a terminal in that folder and hit python (scriptname).py

# Categories
# 1. Metadata Maintenance
- PlexAddTextToRecordLabel:For searching purposes, it might come handy to use the field "record label" (internally called studio) with text. 
You can do that in the plex UI, but only for albums one by one or, if for a multitude for albums, by substituting the old text completely. 
With this script, you preserve the existing text. Use "lockfields.py " to save your changes from altering.

- Lockfields: If metadata has been manually changed in the fields, it is good practice to lock the fields in order to protect them from automatic changes in the future. This tool locks the field "Record Label" (internally called "studio") in all albums in music playlists. 

- PlexRecordingDate: a script  to correct entries in the fields: "originally available"and/or "year" to the date of the recording, not the date of publishing, because plexamp needs that for time travelling. Think of Compilations spanning the career of an artist 10 years later. Backup your work with PlexExportAlbumNFO, below.

- CollectionMoodListandDelete: a script to check the moods appended to tracks in a collection and delete specific moods in the tracks. 

- PlexFixMissingTitles: For reasons unknown to me, my library had lots of tracks without titles. To fix that, this script copies the track title from the filename.

- PlexCheckSimArtists: The script loops through all artists and allows for editing the similar artists associated with each artist.

- PlexGetSummary: The script loops through all albums without a summary/review and allows for adding a summary. An allmusic.com page is opened to quickly scan, whether allmusic has a review. Backup your work with PlexExportAlbumNFO, below.

- PlexExportRatingA-Z: The script copies the user ratings of individual tracks in plex to the tags of mp3 and flac files, uses an album by album approach

- PlexExportRecentRatings: The script copies the user ratings of individual tracks in plex to the tags of mp3 and flac files, uses a time based approach

- PlexReleaseTyper: Changes the releasetag of music files and refreshes the album to help grouping the albums (live albums, compilations, singles and EPs).

- TrxGenres: The script displays the genres of the tracks in a given album, thus offering the album view which is still missing in plex.

- CleanArtistBios: The script removes sentences referring to sources like Last.fm in the artist bios.

# 2. Playlists
- playlist to collection: For putting the contents of a playlist into a collection, see https://github.com/Casvt/Plex-scripts/blob/fc919f3cb23cd19424f50f861efc27d5bcb0719b/playlist_collection/playlist_to_collection.py. Why would you do that? In a collection, you can bulk alter fields to which you have no access in playlists.

- Combine playlists: Takes two or more playlists from a Plex server and combines them into a new playlist. Tracks can be sorted in different ways.

- Deduplicator; There are interesting scripts around (https://github.com/YoonAddicting/PlexSmartPlaylistDeduplicator) which avoid duplicates being played twice in a list by tagging the duplicates which are listed after the first track of the same name as "duplicate". Script so far not be tested by me because I want the track with the best quality played, not any one. A proper routine requires a very (!) good maintenance of the library, including same track titles, and a routine to compare both, tracks in an album by a specific artist and tracks in a compilation by various artist. See my blog for more details in the near future.

- Plex PlaylistAddMood: plex has no built in functionality to quickly assign a mood to all tracks in a playlist. This can come handy if you want to create playlists in the future based on a specific mood, i.e. for seasonal playlists like 'Christmas Songs'. The script asks for an existing playlist and adds a specific mood to all its tracks.

- PlexPlaylistAssignRating: There is no builtin functionality to assign the same rating to all tracks in a playlist. This script helps say if you have imported externally created playlists.

- PlexRemoveSongfromPlaylist: Script to identify a track and remove it from non-smart playlists.

- SonicAdventureBuilder: Creates a Sonic Adventure with two tracks as endpoints and saves it to a playlist in plex.

- Plex Trackradio: Creates a (sonically similar) radio playlist from a specific track as a source. It fills the playlist with tracks from the artist who has recorded the source track, and tracks from albums of other artists and from compilations. Sonic Similarity of the tracks and the number of tracks in the Radio playlist can be adjusted. Duplicates are sorted out if the tracks are tagged as either "Duplicate" or "X" in their moods field.  
The user can choose to add a second source track to the playlist to find more tracks or for variation. 
Also, the rating is looked at and already rated tracks with a rating lesser than ***1/2 are sorted out.  

# 3. Interoperability / Backups
- Export playlists for use in other software like Mediamonkey, foobar: https://forums.plex.tv/t/webtools-ng/598539
- Playlist Import: Importing .m3u playlists into plex: https://github.com/gregchak/plex-playlist-import
- PlexRecordingDate: script to query discogs and populate the Release Date field, see above
- PlexExportAlbumNFO: Script to backup all album reviews/summaries (if you added to those plex has created automatically) and the release date (nice if you use it for the recording date, 
  see above).
- PlexExportRatingA-Z: The script copies the user ratings of individual tracks in plex to the tags of mp3 and flac files, uses an album by album approach
- PlexExportRecentRatings: The script copies the user ratings of individual tracks in plex to the tags of mp3 and flac files, uses a time based approach

 # 4. Plex Meta Manager configs
 - overlays; I like that the album covers in plex and plexamp show which codec (mp3 or flac) was used to encode the album tracks. Looks good too. That is achieved with the overlays-function in Plex Meta  Manager.
