import os
from genre_analysis import GenrePulseAnalyzer

def test_report_generation():
    analyzer = GenrePulseAnalyzer()
    analyzer.analyze_trends()
    analyzer.save_report()

    assert os.path.exists("./reports/weekly_genre_pulse.md"), "❌ Report was not generated"
    print("✅ Report successfully generated.")

if __name__ == "__main__":
    test_report_generation()
