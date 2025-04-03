import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from genre_analysis import GenrePulseAnalyzer
from data_collector import GenreDataCollector

app = FastAPI(
    title="Genre Pulse API",
    description="API for generating music genre trend reports and artist analysis",
    version="1.0.0"
)

analyzer = GenrePulseAnalyzer()
collector = GenreDataCollector()

@app.get("/generate_report")
async def get_report():
    try:
        # Collect data from all sources
        data = collector.collect_all_data()
        
        # Process the data
        analyzer.process_api_data(
            data["spotify"],
            data["youtube"],
            data["lastfm"]
        )
        
        # Analyze trends and generate report
        analyzer.analyze_trends()
        analyzer.save_report()
        
        return {
            "status": "success",
            "message": "✅ Weekly Genre Pulse Report Generated",
            "report_path": "./reports/weekly_genre_pulse.md"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download_report")
async def download_report():
    report_path = "./reports/weekly_genre_pulse.md"
    if not os.path.exists(report_path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(
        report_path,
        media_type="text/markdown",
        filename="weekly_genre_pulse.md"
    )

@app.get("/analyze_artist/{artist_name}")
async def analyze_artist(artist_name: str):
    try:
        # Collect data for the specific artist
        data = collector.collect_all_data()
        
        # Process and analyze the data
        analyzer.process_api_data(
            data["spotify"],
            data["youtube"],
            data["lastfm"]
        )
        
        # Generate artist-specific report
        report_path = f"./reports/{artist_name.lower().replace(' ', '_')}_analysis.md"
        analyzer.save_report(filename=report_path)
        
        return {
            "status": "success",
            "message": f"✅ {artist_name} Analysis Report Generated",
            "report_path": report_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {
        "status": "✅ API is running",
        "data_directory_exists": os.path.exists('./data'),
        "report_directory_exists": os.path.exists('./reports'),
        "services": {
            "spotify": collector.get_spotify_token() is not None,
            "youtube": YOUTUBE_API_KEY is not None,
            "lastfm": LASTFM_API_KEY is not None
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
