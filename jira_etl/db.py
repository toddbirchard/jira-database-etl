import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, TIMESTAMP
import pandas as pd

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class DatabaseImport:
    """Merge Epic metadata and upload JIRA issues.

    1. Merge Epic metadata by fetching an existing table.
    2. Explicitly set data types for all columns found in jira_issues_df.
    2. Create a new table from the final jira_issues_df.
    """

    URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    db_epic_table = os.environ.get('SQLALCHEMY_EPIC_TABLE')
    db_jira_table = os.environ.get('SQLALCHEMY_JIRA_TABLE')
    db_schema = os.environ.get('SQLALCHEMY_DB_SCHEMA')

    # Create Engine
    engine = create_engine(URI, echo=True)

    @classmethod
    def merge_epic_metadata(cls, jira_issues_df):
        """Merge epic metadata from existing SQL table."""
        epics_df = pd.read_sql_table(cls.db_epic_table,
                                     cls.engine,
                                     schema=cls.db_schema)
        jira_issues_df = pd.merge(jira_issues_df,
                                  epics_df[['epic_link', 'epic_name', 'epic_color']],
                                  how='left',
                                  on='epic_link',
                                  copy=False)
        return jira_issues_df

    @classmethod
    def upload_dataframe(cls, jira_issues_df):
        """Upload JIRA DataFrame to PostgreSQL database."""
        jira_issues_df = cls.merge_epic_metadata(jira_issues_df)
        jira_issues_df.to_sql(cls.db_jira_table, 
                              cls.engine, 
                              if_exists='replace', 
                              schema=cls.db_schema, 
                              dtype={"id": Integer,
                                     "assignee": Text,
                                     "assignee_url": Text,
                                     "epic_link": Text,
                                     "issuetype": Text,
                                     "issuetype_icon": Text,
                                     "key": Text,
                                     "priority": Text,
                                     "priority_rank": Text,
                                     "priority_url": Text,
                                     "project": Text,
                                     "status": Text,
                                     "summary": Text,
                                     "updated": Text,
                                     "updatedAt": TIMESTAMP,
                                     "createdAt": TIMESTAMP,
                                     "epic_color": Text,
                                     "epic_name": Text
                                     })
        success_message = 'Successfully uploaded' \
                          + str(jira_issues_df.count) \
                          + str(jira_issues_df.count) \
                          + ' rows to ' + cls.db_jira_table
        return success_message
