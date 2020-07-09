import json
from pandas.io.json import json_normalize
from datetime import datetime
from collections import defaultdict


class TransformData:
    """Build JIRA issue DataFrame from raw JSON respsone."""

    def construct_dataframe(self, issues_json):
        """Make DataFrame out of data received from JIRA API."""
        issue_list = [self.make_issue_body(issue) for issue in issues_json]
        issue_json_list = [self.dict_to_json_string(issue) for issue in issue_list]
        jira_issues_df = json_normalize(issue_json_list)
        return jira_issues_df

    @staticmethod
    def dict_to_json_string(issue_dict):
        """Convert dict to JSON to string."""
        issue_json_string = json.dumps(issue_dict)
        issue_json = json.loads(issue_json_string)
        return issue_json

    def make_issue_body(self, issue):
        """Create a JSON body for each ticket."""
        updated_date = issue['fields'].get('updated', None)
        created_date = issue['fields'].get('created', None)
        body = defaultdict(None)
        body['id'] = issue['fields'].get('id', {})
        body['key'] = issue.get('key')
        body['summary'] = str(issue['fields'].get('summary'))
        body['status'] = issue['fields'].get('status', {}).get('name', {})
        body['priority_rank'] = issue['fields'].get('priority', {}).get('id', {})
        body['priority_name'] = issue['fields'].get('priority', {}).get('name', {})
        body['issuetype'] = issue['fields'].get('issuetype', {}).get('name', {})
        body['project'] = issue['fields'].get('project', {}).get('name', {})
        body['epic_link'] = issue['fields'].get('customfield_10008', None)
        body['story_points'] = issue['fields'].get('customfield_10004', None)
        if issue['fields'].get('customfield_11600', None):
            body['sponsoring_team'] = issue['fields']['customfield_11600'].get('value', None)
        if issue['fields'].get('resolution', None):
            body['resolution'] = issue['fields'].get('resolution', None).get('name', None)
        if updated_date:
            body['updated'] = int(datetime.timestamp(datetime.strptime(updated_date, "%Y-%m-%dT%H:%M:%S.%f%z")))
        if created_date:
            body['created'] = int(datetime.timestamp(datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S.%f%z")))
        if issue['fields'].get('assignee', {}):
            body['assignee_name'] = issue['fields'].get('assignee', {}).get('displayName', {})
        if issue['fields'].get('customfield_10005', {}):
            body['epic_name'] = issue['fields'].get('customfield_10005', None)
        if issue['fields'].get('customfield_10007', None):
            body.update(self.parse_sprint_data(issue['fields']['customfield_10007']))
        if issue['fields'].get('labels', None):
            body['labels'] = self.parse_label_data(issue['fields']['labels'])
        return body

    @staticmethod
    def parse_sprint_data(sprint):
        """Parse raw sprint string."""
        sprint_body = {
            'sprint_status': sprint[0].split('state=')[1].split(',', 1)[0],
            'sprint_name': sprint[0].split('name=')[1].split(',', 1)[0],
            'sprint_goal': sprint[0].split('goal=')[1].split(',', 1)[0],
        }
        return sprint_body

    @staticmethod
    def parse_label_data(labels):
        """Parse list of labels."""
        labels = ', '.join(labels)
        return labels
