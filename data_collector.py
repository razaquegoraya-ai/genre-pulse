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

    def fetch_data(self, url, headers=None):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            time.sleep(5)
            return None

    def collect_all_data(self, days=7):
        logging.info(f"Collecting data for the past {days} days")

        # Placeholder endpoints – replace with real authenticated calls
        spotify_data = self.fetch_data("https://api.spotify.com/v1/placeholder")
        youtube_data = self.fetch_data(
            f"https://www.googleapis.com/youtube/v3/videos?key={YOUTUBE_API_KEY}"
        )
        lastfm_data = self.fetch_data(
            f"http://ws.audioscrobbler.com/2.0/?api_key={LASTFM_API_KEY}&method=chart.gettoptracks&format=json"
        )

        return {
            "spotify": spotify_data,
            "youtube": youtube_data,
            "lastfm": lastfm_data
        }

if __name__ == "__main__":
    collector = GenreDataCollector()
    collector.collect_all_data()
