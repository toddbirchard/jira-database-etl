from jiraserverless import fetch
from jiraserverless import data
from jiraserverless import db


def main():
    """Application Entry Point.

    1. Fetch all desired JIRA issues from an instance's REST API.
    2. Sanitize the data and add secondary metadata.
    3. Upload resulting DataFrame to database.
    """
    issues_json = fetch.FetchPublicJiraIssues.fetch_all_pages_of_results()
    jira_df = data.JiraDataFrameConstructor.construct_dataframe_for_upload(issues_json)
    upload_status = db.DatabaseImport.upload_dataframe_to_database(jira_df)
    return upload_status


main()
