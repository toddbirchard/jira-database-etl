import os
import math
import requests


class fetchPublicJiraIssues:
    """Fetch all public-facing issues from JIRA instance.

    1. Retrieve all values from env vars.
    2. Construct request against JIRA REST API.
    3. Fetch paginated issues via recursion.
    4. Pass final JSON to be transformed into a DataFrame.
     """
    results_per_page = 100
    username = os.environ.get('JIRA_USERNAME')
    password = os.environ.get('JIRA_PASSWORD')
    endpoint = os.environ.get('JIRA_ENDPOINT')
    jql = 'project in ("Hackers and Slackers", "DevOps", "Linkbox API", "Roblog", "Toddzilla", "Tableau Extraction", "ghostthemes.io") AND status != Decline ORDER BY updated DESC'
    headers = {
        "Accept": "application/json"
    }

    @classmethod
    def get_total_number_of_issues(cls):
        """Gets the total number of results."""
        params = {
            "jql": cls.jql,
            "maxResults": 0,
            "startAt": 0
        }
        req = requests.get(cls.endpoint,
                           headers=cls.headers,
                           params=params,
                           auth=(cls.username, cls.password)
                           )
        response = req.json()
        try:
            total_results = response['total']
            return total_results
        except KeyError:
            print('Could not find any issues!')

    @classmethod
    def fetch_all_pages_of_results(cls):
        """Recursively retrieve all pages of JIRA issues."""
        total_results = cls.get_total_number_of_issues()
        issue_arr = []

        def fetch_single_page():
            params = {
                "jql": cls.jql,
                "maxResults": cls.results_per_page,
                "startAt": len(issue_arr)
            }
            req = requests.get(cls.endpoint,
                               headers=cls.headers,
                               params=params,
                               auth=(cls.username, cls.password)
                               )
            response = req.json()
            issues = response['issues']
            issues_so_far = len(issue_arr) + cls.results_per_page
            print(issues_so_far, ' out of', total_results)
            issue_arr.extend(issues)
            # Check if additional pages of results exist.
        count = math.ceil(total_results/cls.results_per_page)
        for x in range(0, count):
            fetch_single_page()
        return issue_arr


jira_issues = fetchPublicJiraIssues.fetch_all_pages_of_results()
