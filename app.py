import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from spotify_client import SpotifyClient
from recommender import SongRecommender

# Set page config
st.set_page_config(
    page_title="Spotify Song Recommender",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"  # Hide sidebar since we don't need inputs anymore
)


# Custom CSS - Add this in assets/style.css
def load_css():
    st.markdown("""
    <style>
        /* Main container */
        .stApp {
            background-color: #121212;
            color: white;
        }

        /* Search box */
        .stTextInput>div>div>input {
            color: white;
            background-color: #333333;
            border-radius: 8px;
            padding: 12px;
        }

        /* Buttons */
        .stButton>button {
            background-color: #1DB954;
            color: white;
            border-radius: 20px;
            padding: 10px 24px;
            font-weight: bold;
        }

        /* Song cards */
        .song-card {
            background-color: #181818;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            transition: transform 0.2s;
        }
        .song-card:hover {
            transform: scale(1.02);
        }
    </style>
    """, unsafe_allow_html=True)


def main():
    load_css()

    # Main content
    st.title("🎧 Spotify Song Recommender")
    st.markdown("Discover songs similar to your favorites!")

    # Initialize components with hardcoded credentials
    recommender = SongRecommender("data/processed_song_features.csv")
    spotify = SpotifyClient()  # Uses hardcoded credentials from spotify_client.py

    # Search box
    search_query = st.text_input(
        "Search for a song:",
        placeholder="Type a song name and press Enter",
        key="song_search"
    )

    # Only show results after search
    if search_query:
        with st.spinner(f"🔍 Searching for '{search_query}'..."):
            try:
                # Get matching songs
                matching_songs = [song for song in recommender.get_song_list()
                                  if search_query.lower() in song.lower()][:20]  # Limit to 20 results

                if not matching_songs:
                    st.warning("No songs found. Try a different search term.")
                    return

                # Let user select from filtered results
                selected_song = st.selectbox(
                    "Select your song:",
                    options=matching_songs,
                    key="song_select"
                )

                if st.button("Get Recommendations", type="primary"):
                    with st.spinner("🎶 Finding similar songs..."):
                        recs = recommender.recommend_songs(selected_song)

                        if recs.empty:
                            st.error("Couldn't generate recommendations for this song.")
                        else:
                            st.success(f"🎧 Recommendations similar to **{selected_song}**")

                            # Display recommendations in columns
                            cols = st.columns(3)  # 3 columns layout
                            for idx, (_, row) in enumerate(recs.iterrows()):
                                song, artist = row['name'], row['artists']
                                spotify_data = spotify.get_track_data(song, artist)

                                with cols[idx % 3]:  # Cycle through columns
                                    st.markdown(f"""
                                    <div class="song-card">
                                        <h4>{song[:25]}{'...' if len(song) > 25 else ''}</h4>
                                        <p><i>by {artist[:20]}{'...' if len(artist) > 20 else ''}</i></p>
                                    """, unsafe_allow_html=True)

                                    if spotify_data and spotify_data['image_url']:
                                        response = requests.get(spotify_data['image_url'])
                                        img = Image.open(BytesIO(response.content))
                                        st.image(img, width=200)

                                        if spotify_data.get('url'):
                                            st.markdown(f"""
                                            <a href="{spotify_data['url']}" target="_blank" style="color:#1DB954;">
                                                🎵 Listen on Spotify
                                            </a>
                                            """, unsafe_allow_html=True)

                                        if spotify_data.get('preview_url'):
                                            st.audio(spotify_data['preview_url'], format='audio/mp3')

                                    st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()