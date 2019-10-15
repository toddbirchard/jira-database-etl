from jira_etl.fetch import FetchJiraIssues
from jira_etl.data import TransformData
from jira_etl.db import Database


def main():
    """Application Entry Point.

    1. Fetch all desired JIRA issues from an instance's REST API.
    2. Sanitize the data and add secondary metadata.
    3. Upload resulting DataFrame to database.
    """
    jira_issues = FetchJiraIssues()
    jira_issues_json = jira_issues.fetch_all_results()
    jira_issues_df = TransformData.construct_dataframe(jira_issues_json)
    upload_status = Database.upload_dataframe(jira_issues_df)
    return upload_status


main()
