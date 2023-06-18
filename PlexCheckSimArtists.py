# Plex uses Similar Artists for adding tracks to playlists. A well maintained database is thus essential for a good listening experience. 
# This script for windows loops through all the artists and allows for each artist to delete or add similar artists. Sources for that can be among others, last.fm, allmusic.com.
# Fill in the music libraries' name in line 14 and make sure that the config.ini is in the same folder. 
# tkinter library must be availabl, if not, pip install.

import os
from plexapi.server import PlexServer
import tkinter as tk

# read config.ini. In config.ini, insert your personal PlexUrl and PlexToken.
with open("config.ini", "r") as f:
    config = f.read()
exec(config)

# Set the name of the music library
MUSIC_LIBRARY_NAME = ""

# Set the path to the progress file
PROGRESS_FILE_PATH = "progressSimArtists.txt"

# Connect to the Plex server
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# Get the music library
music_library = plex.library.section(MUSIC_LIBRARY_NAME)


# Function to get the similar artists for an artist from Plex
def get_similar_artists_from_plex(artist):
    # Get the artist from Plex
    plex_artist = music_library.get(artist)

    # Get the similar artists for the artist from Plex
    similar_artists = plex_artist.similar

    # Return the list of similar artists
    return similar_artists


# Function to add similar artists to an artist in Plex
def add_similar_artists_to_plex(artist, similar_artists):
    # Get the artist from Plex
    plex_artist = music_library.get(artist)

    # Add the similar artists to the artist in Plex
    plex_artist.addSimilarArtist(similar_artists, locked=True)


# Function to remove similar artists
def remove_similar_artists_from_plex(artist, similar_artists):
    # Get the artist
    plex_artist = music_library.get(artist)

    # Remove the similar artists
    plex_artist.removeSimilarArtist(similar_artists, locked=True)


# Function to save progress to a file
def save_progress(progress_file_path, progress):
    with open(progress_file_path, "w") as f:
        f.write(str(progress))


# Function to load progress from a file
def load_progress(progress_file_path):
    if os.path.exists(progress_file_path):
        with open(progress_file_path, "r") as f:
            progress = int(f.read())
            return progress
    else:
        return 0


# Load progress from file
progress = load_progress(PROGRESS_FILE_PATH)

# Get all artists from Plex
artists = music_library.all()

# Create a Tkinter window
window = tk.Tk()
window.title("Plex Similar Artists")

# Create a label for the current artist
artist_label = tk.Label(window, text="", font=("TkDefaultFont", 14, "bold"))
artist_label.pack()

# Create a frame for displaying and removing similar artists
remove_frame = tk.LabelFrame(window, text="Remove Similar Artists", font=("TkDefaultFont", 9, "bold"))
remove_frame.pack(fill="both", expand=True)

# Create a canvas and scrollbar for displaying checkboxes for each similar artist in remove_frame
remove_canvas = tk.Canvas(remove_frame)
remove_scrollbar = tk.Scrollbar(
    remove_frame, orient="vertical", command=remove_canvas.yview)
remove_canvas.configure(yscrollcommand=remove_scrollbar.set)
remove_scrollbar.pack(side="right", fill="y")
remove_canvas.pack(side="left", fill="both", expand=True)

# Create a frame for holding checkboxes for each similar artist in remove_canvas
checkbox_frame = tk.Frame(remove_canvas)
remove_canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")

# Create a list of IntVars for storing checkbox states and a list of Checkbuttons for displaying checkboxes for each similar artist in checkbox_frame
checkbox_vars = []
checkboxes = []

def update_checkboxes():
    global checkbox_vars, checkboxes

    # Clear checkbox_vars and checkboxes lists and destroy any existing Checkbuttons in checkbox_frame
    checkbox_vars.clear()
    checkboxes.clear()
    for widget in checkbox_frame.winfo_children():
        widget.destroy()

    # Get current artist's similar artists and create a Checkbutton with an associated IntVar for each one in checkbox_frame
    for i, similar_artist in enumerate(get_similar_artists_from_plex(artists[progress].title)):
        var = tk.IntVar(value=0)
        checkbox_vars.append(var)
        checkbox = tk.Checkbutton(checkbox_frame, text=similar_artist, variable=var)
        checkbox.grid(row=i, column=0, sticky="w")
        checkboxes.append(checkbox)

    # Update checkbox_frame's size and remove_canvas's scrollregion
    checkbox_frame.update_idletasks()
    remove_canvas.configure(scrollregion=remove_canvas.bbox("all"))

# Create a frame for adding similar artists
add_frame = tk.LabelFrame(window, text="Add Similar Artists", font=("TkDefaultFont", 9, "bold"))
add_frame.pack(fill="both", expand=True)

# Create an entry widget for entering similar artists to add in add_frame
similar_artists_entry = tk.Entry(add_frame)
similar_artists_entry.pack(fill="x")

# Function to update the GUI with the current artist and their similar artists
def update_gui():
    # Update the artist label with the current artist
    artist_label["text"] = f"{artists[progress].title}:"

    # Update checkboxes in remove_frame with current artist's similar artists
    update_checkboxes()

    # Clear similar_artists_entry in add_frame
    similar_artists_entry.delete(0, tk.END)


# Function to handle adding and removing similar artists when the "Apply" button is clicked
def apply_button_clicked():
    global progress

    # Get checked similar artists from remove_frame and remove them from Plex
    checked_similar_artists = [
        checkbox["text"] for i, checkbox in enumerate(checkboxes) if checkbox_vars[i].get()
    ]
    if checked_similar_artists:
        remove_similar_artists_from_plex(artists[progress].title, checked_similar_artists)

    # Get entered similar artists from add_frame and add them to Plex
    entered_similar_artists = [
        x.strip() for x in similar_artists_entry.get().split(",") if x.strip()
    ]
    if entered_similar_artists:
        add_similar_artists_to_plex(artists[progress].title, entered_similar_artists)

    # Update progress and save it to file
    progress += 1
    save_progress(PROGRESS_FILE_PATH, progress)

    # Update GUI with next artist and their similar artists if there are more artists left,
    # otherwise destroy window and exit program.
    if progress < len(artists):
        update_gui()
    else:
        window.destroy()


# Create an "Apply" button for adding and removing similar artists
apply_button = tk.Button(window, text="Apply", command=apply_button_clicked)
apply_button.pack()

# Update GUI with first artist and their similar artists
update_gui()

# Start the Tkinter main loop
window.mainloop()
