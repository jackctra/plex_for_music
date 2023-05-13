# plex-scripts for music libraries
Repository for Scripts helping optimize Music Libraries in Plex.
Plex is a great tool for listening to music especially with plexamp. However, there are some issues with keeping the database meaningful, correct and clean. As plex mostly is used for movies and tv shows, there are considerably less scripts for music libraries around.
These scripts were created for personal use to adress these issues and come with the warning that they need to be adapted for a different setting. 

This is an unfinished project. Possible Categories (found in the branches) are:
1. Metadata Maintenance
2. Playlists
3. Interoperability with other tools.

Usage:
1. All scripts point at a config.ini, in which you have to type your personal Plex configuration. The template is provided, has to be renamed to config.ini and completed. See the official documentation how to get your server-ip and token. You have to provide the name of your musiclibrary as well. 
2. In Windows, create a folder for that script. In this folder, put the script- and the ini-file. Then open a terminal in that folder and hit python (scriptname).py

# Branches
1. Metadata Maintenance
- PlexAddTextToRecordLabel:For searching purposes, it might come handy to use the field "record label" (internally called studio) with text. 
You can do that in the plex UI, but only for albums one by one or, if for a multitude for albums, by substituting the old text completely. 
With this script, you preserve the existing text. Use "lockfields.py " to save your changes from altering.

- Lockfields: If metadata has been manually changed in the fields, it is good practice to lock the fields in order to protect them from automatic changes in the future. This tool locks the field "Record Label" (internally called "studio") in all albums in music playlists. 

- not yet coded: a script  to mass correct wrong entries in the fields: "originally available"and/or "year" becaus plexamp needs that for time travelling. Might use data from other sources like discogs.Might also fall under "Interoperability".

2. Playlists
- playlist to collection: For putting the contents of a playlist into a collection, see https://github.com/Casvt/Plex-scripts/blob/fc919f3cb23cd19424f50f861efc27d5bcb0719b/playlist_collection/playlist_to_collection.py. Why would you do that? In a collection, you can bulk alter fields to which you have no access in playlists.

- Deduplicator; There are interesting scripts around which avoid duplicates being played twice in a list by tagging the duplicates which are listed after the first track of the same name as "duplicate". Script so far not be tested by me because I want the track with the best quality played, not any one. Although not always the case, bitrate could serve as aproxy for quality and tracks could be compared before deciding whether to tag them as a duplicate. 

3. Interoperability
- Export playlists for use in other software like Mediamonkey, foobar: https://forums.plex.tv/t/webtools-ng/598539
- Playlist Import: Importing .m3u playlists into plex: https://github.com/gregchak/plex-playlist-import
- not vet coded: script to query discogs and populate plex fields, see also above
