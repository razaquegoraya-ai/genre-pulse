import os
from fastapi import FastAPI
from genre_analysis import GenrePulseAnalyzer

app = FastAPI()
analyzer = GenrePulseAnalyzer()

@app.get("/generate_report")
def get_report():
    analyzer.analyze_trends()
    analyzer.save_report()
    return {"report": "✅ Weekly Genre Pulse Report Generated"}

@app.get("/health")
def health_check():
    return {
        "status": "✅ API is running",
        "data_directory_exists": os.path.exists('./data'),
        "report_directory_exists": os.path.exists('./reports')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
