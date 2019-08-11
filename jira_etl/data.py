import json
from pandas.io.json import json_normalize
from datetime import datetime


class TransformData:
    """Build JIRA issue DataFrame.

    1. Loop through JIRA issues and create a dictionary of desired data.
    2. Convert each issue dictionary into a JSON object.
    3. Load all issues into a Pandas DataFrame.
    """

    issue_count = 0

    @classmethod
    def construct_dataframe(cls, issue_list_chunk):
        """Make DataFrame out of data received from JIRA API."""
        issue_list = [cls.make_issue_body(issue) for issue in issue_list_chunk]
        issue_json_list = [cls.dict_to_json_string(issue) for issue in issue_list]
        jira_issues_df = json_normalize(issue_json_list)
        return jira_issues_df

    @staticmethod
    def dict_to_json_string(issue_dict):
        """Convert dict to JSON to string."""
        issue_json_string = json.dumps(issue_dict)
        issue_json = json.loads(issue_json_string)
        return issue_json

    @classmethod
    def make_issue_body(cls, issue):
        """Create a JSON body for each ticket."""
        updated_date = datetime.strptime(issue['fields']['updated'], "%Y-%m-%dT%H:%M:%S.%f%z")
        body = {
            'id': str(cls.issue_count),
            'key': str(issue['key']),
            'assignee_name': str(issue['fields']['assignee']['displayName']),
            'assignee_url': str(issue['fields']['assignee']['avatarUrls']['48x48']),
            'summary': str(issue['fields']['summary']),
            'status': str(issue['fields']['status']['name']).replace(' ', ''),
            'priority_url': str(issue['fields']['priority']['iconUrl']),
            'priority_rank': int(issue['fields']['priority']['id']),
            'issuetype_name': str(issue['fields']['issuetype']['name']),
            'issuetype_icon': str(issue['fields']['issuetype']['iconUrl']),
            'epic_link': str(issue['fields']['customfield_10008']),
            'project': str(issue['fields']['project']['name']),
            'updated': int(datetime.timestamp(updated_date)),
            'updatedAt': str(updated_date)
        }
        cls.issue_count += 1
        return body
