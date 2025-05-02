import streamlit as st
from streamlit_player import st_player
import plotly.express as px
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from spotify_client import SpotifyClient
from recommender import SongRecommender
import os

<<<<<<< HEAD
# Page Configuration
st.set_page_config(
    page_title="Spotify Recommender Pro",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS (embedded directly)
=======
# Configuration
st.set_page_config(
    page_title="Spotify Recommender Pro",
    page_icon="🎧",
    layout="wide"
)

# Custom CSS
>>>>>>> e44f7887a4b612a2690fecef055aa0dfa01c5401
def load_css():
    st.markdown("""
    <style>
        :root {
            --primary: #1DB954;
            --background: #121212;
            --card: #181818;
<<<<<<< HEAD
            --text: #FFFFFF;
        }
        
        .stApp {
            background: var(--background);
            color: var(--text);
            padding: 2rem;
        }
        
        .stTextInput>div>div>input {
            color: var(--text);
            background: #333;
            border-radius: 8px;
            padding: 12px;
        }
        
        .stButton>button {
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 24px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .stButton>button:hover {
            transform: scale(1.05);
            opacity: 0.9;
        }
        
        .song-card {
            background: var(--card);
            border-radius: 12px;
            padding: 1rem;
            transition: transform 0.3s;
            margin-bottom: 1rem;
=======
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
>>>>>>> e44f7887a4b612a2690fecef055aa0dfa01c5401
        }
        
        .song-card:hover {
<<<<<<< HEAD
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        
        .player-container {
            border-radius: 12px;
            overflow: hidden;
            margin: 1rem 0;
=======
            transform: scale(1.03);
>>>>>>> e44f7887a4b612a2690fecef055aa0dfa01c5401
        }
    </style>
    """, unsafe_allow_html=True)

# Radar chart visualization
def show_feature_radar(selected_song, recommended_songs, df):
    features = ["danceability", "energy", "acousticness", "valence", "speechiness"]
<<<<<<< HEAD
    
    selected_features = df[df['name'] == selected_song][features].iloc[0]
    recommended_mean = df[df['name'].isin(recommended_songs['name'])][features].mean()
=======
    selected = df[df['name'] == selected_song][features].iloc[0]
    recommended = df[df['name'].isin(recommended_songs['name'])][features].mean()
>>>>>>> e44f7887a4b612a2690fecef055aa0dfa01c5401
    
    fig = px.line_polar(
        pd.DataFrame({
            'Features': features,
<<<<<<< HEAD
            'Selected Song': selected_features,
            'Recommended': recommended_mean
=======
            'Selected': selected,
            'Recommended': recommended
>>>>>>> e44f7887a4b612a2690fecef055aa0dfa01c5401
        }).melt(id_vars='Features'),
        r='value',
        theta='Features',
        color='variable',
<<<<<<< HEAD
        color_discrete_sequence=["#1DB954", "#FFFFFF"],
        template="plotly_dark",
        line_close=True
    )
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,1])),
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    
=======
        color_discrete_map={
            'Selected': '#1DB954',
            'Recommended': '#FFFFFF'
        },
        template="plotly_dark"
    )
    fig.update_traces(fill='toself')
>>>>>>> e44f7887a4b612a2690fecef055aa0dfa01c5401
    st.plotly_chart(fig, use_container_width=True)

def main():
    load_css()
<<<<<<< HEAD
    
    # App Header
    st.markdown("<h1 style='text-align: center; color: #1DB954;'>🎧 Spotify Recommender Pro</h1>", 
                unsafe_allow_html=True)
    
    # Initialize components
    try:
        df = pd.read_csv("data/processed_song_features.csv")
        recommender = SongRecommender(df)
        spotify = SpotifyClient()
    except Exception as e:
        st.error(f"Initialization failed: {str(e)}")
        st.stop()
    
    # Search Section
    with st.container():
        col1, col2 = st.columns([3,1])
        with col1:
            search_query = st.text_input(
                "Search for a song:",
                placeholder="Try 'Blinding Lights'...",
                key="search"
            )
        
    # Results Section
    if search_query:
        with st.spinner("🔍 Finding your musical matches..."):
            try:
                matching_songs = [song for song in recommender.get_song_list() 
                                if search_query.lower() in song.lower()][:10]
                
                if not matching_songs:
                    st.warning("No matching songs found. Try a different search!")
                    return
                
                selected_song = st.selectbox(
                    "Select a song from the results:",
                    matching_songs,
                    key="song_select"
                )
                
                if st.button("Get Recommendations", type="primary"):
                    with st.spinner("🎶 Analyzing audio features..."):
                        recs = recommender.recommend_songs(selected_song)
                        
                        # Player and Features Section
                        st.markdown("---")
                        st.markdown(f"<h2 style='color: #1DB954;'>Now Playing: {selected_song}</h2>", 
                                   unsafe_allow_html=True)
                        
                        spotify_data = spotify.get_track_data(selected_song, "")
                        if spotify_data and spotify_data['url']:
                            with st.container():
                                st.markdown("<div class='player-container'>", unsafe_allow_html=True)
                                track_id = spotify_data['url'].split("/")[-1].split("?")[0]
                                st_player(
                                    f"https://open.spotify.com/embed/track/{track_id}",
                                    height=80,
                                    playing=False
                                )
                                st.markdown("</div>", unsafe_allow_html=True)
                        
                        # Radar Chart
                        st.markdown("### Audio Features Comparison")
                        show_feature_radar(selected_song, recs, df)
                        
                        # Recommendations Grid
                        st.markdown("---")
                        st.markdown("### 🎵 Recommended Tracks")
                        cols = st.columns(3)
                        for idx, (_, row) in enumerate(recs.iterrows()):
                            with cols[idx % 3]:
                                with st.container():
                                    st.markdown(f"""
                                    <div class='song-card'>
                                        <h4>{row['name'][:25]}{'...' if len(row['name']) > 25 else ''}</h4>
                                        <p><i>{row['artists'][:20]}{'...' if len(row['artists']) > 20 else ''}</i></p>
                                    """, unsafe_allow_html=True)
                                    
                                    song_data = spotify.get_track_data(row['name'], row['artists'])
                                    if song_data and song_data['image_url']:
                                        st.image(song_data['image_url'], use_column_width=True)
                                        if song_data['preview_url']:
                                            st.audio(song_data['preview_url'], format='audio/mp3')
                                    st.markdown("</div>", unsafe_allow_html=True)
            
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")
                st.code(f"Debug info: {os.listdir('data')}", language="bash")
=======
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
>>>>>>> e44f7887a4b612a2690fecef055aa0dfa01c5401

if __name__ == "__main__":
    main()
