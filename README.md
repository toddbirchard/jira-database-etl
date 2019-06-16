# JIRA-to-Database Import

![Python](https://img.shields.io/badge/Python-v3.7-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Pandas](https://img.shields.io/badge/Pandas-v0.23.0-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Requests](https://img.shields.io/badge/Requests-v2.21.0-red.svg?longCache=true&logo=python&longCache=true&style=flat-square&logoColor=white&colorA=4c566a&colorB=5e81ac)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-v1.3.1-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)
![Psycopg2-binary](https://img.shields.io/badge/Psycopg2--binary-v2.7.7-red.svg?longCache=true&logo=delicious&longCache=true&style=flat-square&logoColor=white&colorA=4c566a&colorB=bf616a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c&logo=GitHub)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/jira-database-etl.svg?style=flat-square&colorA=4c566a&colorB=ebcb8b&logo=GitHub)](https://github.com/toddbirchard/jira-database-etl/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/jira-database-etl.svg?style=flat-square&colorA=4c566a&&colorB=ebcb8b&logo=GitHub)](https://github.com/toddbirchard/jira-database-etl/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/jira-database-etl.svg?style=flat-square&colorA=4c566a&colorB=ebcb8b&logo=GitHub)](https://github.com/toddbirchard/jira-database-etl/network&logo=GitHub)


Python script triggered by a nightly CRON job. Extracts issues from a JIRA instance via the JIRA REST API, transforms the data, and uploads said data to a database. Useful for creating widgets such as public-facing Kanban boards, or doing analysis.
