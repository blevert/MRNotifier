# Standard library imports...
from unittest.mock import patch
import json

# Third-party imports...
from nose.tools import assert_is_not_none, assert_equal, assert_list_equal

# Local imports...
from mrnotifier.gitlab import get_merge_requests, MergeRequest, Award
from mrnotifier.config import TrayConfig


@patch('mrnotifier.gitlab.requests.Session.get')
def test_get_merge_requests_is_ok(mock_get):
    example_request = get_example_merge_requests()
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = [example_request]

    response = get_merge_requests()
    assert_is_not_none(response)
    assert_equal(response, [MergeRequest(example_request)])


@patch('mrnotifier.gitlab.requests.Session.get')
def test_get_opened_merge_requests_is_not_ok(mock_get):
    mock_get.return_value.ok = False
    response = get_merge_requests()
    assert_list_equal(response, [])


def get_example_merge_requests():
    with open('tests/resources/merge_requests.json') as f:
        return json.load(f)[0]


def get_example_award_emoji():
    with open('tests/resources/award_emoji.json') as f:
        return json.load(f)[0]
