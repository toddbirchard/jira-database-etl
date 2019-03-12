import os
import requests


def fetch_public_jira_issues():
    """Fetch all public-facing issues from JIRA instance.

    1. Retrieve all values from env vars.
    2. Construct request against JIRA REST API.
    3. """
    results_per_page = 100
    username = os.environ.get('JIRA_USERNAME')
    password = os.environ.get('JIRA_PASSWORD')
    endpoint = os.environ.get('JIRA_ENDPOINT')
    jql = os.environ.get('JIRA_QUERY')
    headers = {
        "Accept": "application/json"
    }
    arr = []

    def get_total_number_of_issues():
        """Gets the total number of results."""
        params = {
            "jql": jql,
            "maxResults": 0,
            "startAt": 0
        }
        req = requests.get(endpoint,
                           headers=headers,
                           params=params,
                           auth=(username, password)
                           )
        response = req.json()
        total_results = response['total']
        return total_results

    total_results = get_total_number_of_issues()

    def fetch_page_of_results():
        """Recursively retrieve all pages of JIRA issues."""
        params = {
            "jql": jql,
            "maxResults": results_per_page,
            "startAt": len(arr)
        }
        req = requests.get(endpoint,
                           headers=headers,
                           params=params,
                           auth=(username, password)
                           )
        response = req.json()
        issues = response['issues']
        print('number of issues = ', len(issues))
        print('current place = ', len(arr) + results_per_page)
        print('total = ', total_results)
        arr.extend(issues)
        if (len(arr) + results_per_page) < total_results:
            fetch_page_of_results()
        return arr

    results = fetch_page_of_results()
    return results


jira_issues = fetch_public_jira_issues()
