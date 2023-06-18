# A tool which checks whether albums in a music library have a summary. If not, it opens allmusic page to copy the review from it.
# Includes a progress file to allow pausing and restarting where left off.
# config.ini must be in the same folder. Name of music library must be added in line 20

import os
import sys
import webbrowser
import msvcrt
import pyautogui
from plexapi.server import PlexServer
from urllib.parse import quote # to avoid mistakes when passing special characters to a website
import tkinter as tk

# read config.ini. In config.ini, insert your personal PlexUrl and PlexToken.
with open("config.ini", "r") as f:
    config = f.read()
print(config)
exec(config)

PLEX_LIBRARY_NAME = ''
PROGRESS_FILE = 'progress-sum.txt'

def main():
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    library = plex.library.section(PLEX_LIBRARY_NAME)
    albums = library.albums()

    # Check for progress file and read progress if it exists
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            completed_albums = f.read().splitlines()
    else:
        completed_albums = []

    for album in albums:
        if album.title in completed_albums:
            continue

        if not album.summary:
            print(f"{album.parentTitle}'s album '{album.title}' has no summary.")
            title = album.title
            if title.endswith("flac"):
                title = title[:-4]
            encoded_title = quote(title)
            
            webbrowser.open_new_tab(f"https://www.allmusic.com/search/albums/{encoded_title}")

            # Create a tkinter GUI to enter the album summary
            root = tk.Tk()
            root.title("Plex Music Library")

            # Create a label for the artist name and album title and display it in bold with a larger font
            artist_album_label = tk.Label(root, text=f"{album.parentTitle} - {album.title}", font=("Helvetica", 16, "bold"))
            artist_album_label.pack()

            # Create a label and text field for the album summary
            album_summary_label = tk.Label(root, text="Album Summary:")
            album_summary_label.pack()

            album_summary_text = tk.Text(root)
            album_summary_text.pack()

            # Create a Frame to hold the Skip and Exit buttons
            button_frame = tk.Frame(root)
            button_frame.pack(side="bottom", pady=10)

            # Create a Skip button that proceeds to the next album
            def skip_album():
                root.destroy()
                # Close web browser after skipping album
                pyautogui.hotkey('ctrl', 'w')

            skip_button = tk.Button(button_frame, text="Skip", command=skip_album)
            skip_button.pack(side="left", padx=10)

            # Create an Exit button that stops the further execution of the script
            def exit_script():
                sys.exit()

            exit_button = tk.Button(button_frame, text="Exit", command=exit_script)
            exit_button.pack(side="right", padx=10)

            # Create a button to save the album summary
            def save_summary():
                album_summary = album_summary_text.get("1.0", "end-1c")
                album.editField("summary", album_summary)
                print(f"Album summary saved: {album_summary}")
                root.destroy()

            save_button = tk.Button(root, text="Save Summary", command=save_summary)
            save_button.pack()

            root.mainloop()

        # Save progress to file
        with open(PROGRESS_FILE, 'a') as f:
            f.write(album.title + '\n')

        # Close web browser after each item
        pyautogui.hotkey('ctrl', 'w')

    print("All albums checked. Press any key to exit")
    msvcrt.getch()

if __name__ == '__main__':
    main()
