import os
import logging
from sqlalchemy import create_engine
import pandas as pd

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def upload_dataframe_to_database(jira_df):
    """Upload JIRA df to Postgres."""
    URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    epic_table = os.environ.get('SQLALCHEMY_EPIC_TABLE')
    jira_table = os.environ.get('SQLALCHEMY_JIRA_TABLE')
    db_name = 'hackers-graphql'
    engine = create_engine(URI, echo=True)
    epics_df = pd.read_sql_query('SELECT * FROM ' + epic_table, con=engine)
    jira_df = pd.merge(jira_df, epics_df, how='left', on='epic_link')
    jira_df = jira_df.rename({"index": "id"}, axis='columns')
    jira_df.to_sql(jira_table, engine, if_exists='replace', schema='hackers$prod', dtype=None)
    success_message = 'Successfully uploaded' + str(jira_df.count) + ' rows to ' + db_name
    return success_message
