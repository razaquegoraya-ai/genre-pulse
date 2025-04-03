import os
import time
import logging
import requests
from config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    YOUTUBE_API_KEY,
    LASTFM_API_KEY,
    LASTFM_API_SECRET,
)

logging.basicConfig(
    level=logging.INFO,
    filename="genre_analysis.log",
    format="%(asctime)s %(levelname)s: %(message)s"
)

class GenreDataCollector:
    def __init__(self, data_directory="./data"):
        self.data_directory = data_directory
        os.makedirs(self.data_directory, exist_ok=True)
        self.spotify_token = None

    def get_spotify_token(self):
        if not self.spotify_token:
            auth_url = "https://accounts.spotify.com/api/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": SPOTIFY_CLIENT_ID,
                "client_secret": SPOTIFY_CLIENT_SECRET,
            }
            response = requests.post(auth_url, data=auth_data)
            if response.status_code == 200:
                self.spotify_token = response.json()["access_token"]
            else:
                logging.error("Failed to get Spotify token")
                return None
        return self.spotify_token

    def fetch_data(self, url, headers=None, params=None):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            time.sleep(5)
            return None

    def collect_spotify_data(self):
        token = self.get_spotify_token()
        if not token:
            return None

        headers = {"Authorization": f"Bearer {token}"}
        
        # Get Nova Sound's artist data
        nova_sound_data = self.fetch_data(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params={"q": "Nova Sound", "type": "artist", "limit": 1}
        )

        # Get audio features for comparison artists
        comparison_artists = ["Coldplay", "Imagine Dragons", "Maroon 5"]
        artist_data = {}
        
        for artist in comparison_artists:
            artist_search = self.fetch_data(
                "https://api.spotify.com/v1/search",
                headers=headers,
                params={"q": artist, "type": "artist", "limit": 1}
            )
            if artist_search and "artists" in artist_search:
                artist_id = artist_search["artists"]["items"][0]["id"]
                top_tracks = self.fetch_data(
                    f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
                    headers=headers,
                    params={"market": "US"}
                )
                artist_data[artist] = top_tracks

        return {
            "nova_sound": nova_sound_data,
            "comparison_artists": artist_data
        }

    def collect_youtube_data(self):
        # Get Nova Sound's YouTube data
        nova_sound_data = self.fetch_data(
            "https://www.googleapis.com/youtube/v3/search",
            params={
                "key": YOUTUBE_API_KEY,
                "q": "Nova Sound",
                "part": "snippet",
                "type": "video",
                "maxResults": 10
            }
        )

        # Get comparison artists' data
        comparison_artists = ["Coldplay", "Imagine Dragons", "Maroon 5"]
        artist_data = {}
        
        for artist in comparison_artists:
            artist_data[artist] = self.fetch_data(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "key": YOUTUBE_API_KEY,
                    "q": artist,
                    "part": "snippet",
                    "type": "video",
                    "maxResults": 10
                }
            )

        return {
            "nova_sound": nova_sound_data,
            "comparison_artists": artist_data
        }

    def collect_lastfm_data(self):
        # Get Nova Sound's Last.fm data
        nova_sound_data = self.fetch_data(
            "http://ws.audioscrobbler.com/2.0/",
            params={
                "method": "artist.getInfo",
                "artist": "Nova Sound",
                "api_key": LASTFM_API_KEY,
                "format": "json"
            }
        )

        # Get comparison artists' data
        comparison_artists = ["Coldplay", "Imagine Dragons", "Maroon 5"]
        artist_data = {}
        
        for artist in comparison_artists:
            artist_data[artist] = self.fetch_data(
                "http://ws.audioscrobbler.com/2.0/",
                params={
                    "method": "artist.getInfo",
                    "artist": artist,
                    "api_key": LASTFM_API_KEY,
                    "format": "json"
                }
            )

        return {
            "nova_sound": nova_sound_data,
            "comparison_artists": artist_data
        }

    def collect_all_data(self, days=7):
        logging.info(f"Collecting data for the past {days} days")

        spotify_data = self.collect_spotify_data()
        youtube_data = self.collect_youtube_data()
        lastfm_data = self.collect_lastfm_data()

        return {
            "spotify": spotify_data,
            "youtube": youtube_data,
            "lastfm": lastfm_data
        }

if __name__ == "__main__":
    collector = GenreDataCollector()
    collector.collect_all_data()
