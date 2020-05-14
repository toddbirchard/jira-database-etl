"""Project configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:

    # Database config
    db_uri = environ.get('SQLALCHEMY_DATABASE_URI')
    db_epic_table = environ.get('SQLALCHEMY_EPIC_TABLE')
    db_jira_table = environ.get('SQLALCHEMY_JIRA_TABLE')

    # JIRA config
    jira_username = environ.get('JIRA_USERNAME')
    jira_api_key = environ.get('JIRA_API_KEY')
    jira_endpoint = environ.get('JIRA_ENDPOINT')
    jira_issues_jql = environ.get('JIRA_ISSUES_JQL')
    jira_issues_fields = environ.get('JIRA_ISSUES_FIELDS')
    jira_epics_jql = environ.get('JIRA_EPICS_JQL')
    jira_epics_fields = environ.get('JIRA_EPICS_FIELDS')
