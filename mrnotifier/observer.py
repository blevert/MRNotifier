from rx import Observable

from mrnotifier.gitlab import get_merge_requests
from mrnotifier.config import ObserveConfig


_observerable = Observable \
    .interval(ObserveConfig.interval) \
    .map(lambda dummy: get_merge_requests()) \
    .retry()

_ready_to_merge = _observerable \
    .map(lambda all_requests: any([_is_ready_to_merge(mr) for mr in all_requests])) \
    .start_with(False) \
    .distinct_until_changed()


def _is_ready_to_merge(merge_request):
    return merge_request.is_work_in_progress() is False \
           and merge_request.get_votes_diff() >= ObserveConfig.upvotes_to_merge


def on_ready_to_merge(on_next):
    _ready_to_merge.subscribe(on_next)
