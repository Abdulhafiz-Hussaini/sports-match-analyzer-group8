from team import Team
from match import Match


team_data = {
    "idTeam": "133604",
    "strTeam": "   Arsenal     ",
    "strSport": "Soccer",
    "strLeague": "English Premier League",
    "strCountry": "England",
    "strBadge": "https://example.com/arsenal.png"
}


match_data = {
    "idEvent": "12345",
    "strHomeTeam": "Arsenal",
    "strAwayTeam": "Chelsea",
    "dateEvent": "2026-08-30",
    "strTime": "18:30:00",
    "intHomeScore": 2,
    "intAwayScore": 1,
    "strStatus": "Match Finished",
    "strVenue": "Emirates Stadium"
}


def test_team_from_api_dict():
    team = Team.from_api_dict(team_data)

    assert team.team_id == "133604"
    assert team.name == "Arsenal"
    assert team.sport == "Soccer"
    assert team.league == "English Premier League"
    assert team.country == "England"
    assert team.badge_url == "https://example.com/arsenal.png"


def test_match_from_api_dict():
    match = Match.from_api_dict(match_data)

    assert match.match_id == "12345"
    assert match.home_team == "Arsenal"
    assert match.away_team == "Chelsea"
    assert match.home_score == 2
    assert match.away_score == 1
    assert match.status == "Match Finished"
    assert match.venue == "Emirates Stadium"


def test_match_score_and_finished_status():
    match = Match.from_api_dict(match_data)

    assert match.score == "2-1"
    assert match.is_finished is True


def test_match_display_name():
    match = Match.from_api_dict(match_data)

    assert match.display_name() == "Arsenal vs Chelsea"


def test_match_result_for_team():
    match = Match.from_api_dict(match_data)

    assert match.result_for_team("Arsenal") == "Win"
    assert match.result_for_team("Chelsea") == "Loss"
