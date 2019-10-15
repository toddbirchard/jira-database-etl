import math
import requests
from config import Config


class FetchJiraIssues:
    """Fetch all public-facing issues from JIRA instance.

    1. Retrieve all values from env vars.
    2. Construct request against JIRA REST API.
    3. Fetch paginated issues via recursion.
    4. Pass final JSON to be transformed into a DataFrame.
    """

    def __init__(self):
        self.jira_username = Config.jira_username
        self.jira_password = Config.jira_password
        self.jira_endpoint = Config.jira_endpoint
        self.jira_jql = Config.jira_jql
        self.results_per_page = 100
        self.num_issues = self.get_total_number_of_issues()

    def get_total_number_of_issues(self):
        """Gets the total number of results."""
        params = {
            "jql": self.jira_jql,
            "maxResults": 0,
            "startAt": 0}
        req = requests.get(self.jira_endpoint,
                           headers={"Accept": "application/json"},
                           params=params,
                           auth=(self.jira_username, self.jira_password))
        return req.json()['total']
        '''try:
            total_results = response['total']
            return total_results
        except KeyError:
            print('Could not find any issues!')'''

    def fetch_all_results(self):
        """Recursively retrieve all pages of JIRA issues."""
        issue_arr = []

        def fetch_single_page(total_results):
            """Fetch one page of results, determine if more pages exist."""
            params = {
                "jql": self.jira_jql,
                "maxResults": self.results_per_page,
                "startAt": len(issue_arr)}
            req = requests.get(self.jira_endpoint,
                               headers={"Accept": "application/json"},
                               params=params,
                               auth=(self.jira_username, self.jira_password))
            response = req.json()
            issues = response['issues']
            issues_so_far = len(issue_arr) + self.results_per_page
            print(f'{issues_so_far} out of {self.num_issues}')
            issue_arr.extend(issues)
            # Check if additional pages of results exist.
        count = math.ceil(self.num_issues/self.results_per_page)
        for x in range(0, count):
            fetch_single_page(self.num_issues)
        return issue_arr
