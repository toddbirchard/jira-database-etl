import logging
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, Text, TIMESTAMP, String
import pandas as pd
from config import Config


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class Database:
    """Merge Epic metadata and upload JIRA issues.

    1. Merge Epic metadata by fetching an existing table.
    2. Explicitly set data types for all columns found in jira_issues_df.
    2. Create a new table from the final jira_issues_df.
    """

    db_uri = Config.db_uri
    db_jira_table = Config.db_jira_table

    # Create Engine
    engine = create_engine(db_uri,
                           echo=True)

    @staticmethod
    def truncate_table(engine):
        """Clear table of data."""
        sql = text('TRUNCATE TABLE JiraIssue"')
        engine.execute(sql)

    @classmethod
    def merge_epic_metadata(cls, jira_issues_df):
        """Merge epic metadata from existing SQL table."""
        cls.truncate_table(cls.engine)
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
        # jira_issues_df = cls.merge_epic_metadata(jira_issues_df)
        jira_issues_df.to_sql(cls.db_jira_table,
                              cls.engine,
                              if_exists='append',
                              index=False,
                              dtype={"assignee": String(30),
                                     "assignee_url": Text,
                                     "epic_link": String(50),
                                     "issuetype_name": String(50),
                                     "issuetype_icon": Text,
                                     "key": String(10),
                                     "priority_name": String(30),
                                     "priority_rank": Integer,
                                     "priority_url": Text,
                                     "project": String(50),
                                     "status": String(30),
                                     "summary": Text,
                                     "updated": Integer,
                                     "updatedAt": TIMESTAMP,
                                     "createdAt": TIMESTAMP,
                                     "epic_color": String(20),
                                     "epic_name": String(50)})
        success_message = 'Successfully uploaded' \
                          + str(jira_issues_df.count) \
                          + str(jira_issues_df.count) \
                          + ' rows to ' + cls.db_jira_table
        return success_message
