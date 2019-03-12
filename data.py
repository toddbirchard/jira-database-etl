import pandas as pd
from pandas.io.json import json_normalize
import json


class JiraDataframeConstructor:
    """Build JIRA issue Dataframe, piece by piece."""

    @staticmethod
    def dict_to_json_string(issue_dict):
        """Converts dict to JSON to string."""
        issue_json_string = json.dumps(issue_dict)
        issue_json = json.loads(issue_json_string)
        return issue_json

    @classmethod
    def add_issues_to_dataframe(cls, issue_list_chunk):
        """Make DataFrame out of JSON."""
        issue_list = [cls.make_issue_body(issue) for issue in issue_list_chunk]
        issue_json_list = [cls.dict_to_json_string(issue) for issue in issue_list]
        jira_df = json_normalize(issue_json_list)
        return jira_df

    @staticmethod
    def make_issue_body(issue):
        """Create a JSON body for each ticket."""
        body = {
            'key': issue['key'],
            'assignee': issue['fields']['assignee']['displayName'],
            'assignee_url': issue['fields']['assignee']['avatarUrls']['48x48'],
            'summary': issue['fields']['summary'],
            'status': issue['fields']['status']['name'],
            'priority': issue['fields']['priority']['name'],
            'priority_url': issue['fields']['priority']['iconUrl'],
            'priority_rank': issue['fields']['priority']['id'],
            'issuetype': issue['fields']['issuetype']['name'],
            'issuetype_icon': issue['fields']['issuetype']['iconUrl'],
            'epic_link': issue['fields']['customfield_10008'],
            'project': issue['fields']['project']['name'],
            'updated': issue['fields']['updated']
        }
        return body
