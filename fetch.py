import os
import requests


def fetch_public_jira_issues():
    """Fetch all public-facing issues from JIRA instance."""
    endpoint = "https://hackersandslackers.atlassian.net/rest/api/3/search"
    jql = 'project in ("Hackers and Slackers", DevOps, hackersndslackers-api, linkbox, Roblog, Toddzilla, "Tableau Extraction", "ghostthemes.io") AND status != Decline ORDER BY updated DESC'
    username = os.environ.get('JIRA_USERNAME')
    password = os.environ.get('JIRA_PASSWORD')
    headers = {
        "Accept": "application/json"
        }
    params = {
        "jql": jql
    }
    req = requests.get(endpoint,
                       headers=headers,
                       params=params,
                       auth=(username, password)
                       )
    response = req.json()
    return response
