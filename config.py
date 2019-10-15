from os import environ


class Config:

    # Database
    db_uri = environ.get('SQLALCHEMY_DATABASE_URI')
    db_epic_table = environ.get('SQLALCHEMY_EPIC_TABLE')
    db_jira_table = environ.get('SQLALCHEMY_JIRA_TABLE')

    # JIRA
    jira_username = environ.get('JIRA_USERNAME')
    jira_password = environ.get('JIRA_PASSWORD')
    jira_endpoint = environ.get('JIRA_ENDPOINT')
    jira_jql = environ.get('JIRA_QUERY')
