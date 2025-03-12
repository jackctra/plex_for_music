'''This script parses the biographies of all artists in a Plex music library and removes sentences containing a specific keyword. This is useful if you want to remove unwanted information from the biographies of your artists, such as "Last.FM" references'''

from plexapi.server import PlexServer

# User defined variables
keywords_to_remove = ["Last.FM", "last.fm", "Last.fm", "User-contributed text is available under"]
focus = True # if set to True, the script will only look for the above keywords, if set to False, the user can search for additional unwanted phrases which is good for testing. 

# connect to plex
PLEX_URL = 'http://your-plex-server:32400'
PLEX_TOKEN = 'your-plex-token' # https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
plex = PlexServer(PLEX_URL, PLEX_TOKEN)
library = plex.library.section('Music') # Adjust name if needed

# Retrieve all artists
print("Retrieving all artists, may take a while...")
artists = library.all()

for artist in artists:
    print(f"Processing {artist.title}...")
    if not artist.summary:
        continue # Skip artists without a biography

    original_summary = artist.summary
    all_sentences = original_summary.split(". ")

    # Remove unwanted sentences i.e. containing "Last.FM"
    filtered_sentences = [s for s in all_sentences if not any(keyword in s for keyword in keywords_to_remove)]
    
    # Reconstruct the biography 
    new_summary = ". ".join(filtered_sentences).strip()
    if new_summary != original_summary:
        if not focus:
            print(f"Updating {artist.title}: Additional Sentence(s) to remove?\n\n")
            temp_sentences = new_summary.split(". ")
            for i, s in enumerate(temp_sentences):
                print(f"{i+1}. {s}")
            
            indices = input('\n\nEnter the indices of the sentences to remove, separated by commas or hit ENTER if nothing to remove: ')
            if indices:
                indices = [int(index.strip()) - 1 for index in indices.split(',')]
                filtered_sentences = [s for i, s in enumerate(filtered_sentences) if i not in indices]

                # Reapply period correction after removal
                for i in range(len(filtered_sentences) - 1):
                    if not filtered_sentences[i].endswith('.'):
                        filtered_sentences[i] += '.'

                new_summary = ". ".join(filtered_sentences).strip()
  
        # check if last sentence misses a period and is a full sentence
        if not new_summary.endswith("."):
            last_sentence = new_summary.rsplit(".", 1)
            # check if the last part has more than 3 words
            if len(last_sentence[-1].split(" ")) > 3:
                new_summary += "."
        artist.editSummary(new_summary)  # Update the biography
        print("...updated\n")
    else:
        print("...ok\n")

print("All artists have been processed.")
