import math
import requests
from loguru import logger


class FetchJiraIssues:
    """Fetch issues from JIRA instance matching JQL query."""

    def __init__(self, config):
        self.jira_username = config.jira_username
        self.jira_api_key = config.jira_api_key
        self.jira_endpoint = config.jira_endpoint
        self.jira_issues_jql = config.jira_issues_jql
        self.jira_issues_fields = config.jira_issues_fields
        self.jira_epics_jql = config.jira_epics_jql
        self.jira_epics_fields = config.jira_epics_fields
        self.results_per_page = 100

    def get_issues(self):
        """Fetch JIRA issues which are not Epics."""
        logger.info('Fetching issues from JIRA...')
        issues = self.__fetch_all_results(
            self.jira_issues_jql,
            self.jira_issues_fields
        )
        return issues

    def get_epics(self):
        """Fetch JIRA issues which are Epics."""
        logger.info('Fetching epics from JIRA...')
        issues = self.__fetch_all_results(
            self.jira_epics_jql,
            self.jira_epics_fields
        )
        return issues

    def __get_total_number_of_issues(self, jql):
        """Gets the total number of results to retrieve."""
        params = {
            "jql": jql,
            "maxResults": 0,
            "startAt": 0}
        req = requests.get(
            self.jira_endpoint,
            headers={"Accept": "application/json"},
            params=params,
            auth=(self.jira_username, self.jira_api_key)
        )
        total_results = req.json().get('total', None)
        if total_results:
            return total_results
        logger.info('Could not find any issues!')

    def __fetch_all_results(self, jql, fields):
        """Retrieve all JIRA issues."""
        num_issues = self.__get_total_number_of_issues(jql)
        issue_arr = []

        def fetch_single_page(jql, fields):
            """Fetch one page of results, determine if more pages exist."""
            params = {
                "jql": jql,
                "maxResults": self.results_per_page,
                "startAt": len(issue_arr),
                "validateQuery": "warn",
                "fields": fields}
            req = requests.get(
                self.jira_endpoint,
                headers={"Accept": "application/json"},
                params=params,
                auth=(self.jira_username, self.jira_api_key)
            )
            response = req.json()
            issues = response['issues']
            issues_so_far = len(issue_arr) + self.results_per_page
            if issues_so_far > num_issues:
                issues_so_far = num_issues
            logger.info(f'Fetched {issues_so_far} out of {num_issues} total issues.')
            issue_arr.extend(issues)
            # Check if additional pages of results exist.
        count = math.ceil(num_issues/self.results_per_page)
        for i in range(0, count):
            fetch_single_page(jql, fields)
        return issue_arr
