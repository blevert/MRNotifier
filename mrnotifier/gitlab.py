from urllib.parse import urljoin

import requests
import logging

from mrnotifier.config import GitlabConfig

_api = urljoin(GitlabConfig.url, 'api/v4/')
_merge_endpoint = urljoin(_api, 'merge_requests?state={state}&scope={scope}')
_award_endpoint = urljoin(
    _api, 'projects/{project_id}/merge_requests/{merge_request_iid}/award_emoji')

_session = requests.Session()
_session.verify = GitlabConfig.verifySSL
_session.headers.update({'private-token': GitlabConfig.token})

requests.packages.urllib3.disable_warnings(
    category=requests.packages.urllib3.exceptions.InsecureRequestWarning)


class JsonContainer:
    def __init__(self, json):
        self.json = json

    def __str__(self):
        return str(self.json)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.json == other.json


class MergeRequest(JsonContainer):
    def __init__(self, json):
        super().__init__(json)

    def get_iid(self):
        return self.json['iid']

    def is_work_in_progress(self):
        return self.json['work_in_progress'] is True

    def get_upvotes(self):
        return self.json['upvotes']

    def get_downvotes(self):
        return self.json['downvotes']

    def get_votes_diff(self):
        return self.get_upvotes() - self.get_downvotes()

    def has_any_votes(self):
        return self.get_upvotes() > 0 or self.get_downvotes() > 0

    def get_web_url(self):
        return self.json['web_url']

    def get_awards(self):
        project_id = self.json['project_id']
        url = _award_endpoint.format(
            project_id=project_id, merge_request_iid=self.get_iid())
        return [Award(award) for award in _get_response_json(url)]


class AwardAuthor(JsonContainer):
    def __init__(self, json):
        super().__init__(json)

    def get_name(self):
        return self.json['name']

    def get_avatar_url(self):
        return self.json['avatar_url']


class Award(JsonContainer):
    def __init__(self, json):
        super().__init__(json)

    def get_id(self):
        return self.json['id']

    def get_emoji(self):
        return self.json['name']

    def get_author(self) -> AwardAuthor:
        return AwardAuthor(self.json['user'])


def get_merge_requests(state='opened', scope='assigned_to_me'):
    url = _merge_endpoint.format(state=state, scope=scope)
    return [MergeRequest(mr) for mr in _get_response_json(url)]


def _get_response_json(url):
    try:
        response = _session.get(url)
        if response.ok:
            return response.json()
    except requests.exceptions.RequestException as err:
        logging.error(err)

    return ""
