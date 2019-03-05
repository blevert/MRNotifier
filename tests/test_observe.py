from unittest.mock import patch, MagicMock

from mrnotifier.config import ObserveConfig
from mrnotifier.gitlab import MergeRequest
from mrnotifier.observe import Observe, is_ready_to_merge

from rx.testing import TestScheduler
from nose.tools import assert_equal


def test_is_ready_to_merge():
    ReadyToMergeTest().given(False, ObserveConfig.upvotes_to_merge, 0).then(True)
    ReadyToMergeTest().given(False, ObserveConfig.upvotes_to_merge, 1).then(False)
    ReadyToMergeTest().given(True, ObserveConfig.upvotes_to_merge, 0).then(False)
    ReadyToMergeTest().given(True, ObserveConfig.upvotes_to_merge, 1).then(False)


class ReadyToMergeTest:
    def __init__(self):
        self.mock = MergeRequest([])

    def given(self, work_in_progress, upvotes, downvotes):
        self.mock.is_work_in_progress = MagicMock(return_value=work_in_progress)
        self.mock.get_upvotes = MagicMock(return_value=upvotes)
        self.mock.get_downvotes = MagicMock(return_value=downvotes)
        return self

    def then(self, ready_to_merge):
        assert_equal(is_ready_to_merge(self.mock), ready_to_merge)


@patch('mrnotifier.observe.is_ready_to_merge')
@patch('mrnotifier.observe.get_merge_requests')
def test_on_ready_to_merge(mock_get_merge_requests, mock_is_ready_to_merge):
    test = OnReadyToMergeTest(mock_get_merge_requests, mock_is_ready_to_merge)
    test.when_interval_passed().then(False, 1)
    test.when_interval_passed().then(False, 1)

    test.when_ready_to_merge(True).then(False, 1)
    test.when_interval_passed().then(True, 2)
    test.when_interval_passed().then(True, 2)

    test.when_ready_to_merge(False).then(True, 2)
    test.when_interval_passed().then(False, 3)
    test.when_interval_passed().then(False, 3)


class OnReadyToMergeTest:
    def __init__(self, mock_get_merge_requests, mock_is_ready_to_merge):
        self._request_sample = MergeRequest([])
        self._mock_get_merge_requests = mock_get_merge_requests
        self._mock_get_merge_requests.return_value = [self._request_sample]

        self._mock_is_ready_to_merge = mock_is_ready_to_merge
        self._mock_is_ready_to_merge.return_value = False

        self._notifications = []

        self._request_count = 0

        self._scheduler = TestScheduler()
        Observe(self._scheduler).on_ready_to_merge(lambda value: self._notifications.append(value))

    def when_interval_passed(self):
        self._scheduler.advance_by(ObserveConfig.interval)
        self._request_count = self._request_count + 1
        return self

    def when_ready_to_merge(self, ready_to_merge):
        self._mock_is_ready_to_merge.return_value = ready_to_merge
        return self

    def then(self, ready_to_merge, notifications_count):
        assert_equal(self._notifications[-1], self._request_sample if ready_to_merge else None)
        assert_equal(len(self._notifications), notifications_count)
        assert_equal(self._mock_is_ready_to_merge.call_count, self._request_count)
