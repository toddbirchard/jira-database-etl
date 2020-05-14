# JIRA-to-Database Import

![Python](https://img.shields.io/badge/Python-v3.8-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Pandas](https://img.shields.io/badge/Pandas-v^1.0.0-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Requests](https://img.shields.io/badge/Requests-v2.22.0-red.svg?longCache=true&logo=python&longCache=true&style=flat-square&logoColor=white&colorA=4c566a&colorB=5e81ac)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v1.3.1-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)
![PyMySQL](https://img.shields.io/badge/PyMySQL-v0.9.3-red.svg?longCache=true&logo=mysql&longCache=true&style=flat-square&logoColor=white&colorA=4c566a&colorB=bf616a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c&logo=GitHub)

![JIRA SQL ETL](https://storage.googleapis.com/hackersandslackers-cdn/2019/03/jira-etl-3-3@2x.jpg)

Extracts issues from a JIRA instance via the JIRA REST API, transforms the data, and loads data to a database.

To derive epic-based information from tickets, the script creates an `JiraEpic` table as well as a `JiraIssue` table. The `JiraIssue` table is joined with the former table to easily perform analysis on aggregated epic data.

Accompanying tutorial can be found here: https://hackersandslackers.com/jira-to-sql-etl/

## Installation

**Installation via `requirements.txt`**:

```shell
$ git clone https://github.com/toddbirchard/jira-database-etl.git
$ cd jira-database-etl
$ python3 -m venv myenv
$ source myenv/bin/activate
$ pip3 install -r requirements.txt
$ flask run
```

**Installation via [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)**:

```shell
$ git clone https://github.com/toddbirchard/jira-database-etl.git
$ cd jira-database-etl
$ pipenv shell
$ pipenv update
$ flask run
```

## Configuration

The following environment variables are needed to run this script:


* `SQLALCHEMY_DATABASE_URI`: A URI for the database intended to store these tables (ie: _mysql+pymysql://[USER]:[PASSWORD]@d[DATABASE_HOST]:[PORT]/[DATABASE_NAME]_)
* `SQLALCHEMY_EPIC_TABLE`: Name of database table to store epics.
* `SQLALCHEMY_JIRA_TABLE`: Name of database table to store JIRA issues.
* `JIRA_ENDPOINT`: Your JIRA Cloud API endpoint for JQL searching (such as *https://mydomain.atlassian.net/rest/api/3/search*)
* `JIRA_USERNAME`: Your JIRA username.
* `JIRA_API_KEY`: An API key associated with the JIRA user.
* `JIRA_ISSUES_JQL`: JQL to get JIRA issues.
* `JIRA_ISSUES_FIELDS`: Specific fields to retrieve from the JIRA query.
* `JIRA_EPICS_JQL`: JQL to get JIRA epics.
* `JIRA_EPICS_FIELDS`: Specific fields to retrieve from the epics query.


### Troubleshooting

Make sure your database contains tables named `JiraEpic` and `JiraIssue` prior to running this script (columns/schema don't matter, these will be overridden).

-----

This project and all publically-visible repositories are free of charge. If you've found this project to be helpful, a [small donation](https://www.buymeacoffee.com/hackersslackers) would be greatly appreciated to keep us in business. All proceeds go towards coffee, and all coffee goes towards improving these projects.
