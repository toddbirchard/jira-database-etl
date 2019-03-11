from flask import Flask, make_response
from fetch import fetch_public_jira_issues
from data import create_issues_dataframe


def main():
    """Application Entry Point."""
    issues_json = fetch_public_jira_issues()
    issues_table = create_issues_dataframe(issues_json)
    pass


main()
