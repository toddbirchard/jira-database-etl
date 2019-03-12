import os
from sqlalchemy import create_engine
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def upload_dataframe(jira_df):
    """Upload JIRA df to Postgres."""
    print('test')
    URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    print('URI = ', URI)
    engine = create_engine(URI, echo=True)
    jira_df.to_sql('jira', engine, schema='public', if_exists='replace', dtype=None)