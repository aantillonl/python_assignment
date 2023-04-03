import json
from unittest.mock import MagicMock
from jsonschema import validate
import pytest

from ctw_assignment.get_raw_data import get_raw_data

@pytest.fixture
def  schema():
    with open("src/ctw_assignment/api_response_schema.json", "rb") as f:
        yield json.load(f)


@pytest.fixture
def test_response():
    with open("tests/data/test_response.json", "rb") as f:
        yield json.load(f)


def test_schema(schema, test_response):
    validate(test_response, schema)


def test_get_raw_data():
    session_mock = MagicMock()
    response = session_mock.get.return_value
    response.json.return_value = test_response
    assert get_raw_data(session_mock, "test_apikey", "TEST_COMP") == test_response


def test_get_raw_data_raise(test_response):
    session_mock = MagicMock()
    response = session_mock.get.return_value
    response.raise_for_status.side_effect = Exception("Test")
    with pytest.raises(Exception):
        get_raw_data(session_mock, "test_apikey", "TEST_COMP")