# Genre Pulse

A comprehensive music genre trend analysis and artist comparison system that provides weekly reports and detailed artist analyses.

## Features

- Automated data collection from Spotify, YouTube, and Last.fm
- AI-powered trend prediction using StatsForecast
- Detailed artist analysis and comparison
- FastAPI web service for report generation
- Docker-based deployment with monitoring
- Weekly automation with Prefect
- Comprehensive logging and error handling

## System Requirements

- Python 3.10 or higher
- Docker and Docker Compose
- API keys for Spotify, YouTube, and Last.fm

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/genre-pulse.git
cd genre-pulse
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API keys:
```ini
SPOTIFY_CLIENT_ID='your_spotify_client_id'
SPOTIFY_CLIENT_SECRET='your_spotify_client_secret'
YOUTUBE_API_KEY='your_youtube_api_key'
LASTFM_API_KEY='your_lastfm_api_key'
LASTFM_API_SECRET='your_lastfm_api_secret'
```

## Running the Application

### Development Mode

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation at `http://localhost:8000/docs`

### Production Mode with Docker

1. Build and start the containers:
```bash
docker-compose up --build -d
```

2. Access the services:
- API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## API Endpoints

- `GET /generate_report`: Generate the weekly genre pulse report
- `GET /download_report`: Download the latest report
- `GET /analyze_artist/{artist_name}`: Generate an analysis report for a specific artist
- `GET /health`: Check the health status of the API

## Monitoring

The application includes:
- Prometheus for metrics collection
- Grafana for visualization
- Redis for caching
- Health checks and logging

## Weekly Automation

The system can be automated using Prefect:
```bash
prefect deployment create automation.py:weekly_flow
prefect deployment run weekly_flow
```

## Report Format

The generated reports include:
- Breakout Genres
- Declining Genres
- Early Detection Radar
- Cross-Genre Flow
- Next Week Predictions
- Strategic Insights
- Artist Analysis (when requested)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Spotify API
- YouTube Data API
- Last.fm API
- StatsForecast
- FastAPI
- Docker
- Prometheus & Grafana
