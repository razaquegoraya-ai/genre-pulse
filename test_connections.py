from data_collector import GenreDataCollector

def test_api_connections():
    collector = GenreDataCollector()
    data = collector.collect_all_data(days=1)

    assert data['spotify'] is not None, "❌ Spotify API failed"
    assert data['youtube'] is not None, "❌ YouTube API failed"
    assert data['lastfm'] is not None, "❌ Last.fm API failed"

    print("✅ All API connections successful.")

if __name__ == "__main__":
    test_api_connections()
