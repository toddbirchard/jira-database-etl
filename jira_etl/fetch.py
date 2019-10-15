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
    jira_username = Config.jira_username
    jira_password = Config.jira_password
    jira_endpoint = Config.jira_endpoint
    jira_jql = Config.jira_jql
    results_per_page = 100

    headers = {
        "Accept": "application/json"
    }

    @classmethod
    def get_total_number_of_issues(cls):
        """Gets the total number of results."""
        params = {
            "jql": cls.jira_jql,
            "maxResults": 0,
            "startAt": 0
        }
        req = requests.get(cls.jira_endpoint,
                           headers=cls.headers,
                           params=params,
                           auth=(cls.jira_username, cls.jira_password)
                           )
        response = req.json()
        try:
            total_results = response['total']
            return total_results
        except KeyError:
            print('Could not find any issues!')

    @classmethod
    def fetch_all_results(cls):
        """Recursively retrieve all pages of JIRA issues."""
        issue_arr = []
        total_results = cls.get_total_number_of_issues()

        def fetch_single_page(total_results):
            """Fetch one page of results and determine if another page exists."""
            params = {
                "jql": cls.jira_jql,
                "maxResults": cls.results_per_page,
                "startAt": len(issue_arr)
            }
            req = requests.get(cls.jira_endpoint,
                               headers=cls.headers,
                               params=params,
                               auth=(cls.jira_username, cls.jira_password)
                               )
            response = req.json()
            issues = response['issues']
            issues_so_far = len(issue_arr) + cls.results_per_page
            print(issues_so_far, ' out of', total_results)
            issue_arr.extend(issues)
            # Check if additional pages of results exist.
        count = math.ceil(total_results/cls.results_per_page)
        for x in range(0, count):
            fetch_single_page(total_results)
        return issue_arr
