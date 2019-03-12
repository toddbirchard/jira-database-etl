from flask import make_response, request
from fetch import fetch_public_jira_issues
from data import JiraDataframeConstructor
from db import upload_dataframe


def main(request):
    """Application Entry Point."""
    issues_json = fetch_public_jira_issues()
    jira_df = JiraDataframeConstructor.add_issues_to_dataframe(issues_json)
    upload_dataframe(jira_df)
    return make_response(str(jira_df.describe()), 200)
