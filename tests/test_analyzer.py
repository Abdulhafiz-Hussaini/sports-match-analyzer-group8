from match import Match
from match_analyzer import MatchAnalyzer


arsenal_matches = [
    Match(
        "1",
        "Arsenal",
        "Chelsea",
        "2026-08-20",
        home_score=3,
        away_score=1
    ),
    Match(
        "2",
        "Liverpool",
        "Arsenal",
        "2026-08-16",
        home_score=2,
        away_score=2
    ),
    Match(
        "3",
        "Arsenal",
        "Newcastle",
        "2026-08-10",
        home_score=2,
        away_score=0
    ),
    Match(
        "4",
        "Manchester City",
        "Arsenal",
        "2026-08-03",
        home_score=1,
        away_score=0
    ),
    Match(
        "5",
        "Arsenal",
        "Everton",
        "2026-07-27",
        home_score=2,
        away_score=1
    )
]


chelsea_matches = [
    Match(
        "6",
        "Chelsea",
        "Liverpool",
        "2026-08-20",
        home_score=1,
        away_score=2
    ),
    Match(
        "7",
        "Chelsea",
        "Newcastle",
        "2026-08-16",
        home_score=2,
        away_score=2
    ),
    Match(
        "8",
        "Everton",
        "Chelsea",
        "2026-08-10",
        home_score=0,
        away_score=1
    ),
    Match(
        "9",
        "Chelsea",
        "West Ham",
        "2026-08-03",
        home_score=3,
        away_score=1
    ),
    Match(
        "10",
        "Manchester City",
        "Chelsea",
        "2026-07-27",
        home_score=2,
        away_score=0
    )
]


def test_analyze_form():
    analyzer = MatchAnalyzer("Arsenal")

    stats = analyzer.analyze_form(arsenal_matches)

    assert stats["team"] == "Arsenal"
    assert stats["matches"] == 5
    assert stats["wins"] == 3
    assert stats["draws"] == 1
    assert stats["losses"] == 1
    assert stats["goals_scored"] == 9
    assert stats["goals_conceded"] == 5
    assert stats["points"] == 10


def test_form_string():
    analyzer = MatchAnalyzer("Arsenal")

    form = analyzer.form_string(arsenal_matches)

    assert form == "W D W L W"


def test_predict_match():
    analyzer = MatchAnalyzer("Arsenal")

    prediction = analyzer.predict_match(
        "Chelsea",
        arsenal_matches,
        chelsea_matches
    )

    assert prediction["prediction"] == "Draw"
    assert prediction["result"] == "Draw"
    assert prediction["confidence"] == 65.0
    assert prediction["team_average"] == 2.0
    assert prediction["opponent_average"] == 1.4
    assert "not a guaranteed prediction" in prediction["message"]
