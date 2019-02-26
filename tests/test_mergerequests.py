from unittest.mock import patch

from nose.tools import assert_is_not_none, assert_equal, assert_list_equal, assert_true

from mrnotifier.gitlab import get_merge_requests, MergeRequest
from tests.utils import get_example_merge_requests


@patch('tests.test_mergerequests.get_merge_requests')
def test_mocking(mock_get_merge_requests):
    get_merge_requests()
    assert_true(mock_get_merge_requests.called)


@patch('mrnotifier.gitlab.requests.Session.get')
def test_get_merge_requests_is_ok(mock_get):
    example_request = get_example_merge_requests()
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = [example_request]

    response = get_merge_requests()
    assert_is_not_none(response)
    assert_equal(response, [MergeRequest(example_request)])

    assert_true(mock_get.called)


@patch('mrnotifier.gitlab.requests.Session.get')
def test_get_opened_merge_requests_is_not_ok(mock_get):
    mock_get.return_value.ok = False
    response = get_merge_requests()
    assert_list_equal(response, [])
