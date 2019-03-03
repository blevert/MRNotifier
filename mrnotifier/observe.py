from rx import Observable

from mrnotifier.gitlab import get_merge_requests
from mrnotifier.config import ObserveConfig


class Observe:
    def __init__(self, scheduler=None):
        self._observerable = Observable \
            .interval(ObserveConfig.interval, scheduler) \
            .map(lambda dummy: get_merge_requests()) \
            .retry() \
            .publish() \
            .ref_count()

        self._ready_to_merge = self._observerable \
            .map(lambda requests: any([is_ready_to_merge(request) for request in requests])) \
            .start_with(False) \
            .distinct_until_changed()

    def on_ready_to_merge(self, on_next):
        self._ready_to_merge.subscribe(on_next)


def is_ready_to_merge(merge_request):
    return merge_request.is_work_in_progress() is False \
           and merge_request.get_votes_diff() >= ObserveConfig.upvotes_to_merge
