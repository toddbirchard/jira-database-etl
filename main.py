from flask import request
from jira_etl import fetch
from jira_etl import data
from jira_etl import db


def main():
    """Application Entry Point.

    1. Fetch all desired JIRA issues from an instance's REST API.
    2. Sanitize the data and add secondary metadata.
    3. Upload resulting DataFrame to database.
    """
    jira_issues_json = fetch.FetchJiraIssues.fetch_all_results()
    jira_issues_df = data.TransformData.construct_dataframe(jira_issues_json)
    upload_status = db.DatabaseImport.upload_dataframe(jira_issues_df)
    return upload_status


main()
