from os import environ
import logging
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.types import Integer, Text, TIMESTAMP, String
import pandas as pd

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class DatabaseImport:
    """Merge Epic metadata and upload JIRA issues.

    1. Merge Epic metadata by fetching an existing table.
    2. Explicitly set data types for all columns found in jira_issues_df.
    2. Create a new table from the final jira_issues_df.
    """

    URI = environ.get('SQLALCHEMY_DATABASE_URI')
    db_epic_table = environ.get('SQLALCHEMY_EPIC_TABLE')
    db_jira_table = environ.get('SQLALCHEMY_JIRA_TABLE')
    db_schema = environ.get('SQLALCHEMY_DB_SCHEMA')

    # Create Engine
    meta = MetaData(schema=db_schema)
    engine = create_engine(URI,
                           connect_args={'sslmode':'require'},
                           echo=True)

    @staticmethod
    def truncate_table(engine):
        """Clear table of data."""
        sql = text('TRUNCATE TABLE "hackers$prod"."JiraIssue"')
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
        jira_issues_df = cls.merge_epic_metadata(jira_issues_df)
        jira_issues_df.to_sql(cls.db_jira_table,
                              cls.engine,
                              if_exists='append',
                              schema=cls.db_schema,
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
