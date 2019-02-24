from urllib.parse import urljoin

import requests

from mrnotifier.config import GitlabConfig

_api = urljoin(GitlabConfig.url, 'api/v4/')
_merge_endpoint = urljoin(_api, 'merge_requests?state={state}&scope={scope}')
_award_endpoint = urljoin(_api, 'projects/{project_id}/merge_requests/{merge_request_iid}/award_emoji')

_session = requests.Session()
_session.verify = GitlabConfig.verifySSL
_session.headers.update({'private-token': GitlabConfig.token})


class JsonContainer:
    def __init__(self, json):
        self.json = json

    def __eq__(self, other):
        return self.json == other.json


class MergeRequest(JsonContainer):
    def __init__(self, json):
        super().__init__(json)

    def is_work_in_progress(self):
        return self.json['work_in_progress'] is True

    def get_upvotes(self):
        return self.json['upvotes']

    def get_downvotes(self):
        return self.json['downvotes']

    def get_votes_diff(self):
        return self.get_upvotes() - self.get_downvotes()

    def get_web_url(self):
        return self.json['web_url']

    def get_awards(self):
        project_id = self.json['project_id']
        merge_request_iid = self.json['merge_request_iid']
        url = _award_endpoint.format(project_id=project_id, merge_request_iid=merge_request_iid)
        response = _session.get(url)
        if response.ok:
            return [Award(award) for award in response.json()]
        else:
            return []

    def __eq__(self, other):
        return self.json == other.json


class Award(JsonContainer):
    def __init__(self, json):
        super().__init__(json)

    def get_author(self):
        return AwardAuthor(self.json['user'])


class AwardAuthor(JsonContainer):
    def __init__(self, json):
        super().__init__(json)

    def get_name(self):
        return self.json['name']

    def get_avatar_url(self):
        return self.json['avatar_url']


def get_merge_requests(state='opened', scope='assigned_to_me'):
    url = _merge_endpoint.format(state=state, scope=scope)
    response = _session.get(url)
    if response.ok:
        return [MergeRequest(mr) for mr in response.json()]
    else:
        return []
