import pytest
from unittest.mock import Mock

from sports_api_client import SportsAPIClient
from exceptions import (
    SportsAPIError,
    TeamNotFoundError,
)
from team import Team
from match import Match


def test_search_team_returns_team_objects():
    client = SportsAPIClient()

    client._get = Mock(return_value={
        "teams": [
            {
                "idTeam": "133604",
                "strTeam": "Arsenal",
                "strSport": "Soccer",
                "strLeague": "English Premier League",
                "strCountry": "England",
                "strTeamBadge": "https://example.com/arsenal.png",
            }
        ]
    })

    teams = client.search_team("Arsenal")

    assert len(teams) == 1
    assert isinstance(teams[0], Team)
    assert teams[0].name == "Arsenal"
    assert teams[0].team_id == "133604"

    client._get.assert_called_once()


def test_search_team_raises_when_team_not_found():
    client = SportsAPIClient()

    client._get = Mock(return_value={
        "teams": None
    })

    with pytest.raises(TeamNotFoundError):
        client.search_team("ThisTeamDefinitelyDoesNotExist123456")


def test_get_next_events_returns_match_objects():
    client = SportsAPIClient()

    client._get = Mock(return_value={
        "events": [
            {
                "idEvent": "999001",
                "strHomeTeam": "Arsenal",
                "strAwayTeam": "Chelsea",
                "dateEvent": "2026-09-06",
                "strTime": "15:30:00",
                "intHomeScore": None,
                "intAwayScore": None,
                "strStatus": "NS",
                "strVenue": "Emirates Stadium",
            }
        ]
    })

    matches = client.get_next_events("133604")

    assert len(matches) == 1
    assert isinstance(matches[0], Match)
    assert matches[0].home_team == "Arsenal"
    assert matches[0].away_team == "Chelsea"
    assert matches[0].status == "NS"


def test_get_last_events_returns_match_objects():
    client = SportsAPIClient()

    client._get = Mock(return_value={
        "results": [
            {
                "idEvent": "999002",
                "strHomeTeam": "Arsenal",
                "strAwayTeam": "Chelsea",
                "dateEvent": "2026-08-20",
                "strTime": "18:00:00",
                "intHomeScore": "2",
                "intAwayScore": "1",
                "strStatus": "FT",
                "strVenue": "Emirates Stadium",
            }
        ]
    })

    matches = client.get_last_events("133604")

    assert len(matches) == 1
    assert isinstance(matches[0], Match)
    assert matches[0].score == "2-1"
    assert matches[0].is_finished is True


def test_get_next_events_requires_team_id():
    client = SportsAPIClient()

    with pytest.raises(SportsAPIError):
        client.get_next_events("")


def test_get_last_events_requires_team_id():
    client = SportsAPIClient()

    with pytest.raises(SportsAPIError):
        client.get_last_events("")


def test_get_team_matches_returns_both_sections():
    client = SportsAPIClient()

    upcoming_match = Mock()
    recent_match = Mock()

    client.get_next_events = Mock(
        return_value=[upcoming_match]
    )
    client.get_last_events = Mock(
        return_value=[recent_match]
    )

    team = Team(
        team_id="133604",
        name="Arsenal",
        sport="Soccer",
        league="English Premier League",
        country="England",
        badge_url=None,
    )

    result = client.get_team_matches(team)

    assert "upcoming" in result
    assert "recent" in result
    assert result["upcoming"] == [upcoming_match]
    assert result["recent"] == [recent_match]

    client.get_next_events.assert_called_once_with("133604")
    client.get_last_events.assert_called_once_with("133604")


def test_get_team_matches_rejects_invalid_team():
    client = SportsAPIClient()

    with pytest.raises(TypeError):
        client.get_team_matches("Arsenal")
