# plex-scripts for music libraries
Repository for Scripts helping optimize Music Libraries in Plex.
Plex is a great tool for listening to music especially with plexamp. However, there are some issues with keeping the database meaningful, correct and clean. As plex mostly is used for movies and tv shows, there are considerably less scripts for music libraries around.
These scripts were created for personal use to adress these issues and come with the warning that they need to be adapted for a different setting. 

This is an unfinished project. Possible Categories are:
1. Metadata Maintenance
2. Playlists
3. Interoperability with other tools.
Additional scripts to fill these categories are welcome.

Usage:
1. All scripts point at a config.ini, in which you have to type your personal Plex configuration. The template is provided, has to be renamed to config.ini and completed. See the official documentation how to get your server-ip and token. You have to provide the name of your musiclibrary as well. 
2. In Windows, create a folder for that script. In this folder, put the script- and the ini-file. Then open a terminal in that folder and hit python (scriptname).py

Categories
1. Metadata Maintenance
- PlexAddTextToRecordLabel:For searching purposes, it might come handy to use the field "record label" (internally called studio) with text. 
You can do that in the plex UI, but only for albums one by one or, if for a multitude for albums, by substituting the old text completely. 
With this script, you preserve the existing text. Use "lockfields.py " to save your changes from altering.

- Lockfields: If metadata has been manually changed in the fields, it is good practice to lock the fields in order to protect them from automatic changes in the future. This tool locks the field "Record Label" (internally called "studio") in all albums in music playlists. 
