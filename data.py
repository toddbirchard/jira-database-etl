import pandas as pd
from pandas.io.json import json_normalize
import json


def dict_to_json_string(issue_dict):
    """Converts dict to JSON to string."""
    issue_json_string = json.dumps(issue_dict)
    issue_json = json.loads(issue_json_string)
    return issue_json


def create_issues_dataframe(issues_json):
    """Make DataFrame out of JSON."""
    headers = ['key', 'assignee', 'summary', 'status', 'priority', 'rank', 'issuetype', 'epic_link', 'project', 'updated', 'timestamp']
    issue_list = [make_issue_body(issue) for issue in issues_json['issues']]
    issue_json_list = [dict_to_json_string(issue) for issue in issue_list]
    jira_df = json_normalize(issue_json_list)
    print(jira_df)
    jira_df.to_csv('jiratest.csv')


def make_issue_body(issue):
    """Create a JSON body for each ticket."""
    body = {
        'key': issue['key'],
        'assignee': issue['fields']['assignee']['displayName'],
        'summary': issue['fields']['summary'],
        'status': issue['fields']['status']['name'],
        'priority': issue['fields']['priority']['name'],
        'rank': issue['fields']['priority']['id'],
        'issuetype': issue['fields']['issuetype']['name'],
        'epic_link': issue['fields']['customfield_10008'],
        'project': issue['fields']['project']['name'],
        'updated': issue['fields']['updated']
    }
    return body
