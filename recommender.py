import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class SongRecommender:
    def __init__(self, data_path):
        self.df, self.feature_cols = self._load_data(data_path)

    def _load_data(self, path):
        """Load and preprocess the dataset"""
        df = pd.read_csv(path)
        df['artists'] = df['artists'].str.replace(r"['\[\]]", '', regex=True)

        feature_columns = [
            "danceability", "energy", "acousticness", "instrumentalness",
            "liveness", "valence", "loudness", "speechiness", "tempo"
        ]

        # Normalize tempo
        df['tempo_normalized'] = (df['tempo'] - df['tempo'].min()) / (df['tempo'].max() - df['tempo'].min())
        feature_columns.append('tempo_normalized')

        return df, feature_columns

    def get_song_list(self):
        """Get list of available songs for dropdown"""
        return self.df["name"].unique()

    def recommend_songs(self, song_name, top_n=5):
        """Recommend similar songs based on audio features"""
        if song_name not in self.df["name"].values:
            return pd.DataFrame()

        features = self.df[self.feature_cols]
        song_idx = self.df[self.df["name"] == song_name].index[0]
        similarity = cosine_similarity([features.iloc[song_idx]], features)[0]
        similar_indices = similarity.argsort()[::-1][1:top_n + 1]
        return self.df.iloc[similar_indices][["name", "artists"]]