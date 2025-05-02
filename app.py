import streamlit as st
from streamlit_player import st_player
import plotly.express as px
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from spotify_client import SpotifyClient
from recommender import SongRecommender

# Configuration
st.set_page_config(
    page_title="Spotify Recommender Pro",
    page_icon="🎧",
    layout="wide"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
        :root {
            --primary: #1DB954;
            --background: #121212;
            --card: #181818;
        }
        .stApp {
            background: var(--background);
            color: white;
        }
        .stButton>button {
            background: var(--primary);
            border-radius: 20px;
        }
        .song-card {
            background: var(--card);
            border-radius: 10px;
            padding: 15px;
            transition: transform 0.2s;
        }
        .song-card:hover {
            transform: scale(1.03);
        }
    </style>
    """, unsafe_allow_html=True)

# Radar chart visualization
def show_feature_radar(selected_song, recommended_songs, df):
    features = ["danceability", "energy", "acousticness", "valence", "speechiness"]
    selected = df[df['name'] == selected_song][features].iloc[0]
    recommended = df[df['name'].isin(recommended_songs['name'])][features].mean()
    
    fig = px.line_polar(
        pd.DataFrame({
            'Features': features,
            'Selected': selected,
            'Recommended': recommended
        }).melt(id_vars='Features'),
        r='value',
        theta='Features',
        color='variable',
        color_discrete_map={
            'Selected': '#1DB954',
            'Recommended': '#FFFFFF'
        },
        template="plotly_dark"
    )
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)

def main():
    load_css()
    st.title("🎧 Spotify Recommender Pro")
    
    # Initialize components
    recommender = SongRecommender("data/processed_song_features.csv")
    spotify = SpotifyClient()
    df = pd.read_csv("data/processed_song_features.csv")
    
    # Search UI
    search_query = st.text_input("Search songs:", placeholder="Try 'Blinding Lights'...")
    
    if search_query:
        with st.spinner("🎵 Analyzing your music taste..."):
            try:
                matching_songs = [s for s in recommender.get_song_list() 
                                if search_query.lower() in s.lower()][:10]
                
                if not matching_songs:
                    st.warning("No matches found. Try another song!")
                    return
                
                selected_song = st.selectbox("Select a song:", matching_songs)
                
                if st.button("Get Recommendations", type="primary"):
                    recs = recommender.recommend_songs(selected_song)
                    
                    # Player and Visualization
                    st.markdown("---")
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("### Now Playing")
                        spotify_data = spotify.get_track_data(selected_song, "")
                        if spotify_data and spotify_data['url']:
                            track_id = spotify_data['url'].split("/")[-1]
                            st_player(f"https://open.spotify.com/embed/track/{track_id}", 
                                    height=80, playing=False)
                    
                    with col2:
                        st.markdown("### Audio Features")
                        show_feature_radar(selected_song, recs, df)
                    
                    # Recommendations Grid
                    st.markdown("---")
                    st.markdown("### Recommended Tracks")
                    cols = st.columns(3)
                    for idx, (_, row) in enumerate(recs.iterrows()):
                        with cols[idx % 3]:
                            with st.container():
                                st.markdown(f"""
                                <div class="song-card">
                                    <h4>{row['name'][:20]}{'...' if len(row['name']) > 20 else ''}</h4>
                                    <p><i>{row['artists'][:20]}...</i></p>
                                """, unsafe_allow_html=True)
                                
                                song_data = spotify.get_track_data(row['name'], row['artists'])
                                if song_data and song_data['image_url']:
                                    st.image(song_data['image_url'], use_column_width=True)
                                    if song_data['preview_url']:
                                        st.audio(song_data['preview_url'])
                                st.markdown("</div>", unsafe_allow_html=True)
            
            except Exception as e:
                st.error("Our music experts are busy jamming! Try again later.")
                st.code(f"Error: {str(e)}", language='bash')

if __name__ == "__main__":
    main()
