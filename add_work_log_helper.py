# Helper method to add a work-log against a JIRA issue.
# Note that work will be logged as the user who's token is being used
import json

import re
import subprocess
import os

JIRA_BASE_URL = "https://aasaan-jobs.atlassian.net"
JIRA_BOT_ADMIN_TOKEN = os.getenv('JIRA_BOT_ADMIN_TOKEN')


def _add_work_log(issue_key, work_log_str):
    """
        Accepts a JIRA issue key/name and a work_log string and adds a work-log entry against the issue.
        :param issue_key: JIRA card name. eg: API-988, CTS-504 etc...
        :param work_log_str: The time that is to be logged on the issue. eg: 1d 2h 30m
        :return:
    """
    add_work_log_endpoint = "/rest/api/3/issue/{}/worklog"
    work_log_api_url = JIRA_BASE_URL + add_work_log_endpoint.format(issue_key)
    data = {
        "timeSpent": work_log_str,
    }
    bash_command = "curl " \
                   "--request POST --url '{}' " \
                   "--header 'Accept: application/json' " \
                   "--header 'Content-Type: application/json'  " \
                   "--header 'Authorization: Basic {}' --data '{}'" \
                   "".format(work_log_api_url, JIRA_BOT_ADMIN_TOKEN, json.dumps(data))
    output = subprocess.check_output(['bash', '-c', bash_command])  # bytes object is returned


def _get_jira_issue(input_str):
    """Use regex matching to parse the input string/list of input strings and find a matching JIRA issue"""
    if not isinstance(input_str, list):
        input_str = [input_str]
    for _ in input_str:
        match = re.search(r"[A-Z]+-\d+", _)
        if match:
            return match.group()
    return None


def log_work_on_jira(branch, commit_msg):
    # Try to fetch the jira issue name from the branch or commit_msg
    try:
        jira_issue = _get_jira_issue([branch, commit_msg])
        if jira_issue:
            # Commit msgs should be in the format: "Message.... # Time to Log"
            # eg: "Adding new model for Employee # 3h 30m"
            if "#" not in commit_msg:
                print("Failed to Log for Branch[{}] Commit-message[{}]. Error: # format of time not present")
                return
            work_log_str = commit_msg.rsplit("#", 1)[1].strip()
            _add_work_log(jira_issue, work_log_str)
            print("Successfully Logged for Branch[{}] Commit-message[{}]".format(branch, commit_msg))
    except Exception as e:
        print("Failed to Log for Branch[{}] Commit-message[{}]. Error: {}".format(branch, commit_msg, str(e)))


# def get_current_branch():
#     """Fetches the name of the currently checked out branch assuming it is being run in a git folder"""
#     bash_command = "git branch | grep '*'"  # Fetch the current branch
#     output = subprocess.check_output(['bash', '-c', bash_command])  # bytes object is returned
#     branch_name = output.decode("utf-8").strip("*").strip()
#     return branch_name


# def get_last_commit_message():
#     """Fetches the commit message of the last commit from git log"""
#     # Calculate the number of lines in the last entry in git log
#     bash_command = "git log -1 | wc -l"  # Fetch the current branch
#     output = subprocess.check_output(['bash', '-c', bash_command])  # bytes object is returned
#     number_of_lines = int(output.decode("utf-8").strip())
#
#     lines_to_skip = 4
#     # Commit msg format is -
#     # Commit Hash,
#     # Author,
#     # Date,
#     # Blank Line,
#     # Message
#
#     # Get the commit message from the last entry in git log
#     bash_command = "git log -1 | tail -{}".format(str(number_of_lines - lines_to_skip))  # Fetch the current branch
#     output = subprocess.check_output(['bash', '-c', bash_command])  # bytes object is returned
#     commit_message = output.decode("utf-8").strip()
#     return commit_message


# if __name__ == "__main__":
#     branch = get_current_branch()
#     commit_msg = get_last_commit_message()
#     # Try to fetch the jira issue name from the branch or commit_msg
#     jira_issue = get_jira_issue([branch, commit_msg])
#     if jira_issue:
#         # Commit msgs should be in the format: "Message.... # Time to Log"
#         # eg: "Adding new model for Employee # 3h 30m"
#         work_log_str = commit_msg.rsplit("#", 1)[1].strip()
#         # add_work_log(jira_issue, work_log_str)
#         add_work_log(jira_issue, work_log_str)
