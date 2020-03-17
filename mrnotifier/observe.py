import logging
import rx

from rx import Observable
from rx import operators as ops

from mrnotifier.gitlab import get_merge_requests
from mrnotifier.config import ObserveConfig


class Observe:
    def __init__(self, scheduler=None):
        self._observerable = rx.interval(ObserveConfig.interval, scheduler).pipe(
            ops.map(lambda dummy: get_merge_requests()),
            ops.retry(),
            ops.publish(),
            ops.ref_count()
        )

        self._ready_to_merge = self._observerable.pipe(
            ops.map(lambda requests: next((request for request in requests if is_ready_to_merge(request)), None)),
            ops.start_with(None),
            ops.distinct_until_changed()
        )

        self._ready_to_merge.subscribe(lambda ready_to_merge: logging.info('Ready to merge: ' + str(ready_to_merge)))

        voted_merge_requests = self._observerable.pipe(
            ops.map(_to_voted_merge_requests_set)
        )
        self._new_votes_merge_requests = voted_merge_requests.pipe(
            ops.skip(1),
            ops.zip(voted_merge_requests),
            ops.map(lambda zipped: zipped[0] - zipped[1]),
            ops.filter(len),
            ops.map(_to_merge_requests)
        )

        self._new_votes_merge_requests.pipe(
            ops.map(lambda diff_set: [merge_request.get_iid() for merge_request in diff_set]) 
        ).subscribe(lambda ids: logging.info(f'New votes for merge requests: {ids}'))

        awards = self._new_votes_merge_requests.pipe(
            ops.map(_to_awards_set),
            ops.publish(),
            ops.ref_count(),
            ops.start_with(set())
        )
        self._new_awards = awards.pipe(
            ops.skip(1),
            ops.zip(awards),
            ops.map(lambda zipped: zipped[0] - zipped[1]),
            ops.filter(len),
            ops.flat_map(lambda diff_set: rx.from_iterable(diff_set)),
            ops.map(lambda award_key: award_key.award)
        )

        self._new_awards.subscribe(lambda new_award: logging.info('New award: ' + str(new_award)))

    def on_ready_to_merge(self, on_next):
        self._ready_to_merge.subscribe(on_next)


def _to_voted_merge_requests_set(merge_requests):
    return {MergeRequestKey(merge_request) for merge_request in merge_requests if merge_request.has_any_votes()}


def _to_merge_requests(voted_merge_requests_set):
    return [merge_request_key.merge_request for merge_request_key in voted_merge_requests_set]


class HashableKey:
    def __init__(self, key):
        self._key = key

    def __hash__(self):
        return self._key.__hash__()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._key == other._key


class MergeRequestKey(HashableKey):
    def __init__(self, merge_request):
        key = merge_request.get_iid(), merge_request.get_upvotes(), merge_request.get_downvotes()
        super().__init__(key)
        self.merge_request = merge_request


def _to_awards_set(merge_requests):
    return {AwardKey(award) for merge_request in merge_requests for award in merge_request.get_awards()}


class AwardKey(HashableKey):
    def __init__(self, award):
        super().__init__(award.get_id())
        self.award = award


def is_ready_to_merge(merge_request):
    return merge_request.is_work_in_progress() is False \
           and merge_request.get_votes_diff() >= ObserveConfig.upvotes_to_merge
