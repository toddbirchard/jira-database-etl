import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, TIMESTAMP
import pandas as pd

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class DatabaseImport:
    """Merge Epic metadata and upload JIRA issues."""

    URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    epic_table = os.environ.get('SQLALCHEMY_EPIC_TABLE')
    jira_table = os.environ.get('SQLALCHEMY_JIRA_TABLE')
    db_name = 'hackers-graphql'

    # Create Engine
    engine = create_engine(URI, echo=True)

    @classmethod
    def merge_epic_metadata(cls, jira_df):
        """Merge epic table."""
        epics_df = pd.read_sql_table(cls.epic_table, cls.engine, schema='hackers$prod')
        print(cls.epic_table)
        jira_df = pd.merge(jira_df, epics_df, how='left', on='epic_link', copy=False)
        return jira_df

    @classmethod
    def upload_dataframe_to_database(cls, jira_df):
        """Upload JIRA df to Postgres."""
        jira_df = cls.merge_epic_metadata(jira_df)
        jira_df.index(jira_df.iloc[0], name='id')
        jira_df.to_sql(cls.jira_table, cls.engine, if_exists='replace', schema='hackers$prod', dtype={"id": Integer,
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
        success_message = 'Successfully uploaded' + str(jira_df.count) + ' rows to ' + cls.db_name
        return success_message
