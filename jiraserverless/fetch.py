import os
import requests


def fetch_public_jira_issues():
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
        try:
            total_results = response['total']
            return total_results
        except KeyError:
            print('Could not find any issues!')


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
        issues_so_far = len(arr) + results_per_page
        print(issues_so_far, ' out of', total_results)
        arr.extend(issues)
        # Check if additional pages of results exist.
        if issues_so_far < total_results:
            fetch_page_of_results()
        return arr

    results = fetch_page_of_results()
    return results


jira_issues = fetch_public_jira_issues()
