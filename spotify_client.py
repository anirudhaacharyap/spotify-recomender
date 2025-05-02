import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self):
        # Hardcode your credentials here
        auth_manager = SpotifyClientCredentials(
            client_id="df65e30eb0e549c9818e908962326c83",  # Your actual client ID
            client_secret="a1c4819de7894decac88e1f1791eae87"  # Your actual secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_track_data(self, song_name, artist_name):
        """Get track data including URL, image and preview"""
        try:
            query = f"track:{song_name} artist:{artist_name}"
            results = self.sp.search(q=query, type='track', limit=1)

            if not results['tracks']['items']:
                return None

            track = results['tracks']['items'][0]
            return {
                'url': track['external_urls']['spotify'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'preview_url': track.get('preview_url')
            }
        except Exception:
            return None