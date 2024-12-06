import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()


USERNAME = "Mr.Morale"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get(url=URL, headers=HEADER)
response.raise_for_status()
website_html = response.text

soup = BeautifulSoup(website_html, 'html.parser')

# Adjust the selector as needed to extract song names correctly
song_names = soup.select("li ul li h3")  # Update the selector if it's incorrect

# Extract song names as a list of text
song_name_list = [song_name.getText().strip() for song_name in song_names]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username=USERNAME,
    )
)

user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]

for song in song_name_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    if result and "tracks" in result and result["tracks"]["items"]:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    else:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(f"Created playlist: {playlist['name']}")

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"Added {len(song_uris)} songs to the playlist.")
      




             


