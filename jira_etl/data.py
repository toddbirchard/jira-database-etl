import os
import json
from pandas.io.json import json_normalize
import pathlib


class JiraDataFrameConstructor:
    """Build JIRA issue DataFrame, piece by piece."""
    issue_count = 0

    @classmethod
    def construct_dataframe_for_upload(cls, issue_list_chunk):
        """Make DataFrame out of data received from JIRA API."""
        issue_list = [cls.make_issue_body(issue) for issue in issue_list_chunk]
        issue_json_list = [cls.dict_to_json_string(issue) for issue in issue_list]
        issues_df = json_normalize(issue_json_list)
        cls.export_csv_for_testing(issues_df)
        return issues_df

    @staticmethod
    def dict_to_json_string(issue_dict):
        """Convert dict to JSON to string."""
        issue_json_string = json.dumps(issue_dict)
        issue_json = json.loads(issue_json_string)
        return issue_json

    @classmethod
    def make_issue_body(cls, issue):
        """Create a JSON body for each ticket."""
        body = {
            'id': cls.issue_count,
            'key': str(issue['key']),
            'assignee': str(issue['fields']['assignee']['displayName']),
            'assignee_url': str(issue['fields']['assignee']['avatarUrls']['48x48']),
            'summary': str(issue['fields']['summary']),
            'status': str(issue['fields']['status']['name']),
            'priority': str(issue['fields']['priority']['name']),
            'priority_url': str(issue['fields']['priority']['iconUrl']),
            'priority_rank': int(issue['fields']['priority']['id']),
            'issuetype': str(issue['fields']['issuetype']['name']),
            'issuetype_icon': str(issue['fields']['issuetype']['iconUrl']),
            'epic_link': str(issue['fields']['customfield_10008']),
            'project': str(issue['fields']['project']['name']),
            'updated': issue['fields']['updated']
        }
        cls.issue_count += 1
        return body

    @staticmethod
    def export_csv_for_testing(issues_df):
        """Export test CSV of JIRA issues."""
        data_path = pathlib.Path('jira_etl/datafiles')
        csv_export_path = data_path / 'jiraissues.csv'
        csv_export_path = csv_export_path.resolve()
        print('csv_export_path = ', csv_export_path)
        issues_df.to_csv('jira_etl/datafiles/csv_export_path.csv')
