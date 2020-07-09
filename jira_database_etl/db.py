from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.types import Integer, Text, String
import pandas as pd


class Database:
    """Merge Epic metadata and upload JIRA issues."""

    def __init__(self, Config):
        self.db_uri = Config.db_uri
        self.db_jira_table = Config.db_jira_table
        self.db_epic_table = Config.db_epic_table
        self.engine = create_engine(
            self.db_uri,
            echo=False
        )

    def upload_epics(self, epics_df):
        """Create SQL table of JIRA epics."""
        self.__truncate_table(self.db_epic_table)
        result = self.__upload_dataframe(epics_df, self.db_epic_table)
        return result

    def upload_issues(self, issues_df):
        """Create SQL table of JIRA issues & JOIN with epic info."""
        self.__truncate_table(self.db_jira_table)
        issues_df = self.__merge_epic_metadata(issues_df)
        result = self.__upload_dataframe(issues_df, self.db_jira_table)
        return result

    def __truncate_table(self, table):
        """Clear existing SQL table."""
        sql = text(f'TRUNCATE TABLE {table}')
        self.engine.execute(sql)

    def __merge_epic_metadata(self, jira_issues_df):
        """Merge epic metadata from existing SQL table."""
        epics_df = pd.read_sql_table(
            self.db_epic_table,
            self.engine
        )
        logger.info(epics_df)
        jira_issues_df = pd.merge(
            jira_issues_df,
            epics_df[['key', 'epic_name']],
            how='left',
            left_on='epic_link',
            right_on='key',
            copy=False
        )
        jira_issues_df = jira_issues_df.rename(columns={"key_x": "key", "key_y": "epic_key"})
        return jira_issues_df

    def __upload_dataframe(self, issues_df, table):
        """Upload JIRA DataFrame to database."""
        issues_df.to_sql(
            table,
            self.engine,
            if_exists='replace',
            chunksize=500,
            index=False,
            dtype={
                "id": Integer,
                "assignee_name": String(30),
                "epic_link": String(50),
                "issuetype": String(50),
                "key": String(10),
                "priority_name": String(30),
                "priority_rank": Integer,
                "project": String(70),
                "status": String(30),
                "summary": Text,
                "resolution": String(70),
                "story_points": Integer,
                "labels": Text,
                "updated": Integer,
                "created": Integer,
                'sprint_status': String(255),
                'sprint_name': Text,
                'sprint_goal': Text,
                "epic_name": String(100)
            }
        )
        success_message = f'Uploaded {len(issues_df)} rows to {table} table.'
        return success_message
