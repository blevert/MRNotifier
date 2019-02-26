import json


def get_example_merge_requests():
    with open('tests/resources/merge_requests.json') as f:
        return json.load(f)[0]


def get_example_award_emoji():
    with open('tests/resources/award_emoji.json') as f:
        return json.load(f)[0]
