from prefect import task, flow
from genre_analysis import GenrePulseAnalyzer
from data_collector import GenreDataCollector

collector = GenreDataCollector()
analyzer = GenrePulseAnalyzer()

@task
def collect_and_analyze():
    data = collector.collect_all_data(days=7)
    analyzer.process_api_data(data["spotify"], data["youtube"], data["lastfm"])
    analyzer.analyze_trends()
    analyzer.save_report()

@flow
def weekly_flow():
    collect_and_analyze()

if __name__ == "__main__":
    weekly_flow()
