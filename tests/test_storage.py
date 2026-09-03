import json

import pytest

from storage import StorageManager
from team import Team
from exceptions import StorageError


@pytest.fixture
def team():
    return Team(
        team_id="133604",
        name="Arsenal",
        sport="Soccer",
        league="English Premier League",
        country="England",
        badge_url="https://example.com/arsenal.png"
    )


@pytest.fixture
def storage(tmp_path):
    filename = tmp_path / "test_user_data.json"
    return StorageManager(str(filename))


def test_add_favourite_team(storage, team):
    result = storage.add_favourite_team(team)

    assert result is True
    assert len(storage.get_favourite_teams()) == 1
    assert storage.get_favourite_teams()[0]["team_id"] == "133604"
    assert storage.get_favourite_teams()[0]["name"] == "Arsenal"


def test_duplicate_favourite_is_rejected(storage, team):
    storage.add_favourite_team(team)

    result = storage.add_favourite_team(team)

    assert result is False
    assert len(storage.get_favourite_teams()) == 1


def test_is_favourite(storage, team):
    assert storage.is_favourite("133604") is False

    storage.add_favourite_team(team)

    assert storage.is_favourite("133604") is True


def test_remove_favourite_team(storage, team):
    storage.add_favourite_team(team)

    result = storage.remove_favourite_team("133604")

    assert result is True
    assert storage.get_favourite_teams() == []
    assert storage.is_favourite("133604") is False


def test_remove_nonexistent_favourite(storage):
    result = storage.remove_favourite_team("999999")

    assert result is False


def test_save_and_get_match_note(storage):
    storage.save_match_note(
        "12345",
        "Important match. Watch the midfield performance."
    )

    result = storage.get_match_note("12345")

    assert result == (
        "Important match. Watch the midfield performance."
    )


def test_empty_match_note_raises_error(storage):
    with pytest.raises(
        StorageError,
        match="Match note cannot be empty"
    ):
        storage.save_match_note("12345", "")


def test_delete_match_note(storage):
    storage.save_match_note(
        "12345",
        "Important match."
    )

    result = storage.delete_match_note("12345")

    assert result is True
    assert storage.get_match_note("12345") is None


def test_delete_nonexistent_match_note(storage):
    result = storage.delete_match_note("99999")

    assert result is False


def test_save_and_get_summary(storage):
    storage.save_summary(
        "12345",
        "Arsenal showed strong attacking performance."
    )

    result = storage.get_summary("12345")

    assert result == (
        "Arsenal showed strong attacking performance."
    )


def test_empty_summary_raises_error(storage):
    with pytest.raises(
        StorageError,
        match="Summary cannot be empty"
    ):
        storage.save_summary("12345", "")


def test_delete_summary(storage):
    storage.save_summary(
        "12345",
        "Arsenal performed strongly."
    )

    result = storage.delete_summary("12345")

    assert result is True
    assert storage.get_summary("12345") is None


def test_delete_nonexistent_summary(storage):
    result = storage.delete_summary("99999")

    assert result is False


def test_data_persists_between_storage_instances(
    tmp_path,
    team
):
    filename = tmp_path / "persistent_data.json"

    storage = StorageManager(str(filename))

    storage.add_favourite_team(team)
    storage.save_match_note(
        "12345",
        "Watch the midfield."
    )
    storage.save_summary(
        "12345",
        "Arsenal showed strong attacking performance."
    )

    new_storage = StorageManager(str(filename))

    assert new_storage.is_favourite("133604") is True
    assert new_storage.get_match_note("12345") == (
        "Watch the midfield."
    )
    assert new_storage.get_summary("12345") == (
        "Arsenal showed strong attacking performance."
    )


def test_clear_all(storage, team):
    storage.add_favourite_team(team)
    storage.save_match_note(
        "12345",
        "Watch the midfield."
    )
    storage.save_summary(
        "12345",
        "Arsenal performed strongly."
    )

    storage.clear_all()

    assert storage.get_favourite_teams() == []
    assert storage.get_match_note("12345") is None
    assert storage.get_summary("12345") is None


def test_corrupted_json_raises_storage_error(tmp_path):
    filename = tmp_path / "corrupted.json"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("{invalid json")

    with pytest.raises(
        StorageError,
        match="invalid JSON"
    ):
        StorageManager(str(filename))


def test_invalid_json_structure_raises_storage_error(tmp_path):
    filename = tmp_path / "invalid_structure.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(["not", "a", "dictionary"], file)

    with pytest.raises(
        StorageError,
        match="must be stored as a JSON object"
    ):
        StorageManager(str(filename))
