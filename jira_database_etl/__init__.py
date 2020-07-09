from config import Config
from loguru import logger
from .jirafetch import FetchJiraIssues
from .transform import TransformData
from .db import Database


def init_script():
    """Extract, transform, and load issues from JIRA to an RDBMS."""
    issues, epics = fetch_jira_issues()
    issues, epics = clean_jira_issues(issues, epics)
    upload = upload_issues(issues, epics)
    logger.info(upload)


def fetch_jira_issues():
    """Fetch raw JSON data for JIRA issues."""
    jira = FetchJiraIssues(Config)
    issues_json = jira.get_issues()
    epics_json = jira.get_epics()
    return issues_json, epics_json


def clean_jira_issues(issues, epics):
    """Clean data and create pandas DataFrame."""
    logger.info('Transforming JIRA issues to tabular data...')
    transform_data = TransformData()
    issues_df = transform_data.construct_dataframe(issues)
    epics_df = transform_data.construct_dataframe(epics)
    return issues_df, epics_df


def upload_issues(issues, epics):
    """Upload issues table to SQL database."""
    logger.info("Preparing database upload...")
    db = Database(Config)
    epics_upload = db.upload_epics(epics)
    issues_upload = db.upload_issues(issues)
    return epics_upload, issues_upload
