import pytest

from validators import InputValidator
from exceptions import ValidationError


def test_valid_team_name():
    result = InputValidator.validate_team_name("Arsenal")

    assert result == "Arsenal"


def test_empty_team_name_raises_validation_error():
    with pytest.raises(ValidationError):
        InputValidator.validate_team_name("")


def test_invalid_team_name_characters():
    with pytest.raises(ValidationError):
        InputValidator.validate_team_name("Arsenal!!!###")


def test_valid_score():
    result = InputValidator.validate_score("3-1")

    assert result == "3-1"


def test_invalid_score():
    with pytest.raises(ValidationError):
        InputValidator.validate_score("three-one")


def test_empty_note():
    with pytest.raises(ValidationError):
        InputValidator.validate_note("")


def test_valid_match_id():
    result = InputValidator.validate_match_id("12345")

    assert result == "12345"


def test_invalid_match_id():
    with pytest.raises(ValidationError):
        InputValidator.validate_match_id("ABC123")


def test_valid_date():
    result = InputValidator.validate_date("2026-08-30")

    assert result == "2026-08-30"


def test_invalid_date_format():
    with pytest.raises(ValidationError):
        InputValidator.validate_date("30-08-2026")


def test_invalid_calendar_date():
    with pytest.raises(ValidationError):
        InputValidator.validate_date("2026-02-30")
