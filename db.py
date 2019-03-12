import os
from sqlalchemy import create_engine


def upload_dataframe(jira_df):
    """Upload JIRA df to Postgres."""
    print('test')
    URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    print('URI = ', URI)
    engine = create_engine(URI, echo=False)
    jira_df.to_sql('jiraissues', engine, schema='public', if_exists='replace', dtype=None)