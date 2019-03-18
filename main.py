from flask import make_response
from jiraserverless.fetch import fetch_public_jira_issues
from jiraserverless.data import JiraDataFrameConstructor
from jiraserverless.db import upload_dataframe_to_database


def main():
    """Application Entry Point.

    1. Fetch all desired JIRA issues from an instance's REST API.
    2. Sanitize the data and add secondary metadata.
    3. Upload resulting DataFrame to database.
    """
    issues_json = fetch_public_jira_issues()
    jira_df = JiraDataFrameConstructor.construct_dataframe_for_upload(issues_json)
    upload_status = upload_dataframe_to_database(jira_df)
    return make_response(upload_status, 200)
