import os
from sqlalchemy import create_engine
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def upload_dataframe_to_database(jira_df):
    """Upload JIRA df to Postgres."""
    print('test')
    URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    print('URI = ', URI)
    engine = create_engine(URI, echo=True)
    jira_df.to_sql('jira', engine, schema='public', if_exists='replace', dtype=None)
    success_message = 'Successfully uploaded' + str(jira_df.count) + ' rows to ' + os.environ.get('SQLALCHEMY_DATABASE_NAME')
    return success_message
