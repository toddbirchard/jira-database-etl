import os
from sqlalchemy import create_engine

URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(URI, echo=False)

def upload_dataframe(jira_df):
    """Upload JIRA df to Postgres."""
    jira_df.to_sql('jiraissues', engine, schema='public', if_exists='replace', dtype=None)