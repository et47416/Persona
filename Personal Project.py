import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials  # ✅ Make sure this is imported
import os

# Load Spotify credentials from Streamlit secrets
SPOTIPY_CLIENT_ID = st.secrets["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = st.secrets["SPOTIPY_CLIENT_SECRET"]

# Use Client Credentials Flow instead of OAuth
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
))

st.title("🎵 Music Recommender Generator")
st.write("Personalized music recommendations tailored for you!")

# Session state to store user input
if "selected_genres" not in st.session_state:
    st.session_state.selected_genres = []
if "selected_artists" not in st.session_state:
    st.session_state.selected_artists = []
if "fav_song" not in st.session_state:
    st.session_state.fav_song = ""
if "disliked_genres" not in st.session_state:
    st.session_state.disliked_genres = []
if "recommended_songs" not in st.session_state:
    st.session_state.recommended_songs = []

# Step 1: Select Favorite Genres
genre_artists = {
    "Pop": ["Taylor Swift", "Ariana Grande", "Dua Lipa", "The Weeknd"],
    "Hip-Hop": ["Drake", "Kanye West", "Travis Scott", "Kendrick Lamar"],
    "Rock": ["Imagine Dragons", "Queen", "Foo Fighters", "The Rolling Stones"],
    "Electronic": ["Calvin Harris", "Marshmello", "Zedd", "Kygo"],
    "R&B": ["SZA", "Brent Faiyaz", "The Weeknd", "H.E.R."],
    "Indie": ["Arctic Monkeys", "The Strokes", "Radiohead", "Vampire Weekend"]
}

selected_genres = st.multiselect("Select your favorite genres:", list(genre_artists.keys()))
st.session_state.selected_genres = selected_genres

# Step 2: Select Favorite Artists
if selected_genres:
    possible_artists = [artist for genre in selected_genres for artist in genre_artists[genre]]
    selected_artists = st.multiselect("Select your favorite artists:", possible_artists)
    st.session_state.selected_artists = selected_artists

# Step 3: Enter a Favorite Song
fav_song = st.text_input("Enter a song you can listen to on repeat:")
st.session_state.fav_song = fav_song

# Step 4: Select Disliked Genres
disliked_genres = st.multiselect("Select any genres you dislike:", list(genre_artists.keys()))
st.session_state.disliked_genres = disliked_genres

# Fetch recommendations
def get_spotify_song_recommendations():
    song_results = set()
    artist_count = defaultdict(int)
    
    for artist_name in st.session_state.selected_artists:
        result = sp.search(q=f"artist:{artist_name}", type="track", limit=5)
        for track in result["tracks"]["items"]:
            song = f"{track['name']} - {track['artists'][0]['name']}"
            track_artist = track['artists'][0]['name']
            if song not in song_results and st.session_state.fav_song.lower() not in song.lower() and artist_count[track_artist] < 2:
                song_results.add(song)
                artist_count[track_artist] += 1
    
    return list(song_results)[:10]

if st.button("Generate Recommendations"):
    st.session_state.recommended_songs = get_spotify_song_recommendations()
    
# Display Recommendations
if st.session_state.recommended_songs:
    st.subheader("🎧 Your Personalized Playlist")
    for song in st.session_state.recommended_songs:
        st.write(f"- {song}")
